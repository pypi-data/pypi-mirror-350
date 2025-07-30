#! /usr/bin/env bash

function test_bluer_sandbox_seed_arvancloud() {
    local options=$1

    bluer_ai_seed arvancloud screen
    [[ $? -ne 0 ]] && return 1

    bluer_sandbox_arvancloud seed screen
}
