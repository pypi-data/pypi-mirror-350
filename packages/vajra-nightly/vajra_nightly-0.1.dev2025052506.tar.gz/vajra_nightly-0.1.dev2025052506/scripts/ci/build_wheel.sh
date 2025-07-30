#!/bin/bash
set -ex

_script_dir="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd )"
source "${_script_dir}/utils.sh"

assert_env PYPI_RELEASE_CUDA_VERSION
assert_env PYPI_RELEASE_TORCH_VERSION
assert_env IS_NIGHTLY_BUILD

init_conda
activate_vajra_conda_env
switch_to_root_dir
install_pip_dependencies

echo "::group::Build wheel for Vajra"
make build/wheel
ls -la dist/
echo "::endgroup::"
