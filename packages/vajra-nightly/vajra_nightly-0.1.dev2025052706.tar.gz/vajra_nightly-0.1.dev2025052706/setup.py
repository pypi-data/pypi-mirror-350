import io
import os
import subprocess
import sys
from datetime import datetime
from typing import List
import glob

from packaging.version import parse, Version
from setuptools import setup, find_packages, Extension
from setuptools.command.build_ext import build_ext
from setuptools.command.build_py import build_py
from setuptools_scm import get_version
from shutil import which
import torch
from torch.utils.cpp_extension import CUDA_HOME

ROOT_DIR = os.path.dirname(__file__)

# Vajra only supports Linux platform
assert sys.platform.startswith(
    "linux"), "Vajra only supports Linux platform ."


def is_sccache_available() -> bool:
    return which("sccache") is not None


def is_ccache_available() -> bool:
    return which("ccache") is not None


def is_ninja_available() -> bool:
    return which("ninja") is not None


def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text


def get_vajra_version() -> str:
    version = get_version(
        write_to="vajra/_version.py",  # TODO: move this to pyproject.toml
    )

    if _is_cuda():
        cuda_version = str(get_nvcc_cuda_version())
        cuda_version_str = cuda_version.replace(".", "")[:3]
        torch_version = torch.__version__.split("+")[0]
        torch_version = torch_version.split("-")[0]
        torch_version_str = torch_version.replace(".", "")[:3]

        pypi_release_cuda_version = os.getenv("PYPI_RELEASE_CUDA_VERSION", "")
        pypi_release_torch_version = os.getenv("PYPI_RELEASE_TORCH_VERSION", "")

        is_pypi_release = (
            pypi_release_cuda_version == cuda_version_str
            and pypi_release_torch_version == torch_version_str
        )

        is_nightly_build = os.getenv("IS_NIGHTLY_BUILD", "false") == "true"

        if is_nightly_build:
            # the version would be something like 0.0.2.dev17+g6833d6f
            # but for nightly builds, we want to keep the version as 0.0.2.dev{datetime}
            # remove part after dev and replace it with the current datetime
            version = version.split("dev")[0] + f"dev{datetime.now().strftime('%Y%m%d%H')}"

        # a version name can't have two "+" characters
        # so if the name already has a "+" character, we can add
        # the cuda and torch version as a suffix with "."
        # else we can add it with "+"
        sep = "." if "+" in version else "+"

        # skip this for source tarball, required for pypi
        if "sdist" not in sys.argv and not is_pypi_release:
            version += f"{sep}cu{cuda_version_str}torch{torch_version_str}"
    else:
        raise RuntimeError("Unknown runtime environment")

    return version


class CMakeExtension(Extension):

    def __init__(self, name: str, cmake_lists_dir: str = '.', **kwa) -> None:
        super().__init__(name, sources=[], **kwa)
        self.cmake_lists_dir = os.path.abspath(cmake_lists_dir)


