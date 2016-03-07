#!/bin/sh

# Openstack

# bundle instance / create network
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "create", "description": "action=create"}' \
    http://localhost:8001/value/

# describe instances
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "get", "description": "action=get"}' \
    http://localhost:8001/value/

# modify instance attribute
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "update", "description": "action=update"}' \
    http://localhost:8001/value/

# terminate instance
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "delete", "description": "action=delete"}' \
    http://localhost:8001/value/

# start instance
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "start", "description": "action=start"}' \
    http://localhost:8001/value/

# stop instance
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "stop", "description": "action=stop"}' \
    http://localhost:8001/value/

# reboot instance
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "reboot", "description": "action=reboot"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "attach_interface", "description": "action=attach_interface"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "detach_interface", "description": "action=detach_interface"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "attach_volume", "description": "action=attach_interface"}' \
    http://localhost:8001/value/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "detach_volume", "description": "action=detach_interface"}' \
    http://localhost:8001/value/

# Describe snapshot
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "snapshot", "description": "action=snapshot"}' \
    http://localhost:8001/value/

# Create snapshot
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "volume_snapshot_create", "description": "action=volume_snapshot_create"}' \
    http://localhost:8001/value/

# Delete snapshot
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"attribute": 5, "name": "volume_snapshot_delete", "description": "action=volume_snapshot_delete"}' \
    http://localhost:8001/value/

