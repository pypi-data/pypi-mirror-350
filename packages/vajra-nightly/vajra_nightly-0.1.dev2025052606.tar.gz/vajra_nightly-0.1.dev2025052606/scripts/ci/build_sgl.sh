#!/bin/bash
set -ex

_script_dir="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd )"
source "${_script_dir}/utils.sh"

init_conda
clone_sgl
create_sgl_conda_env
activate_sgl_conda_env
install_sglang