class cmake_build_ext(build_ext):
    # A dict of extension directories that have been configured.
    did_config = {}

    #
    # Determine number of compilation jobs and optionally nvcc compile threads.
    #
    def compute_num_jobs(self):
        try:
            # os.sched_getaffinity() isn't universally available, so fall back
            # to os.cpu_count() if we get an error here.
            num_jobs = len(os.sched_getaffinity(0))
        except AttributeError:
            num_jobs = os.cpu_count()

        nvcc_cuda_version = get_nvcc_cuda_version()
        if nvcc_cuda_version >= Version("11.2"):
            nvcc_threads = int(os.getenv("NVCC_THREADS", 8))
            num_jobs = max(1, round(num_jobs / (nvcc_threads / 4)))
        else:
            nvcc_threads = None

        return num_jobs, nvcc_threads

    #
    # Perform cmake configuration for a single extension.
    #
    def configure(self, ext: CMakeExtension) -> None:
        # If we've already configured using the CMakeLists.txt for
        # this extension, exit early.
        if ext.cmake_lists_dir in cmake_build_ext.did_config:
            return

        cmake_build_ext.did_config[ext.cmake_lists_dir] = True

        # Select the build type.
        # Note: optimization level + debug info are set by the build type
        default_cfg = "Debug" if self.debug else "RelWithDebInfo"
        cfg = os.getenv("CMAKE_BUILD_TYPE", default_cfg)

        # where .so files will be written, should be the same for all extensions
        # that use the same CMakeLists.txt.
        outdir = os.path.abspath(
            os.path.dirname(self.get_ext_fullpath(ext.name)))

        cmake_args = [
            '-DCMAKE_BUILD_TYPE={}'.format(cfg),
            '-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={}'.format(outdir),
            '-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY={}'.format(self.build_temp),
        ]

        verbose = bool(int(os.getenv('VERBOSE', '0')))
        if verbose:
            cmake_args += ['-DCMAKE_VERBOSE_MAKEFILE=ON']

        if is_sccache_available():
            cmake_args += [
                '-DCMAKE_CXX_COMPILER_LAUNCHER=sccache',
                '-DCMAKE_CUDA_COMPILER_LAUNCHER=sccache',
            ]
        elif is_ccache_available():
            cmake_args += [
                '-DCMAKE_CXX_COMPILER_LAUNCHER=ccache',
                '-DCMAKE_CUDA_COMPILER_LAUNCHER=ccache',
            ]

        # Pass the python executable to cmake so it can find an exact
        # match.
        cmake_args += ['-DVAJRA_PYTHON_EXECUTABLE={}'.format(sys.executable)]

        #
        # Setup parallelism and build tool
        #
        num_jobs, nvcc_threads = self.compute_num_jobs()

        if nvcc_threads:
            cmake_args += ['-DNVCC_THREADS={}'.format(nvcc_threads)]

        if is_ninja_available():
            build_tool = ['-G', 'Ninja']
            cmake_args += [
                '-DCMAKE_JOB_POOL_COMPILE:STRING=compile',
                '-DCMAKE_JOB_POOLS:STRING=compile={}'.format(num_jobs),
            ]
        else:
            # Default build tool to whatever cmake picks.
            build_tool = []

        subprocess.check_call(
            ['cmake', ext.cmake_lists_dir, *build_tool, *cmake_args],
            cwd=self.build_temp)

    def build_extensions(self) -> None:
        # Ensure that CMake is present and working
        try:
            subprocess.check_output(['cmake', '--version'])
        except OSError as e:
            raise RuntimeError('Cannot find CMake executable') from e

        # Create build directory if it does not exist.
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)

        # Build all the extensions
        for ext in self.extensions:
            self.configure(ext)

            ext_target_name = remove_prefix(ext.name, "vajra.")
            num_jobs, _ = self.compute_num_jobs()

            build_args = [
                '--build', '.', '--target', ext_target_name, '-j',
                str(num_jobs)
            ]

            subprocess.check_call(['cmake', *build_args], cwd=self.build_temp)


def _is_cuda() -> bool:
    return torch.version.cuda is not None


def get_nvcc_cuda_version() -> Version:
    """Get the CUDA version from nvcc.

    Adapted from https://github.com/NVIDIA/apex/blob/8b7a1ff183741dd8f9b87e7bafd04cfde99cea28/setup.py
    """
    nvcc_output = subprocess.check_output([CUDA_HOME + "/bin/nvcc", "-V"],
                                          universal_newlines=True)
    output = nvcc_output.split()
    release_idx = output.index("release") + 1
    nvcc_cuda_version = parse(output[release_idx].split(",")[0])
    return nvcc_cuda_version


def get_path(*filepath) -> str:
    return os.path.join(ROOT_DIR, *filepath)


def read_readme() -> str:
    """Read the README file if present."""
    p = get_path("README.md")
    if os.path.isfile(p):
        return io.open(get_path("README.md"), "r", encoding="utf-8").read()
    else:
        return ""


def get_requirements() -> List[str]:
    """Get Python package dependencies from requirements.txt."""
    if _is_cuda():
        with open(get_path("requirements.txt")) as f:
            requirements = f.read().strip().split("\n")
    else:
        raise ValueError(
            "Unsupported platform, please use CUDA.")

    return requirements


def get_package_name() -> str:
    # nightly builds are published under the vajra-nightly package
    if os.getenv("IS_NIGHTLY_BUILD", "false") == "true":
        return "vajra-nightly"

    return "vajra"

ext_modules = []

ext_modules.append(CMakeExtension(name="vajra._kernels"))
ext_modules.append(CMakeExtension(name="vajra._native"))

package_data = {
    get_package_name(): [
        "model_executor/layers/fused_moe/configs/*.json",
        "datatypes/generated/*.py",
    ]
}

setup(
    name=get_package_name(),
    author="Vajra Team",
    version=get_vajra_version(),
    license="Apache 2.0",
    description=("A high-throughput and low-latency LLM inference system"),
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: Apache Software License",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(exclude=("csrc")),
    python_requires=">=3.12",
    install_requires=get_requirements(),
    ext_modules=ext_modules,
    cmdclass={"build_ext": cmake_build_ext},
    package_data=package_data,
)
