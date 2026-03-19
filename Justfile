default:
    just --list

# ENV = {doc | dev | prod}
up ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f documentation/compose.yml up --detach
    elif [ "{{ENV}}" = "dev" ]; then
        docker compose -f compose.dev.yml up --detach
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml up --detach --build
    else
        echo "{{ENV}}: Accepted values are: 'doc|dev|prod'." >&2
    fi

# ENV = {doc | dev | prod}
down ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f documentation/compose.yml down --volumes
    elif [ "{{ENV}}" = "dev" ]; then
        docker compose -f compose.dev.yml down
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml down
    else
        echo "{{ENV}}: Accepted values are: 'doc|dev|prod'." >&2
    fi

# ENV = {doc | dev | prod}
logs ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f documentation/compose.yml logs --follow
    elif [ "{{ENV}}" = "dev" ]; then
        docker compose -f compose.dev.yml logs --follow
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml logs --follow
    else
        echo "{{ENV}}: Accepted values are: 'doc|dev|prod'." >&2
    fi
