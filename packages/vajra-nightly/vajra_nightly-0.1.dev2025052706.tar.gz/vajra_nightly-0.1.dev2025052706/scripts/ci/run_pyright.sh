#!/bin/bash
set -ex

_script_dir="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd )"
source "${_script_dir}/utils.sh"

init_conda
activate_vajra_conda_env

# Run Python unit tests
echo "::group::Run pyright"
make lint/pyright
echo "::endgroup::"
