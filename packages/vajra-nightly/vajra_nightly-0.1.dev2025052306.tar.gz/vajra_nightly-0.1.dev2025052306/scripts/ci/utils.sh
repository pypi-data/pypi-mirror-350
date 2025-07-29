#!/bin/bash
set -ex

# This script contains utility functions that can be shared across different scripts
# Note: This script should be sourced from other scripts and not executed directly
# and it is only suppose to contain function definitions & not any executable code

_script_dir="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd )"
_root_dir=$(dirname $(dirname $_script_dir))
_root_dir_parent=$(dirname "$_root_dir")
_vllm_dir="$_root_dir_parent/vllm"
_sgl_dir="$_root_dir_parent/sglang"
_mlc_dir="$_root_dir_parent/mlc-llm"

assert_env() {
    local var_name="$1"
    if [ -z "${!var_name}" ]; then
        echo "Error: Environment variable '$var_name' is not set."
        exit 1
    fi
}

function switch_to_root_dir() {
    cd "$_root_dir"
}

function init_conda() {
    export PATH="${HOME}/conda/bin:${PATH}"
    mamba shell init --shell=bash
    mamba shell init --shell=zsh
    source /root/conda/etc/profile.d/conda.sh
}

function login_huggingface() {
    huggingface-cli login --token "$HUGGINGFACE_TOKEN"
}

function activate_vajra_conda_env() {
    conda activate vajra
}

function activate_vllm_conda_env() {
    pushd "$_vllm_dir"
    conda activate vllm
    popd
}

function activate_sgl_conda_env() {
    pushd "$_sgl_dir"
    conda activate sglang
    popd
}

function activate_mlc_conda_env() {
    pushd "$_mlc_dir"
    conda activate mlc
    mamba env config vars set CONDA_CHANNELS="conda-forge,nvidia"
    conda deactivate
    conda activate mlc
    popd
}

function create_vajra_conda_env() {
    echo "::group::Create conda environment"
    pushd "$_root_dir"
    mamba env create -f environment-dev.yml -n vajra
    popd
    echo "::endgroup::"
}

function create_vllm_conda_env() {
    echo "::group::Create vllm conda environment"
    mkdir "$_vllm_dir"
    pushd "$_vllm_dir"
    mamba create -n vllm python=3.10
    popd
    echo "::endgroup::"
}

function create_sgl_conda_env() {
    echo "::group::Create sglang conda environment"
    pushd "$_sgl_dir"
    mamba create -n sglang python=3.10
    popd
    echo "::endgroup::"
}

function create_mlc_conda_env() {
    echo "::group::Create mlc-llm conda environment"
    mkdir "$_mlc_dir"
    pushd "$_mlc_dir"
    mamba create -n mlc python=3.11
    popd
    echo "::endgroup::"
}

function install_pip_dependencies() {
    assert_env VAJRA_CI_CUDA_VERSION
    assert_env VAJRA_CI_TORCH_VERSION

    CUDA_MAJOR="${VAJRA_CI_CUDA_VERSION%.*}"
    CUDA_MINOR="${VAJRA_CI_CUDA_VERSION#*.}"

    pushd "$_root_dir"

    echo "::group::Install PyTorch"
    pip install torch==${VAJRA_CI_TORCH_VERSION}.* \
        --index-url "https://download.pytorch.org/whl/cu${CUDA_MAJOR}${CUDA_MINOR}"
    echo "::endgroup::"

    echo "::group::Install other dependencies"
    pip install -r requirements.txt \
        --extra-index-url https://flashinfer.ai/whl/cu${CUDA_MAJOR}${CUDA_MINOR}/torch${VAJRA_CI_TORCH_VERSION}/
    echo "::endgroup::"

    popd
}

function clone_sgl() {
    pushd "$_root_dir_parent"
    git clone https://github.com/sgl-project/sglang.git
    popd
}

function build_vajra_editable() {
    pushd "$_root_dir"
    echo "::group::Build Vajra in editable mode"
    make build
    echo "::endgroup::"
    popd
}

