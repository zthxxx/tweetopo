#!/usr/bin/env bash

SUFFIX=${SUFFIX:=template}

compile() {
eval "cat <<-EOF
$(< "${1}.${SUFFIX}")
EOF" > "${1}"
}

substitute_template() {
    local target="$1"
    if [[ ! -r "${target}.${SUFFIX}" ]]; then
      echo "Can not find template: ${target}.${SUFFIX}"
      return 1;
    fi

    compile "${target}"
}

template_render() {
    for target in "$@"; do
        substitute_template "$target"
    done
}
