default:
    just --list

up ENV: # doc | dev | prod
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/{{ENV}}/compose.yml up --detach
    elif [ "{{ENV}}" = "dev" ]; then
        docker compose -f compose.dev.yml up --detach
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml up --detach --build
    else
        echo "{{ENV}}: Accepted values are: 'doc|dev|prod'." >&2
    fi

down ENV: # doc | dev | prod
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/doc/compose.yml up --detach
    elif [ "{{ENV}}" = "dev" ]; then
        docker compose -f compose.dev.yml down
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml down
    else
        echo "{{ENV}}: Accepted values are: 'doc|dev|prod'." >&2
    fi

logs ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/{{ENV}}/compose.yml logs --follow
    elif [ "{{ENV}}" = "dev" ]; then
        docker compose -f compose.dev.yml logs --follow
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml logs --follow
    else
        echo "{{ENV}}: Accepted values are: 'doc|dev|prod'." >&2
    fi