function install_vllm() {
    pushd "$_vllm_dir"
    echo "::group::Build vllm"
    assert_env VAJRA_CI_CUDA_VERSION
    assert_env VAJRA_CI_TORCH_VERSION

    CUDA_MAJOR="${VAJRA_CI_CUDA_VERSION%.*}"
    CUDA_MINOR="${VAJRA_CI_CUDA_VERSION#*.}"

    VLLM_DEFAULT_VERSION="0.6.1.post1"
    VLLM_DEFAULT_CUDA="118"
    PYTHON_V="310"

    echo "Checking vLLM for desired CUDA $VAJRA_CI_CUDA_VERSION compatibility..."

    # Fetch PyPI metadata for latest version
    metadata=$(curl -s "https://pypi.org/pypi/vllm/json")
    # get latest vllm version
    latest_version=$(echo "$metadata" | python -c 'import sys, json; print(json.load(sys.stdin)["info"]["version"])' 2>/dev/null)
    echo "Latest vLLM version available on PyPI: $latest_version"

    # Check if wheel exists with desired CUDA version
    wheel_url="https://github.com/vllm-project/vllm/releases/download/v${latest_version}/vllm-${latest_version}+cu${CUDA_MAJOR}${CUDA_MINOR}-cp${PYTHON_V}-cp${PYTHON_V}-manylinux1_x86_64.whl"
    echo "Checking for wheel at: $wheel_url"
    if curl -s -I "$wheel_url" | grep -q "200 OK"; then
        echo "Found vLLM wheel for version $latest_version with CUDA $VAJRA_CI_CUDA_VERSION."
       echo "Installing vLLM $latest_version with CUDA $VAJRA_CI_CUDA_VERSION..."
        pip install "$wheel_url" --extra-index-url "https://download.pytorch.org/whl/cu${CUDA_MAJOR}${CUDA_MINOR}" || {
            echo "Failed to install vLLM $latest_version+$VAJRA_CI_CUDA_VERSION."
            exit 1
        }
    echo "Successfully installed vLLM $latest_version with CUDA $VAJRA_CI_CUDA_VERSION."
    VLLM_VERSION=$latest_version
    VLLM_CUDA_VERSION=$VAJRA_CI_CUDA_VERSION
    else
        echo "No wheel found for vLLM $latest_version with CUDA $VAJRA_CI_CUDA_VERSION."
        echo "Falling back to default: vLLM $VLLM_DEFAULT_VERSION with CUDA $VLLM_DEFAULT_CUDA"
        default_wheel_url="https://github.com/vllm-project/vllm/releases/download/v${VLLM_DEFAULT_VERSION}/vllm-${VLLM_DEFAULT_VERSION}+cu${VLLM_DEFAULT_CUDA}-cp${PYTHON_V}-cp${PYTHON_V}-manylinux1_x86_64.whl"
        echo "Checking fallback wheel at: $default_wheel_url"
        pip install "$default_wheel_url" --extra-index-url "https://download.pytorch.org/whl/cu$VLLM_DEFAULT_CUDA" || {
            echo "Failed to install fallback vLLM $VLLM_DEFAULT_VERSION+$VLLM_DEFAULT_CUDA."
            exit 1
        }
        echo "Successfully installed fallback vLLM $VLLM_DEFAULT_VERSION with CUDA $VLLM_DEFAULT_CUDA."
        VLLM_VERSION=$VLLM_DEFAULT_VERSION
        VLLM_CUDA_VERSION=$VLLM_DEFAULT_CUDA
    fi
    echo "VLLM_VERSION=$VLLM_VERSION" >> /VERSIONS.txt.txt
    echo "VLLM_CUDA_VERSION=$VLLM_CUDA_VERSION" >> /VERSIONS.txt.txt
    echo "::endgroup::"
    popd
}

function install_sglang() {
    pushd "$_sgl_dir"
    echo "::group::Build sglang"
    assert_env VAJRA_CI_CUDA_VERSION
    assert_env VAJRA_CI_TORCH_VERSION

    CUDA_MAJOR="${VAJRA_CI_CUDA_VERSION%.*}"
    CUDA_MINOR="${VAJRA_CI_CUDA_VERSION#*.}"

    SGLANG_DEFAULT_VERSION="0.4.3.post4"
    SGLANG_DEFAULT_CUDA="124"
    SGLANG_DEFAULT_TORCH="2.5"

    echo "SGLang wheel name does not include CUDA or PyTorch info."
    echo "Attempting to install SGLang with desired CUDA $VAJRA_CI_CUDA_VERSION and PyTorch $VAJRA_CI_TORCH_VERSION..."
    echo "Using flashinfer wheel index: https://flashinfer.ai/whl/cu${CUDA_MAJOR}${CUDA_MINOR}/torch${VAJRA_CI_TORCH_VERSION}/flashinfer-python"
    if pip install "sglang[all]==$SGLANG_DEFAULT_VERSION" --find-links "https://flashinfer.ai/whl/cu${CUDA_MAJOR}${CUDA_MINOR}/torch${VAJRA_CI_TORCH_VERSION}/flashinfer-python" 2>/dev/null; then
        echo "Successfully installed SGLang $SGLANG_DEFAULT_VERSION with desired CUDA $VAJRA_CI_CUDA_VERSION and PyTorch $VAJRA_CI_TORCH_VERSION."
        SGL_VERSION=$SGLANG_DEFAULT_VERSION
        SGL_CUDA_VERSION=$VAJRA_CI_CUDA_VERSION
        SGL_TORCH_VERSION=$VAJRA_CI_TORCH_VERSION
    else
        echo "Failed to install SGLang with desired CUDA $VAJRA_CI_CUDA_VERSION and PyTorch $VAJRA_CI_TORCH_VERSION."
        echo "Falling back to default: SGLang $SGLANG_DEFAULT_VERSION with CUDA $SGLANG_DEFAULT_CUDA and PyTorch $SGLANG_DEFAULT_TORCH..."
        echo "Using fallback flashinfer wheel index: https://flashinfer.ai/whl/cu$SGLANG_DEFAULT_CUDA/torch${SGLANG_DEFAULT_TORCH}/flashinfer-python"
        pip install "sglang[all]==$SGLANG_DEFAULT_VERSION" --find-links "https://flashinfer.ai/whl/cu$SGLANG_DEFAULT_CUDA/torch${SGLANG_DEFAULT_TORCH}/flashinfer-python" || {
            echo "Failed to install fallback SGLang $SGLANG_DEFAULT_VERSION with CUDA $SGLANG_DEFAULT_CUDA and PyTorch $SGLANG_DEFAULT_TORCH."
            exit 1
        }
        echo "Successfully installed fallback SGLang $SGLANG_DEFAULT_VERSION with CUDA $SGLANG_DEFAULT_CUDA and PyTorch $SGLANG_DEFAULT_TORCH."
        SGL_VERSION=$SGLANG_DEFAULT_VERSION
        SGL_CUDA_VERSION=$SGLANG_DEFAULT_CUDA
        SGL_TORCH_VERSION=$SGLANG_DEFAULT_TORCH
    fi
    echo "SGL_VERSION=$SGL_VERSION" >> /VERSIONS.txt.txt
    echo "SGL_CUDA_VERSION=$SGL_CUDA_VERSION" >> /VERSIONS.txt.txt
    echo "SGL_TORCH_VERSION=$SGL_TORCH_VERSION" >> /VERSIONS.txt.txt
}

