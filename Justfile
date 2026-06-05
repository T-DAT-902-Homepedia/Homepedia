default:
    just --list

# --- App unifiée (infra + API + webapp dev + pipeline) ----------------------

_app := "docker compose -f compose.app.yml --env-file .env.data"

# Démarre infra + API + webapp (dev). Le pipeline n'est PAS lancé.
app-up:
    UID=$(id -u) GID=$(id -g) {{_app}} up -d --build

# Arrête toute l'app.
app-down:
    {{_app}} down

# Logs de toute l'app.
app-logs:
    {{_app}} logs -f

# Lance le pipeline Kedro une fois (peuple MinIO + PostGIS) puis sort.
pipeline:
    UID=$(id -u) GID=$(id -g) {{_app}} --profile pipeline run --rm pipeline

# Lance un sous-ensemble du pipeline. Ex : just pipeline-only geo
pipeline-only PIPE:
    UID=$(id -u) GID=$(id -g) {{_app}} --profile pipeline run --rm pipeline run --pipeline={{PIPE}}

# --- Recettes legacy (webapp seule) -----------------------------------------

# ENV = {doc | dev | prod}
up ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/{{ENV}}/compose.yml up --detach
    elif [ "{{ENV}}" = "dev" ]; then
        UID=$(id -u) GID=$(id -g) docker compose -f compose.dev.yml up --detach --build
    elif [ "{{ENV}}" = "prod" ]; then
        docker compose -f compose.prod.yml up --detach --build
    else
        echo "{{ENV}}: Accepted values are: 'doc|dev|prod'." >&2
    fi

# ENV = {doc | dev | prod}
down ENV:
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

# ENV = {doc | dev | prod}
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

shell ENV:
    docker compose -f compose.{{ENV}}.yml exec -it webapp sh


