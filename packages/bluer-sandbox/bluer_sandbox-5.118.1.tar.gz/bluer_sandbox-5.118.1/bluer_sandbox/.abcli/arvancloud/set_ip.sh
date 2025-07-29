#! /usr/bin/env bash

function bluer_sandbox_arvancloud_set_ip() {
    local ip=$1
    if [[ -z "$ip" ]]; then
        bluer_ai_log_error "ip not found."
        return 1
    fi

    export ARVANCLOUD_IP=$ip

    pushd $abcli_path_git/bluer-sandbox >/dev/null
    dotenv set ARVANCLOUD_IP $ip
    popd >/dev/null

}
