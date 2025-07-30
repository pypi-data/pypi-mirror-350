#! /usr/bin/env bash

# internal function to bluer_ai_seed.
function bluer_ai_seed_arvancloud() {
    # seed is NOT local

    bluer_ai_seed add_ssh_key

    bluer_ai_seed add_bluer_ai

    seed="${seed}sudo apt-get update$delim"
    seed="${seed}sudo apt install -y python3-pip$delim"
    seed="${seed}sudo apt install -y python3-venv$delim"
    seed="${seed}sudo apt install -y libgl1$delim_section"

    seed="${seed}python3 -m venv \$HOME/venv/bluer_ai$delim"
    seed="${seed}source \$HOME/venv/bluer_ai/bin/activate$delim_section"

    seed="${seed}pip install --upgrade pip --no-input$delim"
    seed="${seed}pip3 install setuptools$delim"
    seed="${seed}pip3 install -e .$delim"
    seed="${seed}pip3 install bluer_objects[opencv]$delim"
    seed="${seed}pip3 install --upgrade opencv-python-headless$delim_section"

    bluer_ai_env_dot_seed $(python3 -m bluer_objects locate)
    [[ $? -ne 0 ]] && return 1

    seed="${seed}source ./bluer_ai/.abcli/bluer_ai.sh$delim_section"
}

function bluer_sandbox_arvancloud_seed() {
    bluer_ai_seed arvancloud "$@"
}
