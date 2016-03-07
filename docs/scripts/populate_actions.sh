#!/bin/sh

# Ontology

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "list", "description": "action list"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "create", "description": "action create"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "read", "description": "action read"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "write", "description": "action write"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "delete", "description": "action delete"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "update", "description": "action update"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "append", "description": "action append"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "replace", "description": "action replace"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "resume", "description": "action resume"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "suspend", "description": "action suspend"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "start", "description": "action start"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "stop", "description": "action stop"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "add", "description": "action add"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 6, "name": "remove", "description": "action remove"}' \
    http://localhost:8001/value/

# Openstack

# Service

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "get_service", "description": "action=get; resource=service"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "list_service", "description": "action=list; resource=service"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "create_service", "description": "action=create; resource=service"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "update_service", "description": "action=update; resource=service"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "delete_service", "description": "action=delete; resource=service"}' \
    http://localhost:8001/value/

# User

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "get_user", "description": "action=get; resource=user"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "list_users", "description": "action=list; resource=user"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "create_user", "description": "action=create; resource=user"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "update_user", "description": "action=update; resource=user"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "delete_user", "description": "action=delete; resource=user"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "change_password", "description": "action=update; resource=user; param=password"}' \
    http://localhost:8001/value/

# Group

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "get_group", "description": "action=get; resource=group"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "list_groups", "description": "action=list; resource=group"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "create_group", "description": "action=create; resource=group"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "update_group", "description": "action=update; resource=group"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "delete_group", "description": "action=delete; resource=group"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "list_users_in_group", "description": "action=read; resource=group; param=user_list"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "remove_user_from_group", "description": "action=remove; resource=group; param=user"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "check_user_in_group", "description": "action=read; resource=group; param=user"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "add_user_to_group", "description": "action=add; resource=group; param=user"}' \
    http://localhost:8001/value/

# Role

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "get_role", "description": "action=get; resource=role"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "list_role", "description": "action=list; resource=role"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "create_role", "description": "action=create; resource=role"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "update_role", "description": "action=update; resource=role"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "delete_role", "description": "action=delete; resource=role"}' \
    http://localhost:8001/value/


