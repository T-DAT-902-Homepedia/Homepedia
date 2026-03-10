default:
    just --list

up ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/doc/compose.yml up --detach
    else
        echo "{{ENV}}: Accepted values are: 'doc'." >&2
    fi

down ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/doc/compose.yml down
    else
        echo "{{ENV}}: Accepted values are: 'doc'." >&2
    fi

logs ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/{{ENV}}/compose.yml logs --follow
    else
        echo "{{ENV}}: Accepted values are: 'doc'." >&2
    fi


