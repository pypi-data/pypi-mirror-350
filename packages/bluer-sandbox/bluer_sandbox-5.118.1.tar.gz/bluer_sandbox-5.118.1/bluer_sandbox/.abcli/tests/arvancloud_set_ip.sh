#! /usr/bin/env bash

function test_bluer_sandbox_arvancloud_set_ip() {
    local options=$1

    bluer_ai_eval ,$options \
        bluer_sandbox_arvancloud_set_ip
    [[ $? -eq 0 ]] && return 1

    bluer_ai_eval ,$options \
        bluer_sandbox_arvancloud_set_ip 1.2.3.4
}
