#!/bin/sh

## Role

# Get Service
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 51, "apf_value": 19}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 51, "apf_value": 59}' \
    http://localhost:8001/value_mapping/

# List Services
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 52, "apf_value": 17}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 52, "apf_value": 59}' \
    http://localhost:8001/value_mapping/

# Create Services
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 53, "apf_value": 18}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 53, "apf_value": 59}' \
    http://localhost:8001/value_mapping/

# Update Services
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 54, "apf_value": 22}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 54, "apf_value": 59}' \
    http://localhost:8001/value_mapping/

# Delete Services
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 55, "apf_value": 21}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 55, "apf_value": 59}' \
    http://localhost:8001/value_mapping/
