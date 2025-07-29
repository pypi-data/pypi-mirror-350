#!/bin/bash
set -ex

_script_dir="$( cd -- "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd )"
source "${_script_dir}/utils.sh"

bash "${_script_dir}/setup/install_base.sh"
bash "${_script_dir}/setup/install_mamba.sh"

init_conda
create_vajra_conda_env
activate_vajra_conda_env