function install_mlc() {
    pushd "$_mlc_dir"
    echo "::group::Build mlc"
    assert_env VAJRA_CI_CUDA_VERSION
    assert_env VAJRA_CI_TORCH_VERSION

    CUDA_MAJOR="${VAJRA_CI_CUDA_VERSION%.*}"
    CUDA_MINOR="${VAJRA_CI_CUDA_VERSION#*.}"

    MLC_DEFAULT_VERSION="nightly"
    MLC_DEFAULT_CUDA="123"

    echo "Checking MLC for desired CUDA $VAJRA_CI_CUDA_VERSION compatibility..."
    wheels_url="https://mlc.ai/wheels"
    echo "Fetching wheel index from: $wheels_url"
    if curl -s "$wheels_url" | grep -q "mlc-llm-${MLC_DEFAULT_VERSION}-cu${CUDA_MAJOR}${CUDA_MINOR}"; then
        echo "Found MLC wheel for version $MLC_DEFAULT_VERSION for CUDA $VAJRA_CI_CUDA_VERSION."
        echo "Installing MLC $MLC_DEFAULT_VERSION for CUDA $VAJRA_CI_CUDA_VERSION..."
        pip install --pre -U -f "$wheels_url" "mlc-llm-${MLC_DEFAULT_VERSION}-cu${CUDA_MAJOR}${CUDA_MINOR}" "mlc-ai-${MLC_DEFAULT_VERSION}-cu${CUDA_MAJOR}${CUDA_MINOR}" || {
            echo "Failed to install MLC $MLC_DEFAULT_VERSION+$VAJRA_CI_CUDA_VERSION."
            exit 1
        }
        echo "Successfully installed MLC $MLC_DEFAULT_VERSION for CUDA $VAJRA_CI_CUDA_VERSION."
        MLC_VERSION=$MLC_DEFAULT_VERSION
        MLC_CUDA_VERSION=$VAJRA_CI_CUDA_VERSION
    else
        echo "No MLC wheel found for version $MLC_DEFAULT_VERSION for CUDA $VAJRA_CI_CUDA_VERSION in index."
        echo "Falling back to default: MLC $MLC_DEFAULT_VERSION for CUDA $MLC_DEFAULT_CUDA"
        pip install --pre -U -f "$wheels_url" "mlc-llm-${MLC_DEFAULT_VERSION}-cu${MLC_DEFAULT_CUDA}" "mlc-ai-${MLC_DEFAULT_VERSION}-cu${MLC_DEFAULT_CUDA}" || {
            echo "Failed to install fallback MLC $MLC_DEFAULT_VERSION+$MLC_DEFAULT_CUDA."
            exit 1
        }
        echo "Successfully installed fallback MLC $MLC_DEFAULT_VERSION for CUDA $MLC_DEFAULT_CUDA."
        MLC_VERSION=$MLC_DEFAULT_VERSION
        MLC_CUDA_VERSION=$MLC_DEFAULT_CUDA
    fi
    echo "MLC_VERSION=$MLC_VERSION" >> /VERSIONS.txt.txt
    echo "MLC_CUDA_VERSION=$MLC_CUDA_VERSION" >> /VERSIONS.txt.txt
    echo "::endgroup::"
    popd
}

function install_git_lfs() {
  # MLC-LLM requires git-lfs to download models
  curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
  apt-get update
  apt-get install git-lfs
  git lfs install
}