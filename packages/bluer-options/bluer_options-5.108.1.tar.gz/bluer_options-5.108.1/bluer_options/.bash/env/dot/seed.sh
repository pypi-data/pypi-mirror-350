#! /usr/bin/env bash

# internal function for bluer_ai_seed.
function bluer_ai_env_dot_seed() {
    # seed is NOT local

    local path=$1

    if [[ ! -d "$path" ]]; then
        bluer_ai_log_error "$path not found."
        return 1
    fi

    pushd $path >/dev/null
    local line
    for line in $(dotenv \
        --file .env \
        list \
        --format shell); do

        seed="${seed}export $line$delim"
    done
    popd >/dev/null

    seed="$seed$delim"
}
