default:
    just --list

# ENV = {doc}
up ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/{{ENV}}/compose.yml up --detach
    else
        echo "{{ENV}}: Accepted values are: 'doc'." >&2
    fi

# ENV = {doc}
down ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/{{ENV}}/compose.yml down
    else
        echo "{{ENV}}: Accepted values are: 'doc'." >&2
    fi

# ENV = {doc}
logs ENV:
    #!/bin/bash
    if [ "{{ENV}}" = "doc" ]; then
        docker compose -f docker/{{ENV}}/compose.yml logs --follow
    else
        echo "{{ENV}}: Accepted values are: 'doc'." >&2
    fi
