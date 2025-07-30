#! /usr/bin/env bash

function bluer_sandbox_arvancloud_ssh() {
    local options=$1
    local do_dryrun=$(bluer_ai_option_int "$options" dryrun 0)
    local do_seed=$(bluer_ai_option_int "$options" seed 1)

    local pem_filename="$HOME/.ssh/$ARVANCLOUD_PRIVATE_KEY.pem"
    if [[ ! -f "$pem_filename" ]]; then
        bluer_ai_log_error "$pem_filename not found."
        return 1
    fi

    chmod 400 $pem_filename

    bluer_ai_badge "🌀"

    if [[ "$do_seed" == 1 ]]; then
        bluer_ai_seed arvancloud clipboard
        [[ $? -ne 0 ]] && return 1
    fi

    bluer_ai_eval dryrun=$do_dryrun \
        ssh \
        -i $pem_filename \
        ubuntu@$ARVANCLOUD_IP
}
