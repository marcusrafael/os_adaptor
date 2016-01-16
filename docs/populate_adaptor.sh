#!/bin/sh
#curl -v -X POST -H "Content-Type: application/json" \
#    -d '{"attribute": 6, "name": "list", "description": "action list"}' \
#    http://localhost:8001/value/

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








curl -v -X POST -H "Content-Type: application/json" \
    -d '{               \
    "tenant": null,     \
    "apf": null,        \
    "ontology": false,  \
    "name": "action",   \
    "description": "create"   \
    }'                  \
    http://localhost:8001/attribute/



curl -v -X POST -H "Content-Type: application/json" \
    -d '{               \
    "tenant": null,     \
    "apf": null,        \
    "ontology": false,  \
    "name": "action",   \
    "description": "get_service"   \
    }'                  \
    http://localhost:8001/attribute/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{               \
    "tenant": null,     \
    "apf": null,        \
    "ontology": false,  \
    "name": "action",   \
    "description": "get_service"   \
    }'                  \
    http://localhost:8001/attribute/
