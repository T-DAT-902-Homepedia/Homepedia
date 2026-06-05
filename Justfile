default:
    just --list

# ENV = {doc | data | dev | prod}
up ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/{{ENV}}/compose.yml up --detach
    elif [ "{{ENV}}" = "dev" ]; then
        docker compose -f compose.dev.yml up --detach
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml up --detach --build
    elif [ "{{ENV}}" = "data" ]; then
        docker compose -f docker/{{ENV}}/compose.yml up --detach
    else
        echo "{{ENV}}: Accepted values are: 'doc|data|dev|prod'." >&2
    fi

# ENV = {doc | data | dev | prod}
down ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/doc/compose.yml up --detach
    elif [ "{{ENV}}" = "dev" ]; then
        docker compose -f compose.dev.yml down
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml down
    elif [ "{{ENV}}" = "data" ]; then
        docker compose -f docker/{{ENV}}/compose.yml down
    else
        echo "{{ENV}}: Accepted values are: 'doc|data|dev|prod'." >&2
    fi

# ENV = {doc | data | dev | prod}
logs ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/{{ENV}}/compose.yml logs --follow
    elif [ "{{ENV}}" = "dev" ]; then
        docker compose -f compose.dev.yml logs --follow
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml logs --follow
    elif [ "{{ENV}}" = "data" ]; then
        docker compose -f docker/{{ENV}}/compose.yml logs --follow
    else
        echo "{{ENV}}: Accepted values are: 'doc|data|dev|prod'." >&2
    fi


