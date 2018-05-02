#!/usr/bin/env bash

substitute_template() {
    local target="$1"
    if [[ ! -r "${target}.template" ]]; then
      echo "Can not find"
      return 1;
    fi
    eval "echo \"$(< ${target}.template)\"" > "$target"
}

template_render() {
    for target in "$@"; do
        substitute_template "$target"
    done
}
