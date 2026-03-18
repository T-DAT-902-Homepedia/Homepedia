default:
    just --list

up ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f documentation/compose.yml up --detach
    else
        echo "{{ENV}}: Accepted values are: 'doc'." >&2
    fi

down ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f documentation/compose.yml down --volumes
    else
        echo "{{ENV}}: Accepted values are: 'doc'." >&2
    fi

logs ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f documentation/compose.yml logs --follow
    else
        echo "{{ENV}}: Accepted values are: 'doc'." >&2
    fi


