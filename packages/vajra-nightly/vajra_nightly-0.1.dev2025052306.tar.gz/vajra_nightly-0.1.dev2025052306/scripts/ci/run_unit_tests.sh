#!/bin/bash
set -ex

_script_dir="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd )"
source "${_script_dir}/utils.sh"

init_conda
activate_vajra_conda_env
login_huggingface

# Run Python unit tests
echo "::group::Run python unit tests"
make test/pyunit
echo "::endgroup::"

# Run Python integration tests
echo "::group::Run python integration tests"
make test/pyintegration
echo "::endgroup::"

# Run C++ unit tests
echo "::group::Run C++ unit tests"
make test/ctest BUILD_TYPE=Release
echo "::endgroup::"
