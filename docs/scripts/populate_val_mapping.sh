#!/bin/sh

## Service

# Get Service
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 31, "apf_value": 19}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 31, "apf_value": 56}' \
    http://localhost:8001/value_mapping/

# List Services
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 32, "apf_value": 17}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 32, "apf_value": 56}' \
    http://localhost:8001/value_mapping/

# Create Services
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 33, "apf_value": 18}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 33, "apf_value": 56}' \
    http://localhost:8001/value_mapping/

# Update Services
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 34, "apf_value": 22}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 34, "apf_value": 56}' \
    http://localhost:8001/value_mapping/

# Delete Services
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 35, "apf_value": 21}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 35, "apf_value": 56}' \
    http://localhost:8001/value_mapping/

## User

# Get
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 36, "apf_value": 19}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 36, "apf_value": 57}' \
    http://localhost:8001/value_mapping/

# List
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 37, "apf_value": 17}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 37, "apf_value": 57}' \
    http://localhost:8001/value_mapping/

# Create
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 38, "apf_value": 18}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 38, "apf_value": 57}' \
    http://localhost:8001/value_mapping/

# Update
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 39, "apf_value": 22}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 39, "apf_value": 57}' \
    http://localhost:8001/value_mapping/

# Delete
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 40, "apf_value": 21}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 40, "apf_value": 57}' \
    http://localhost:8001/value_mapping/

# Change Password
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 41, "apf_value": 22}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 41, "apf_value": 57}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 41, "apf_value": 60}' \
    http://localhost:8001/value_mapping/

## Group

# Get
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 42, "apf_value": 19}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 42, "apf_value": 58}' \
    http://localhost:8001/value_mapping/

# List
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 43, "apf_value": 17}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 43, "apf_value": 58}' \
    http://localhost:8001/value_mapping/

# Create
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 44, "apf_value": 18}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 44, "apf_value": 58}' \
    http://localhost:8001/value_mapping/

# Update
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 45, "apf_value": 22}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 45, "apf_value": 58}' \
    http://localhost:8001/value_mapping/

# Delete
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 46, "apf_value": 21}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 46, "apf_value": 58}' \
    http://localhost:8001/value_mapping/

# List Users in Group
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 47, "apf_value": 19}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 47, "apf_value": 58}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 47, "apf_value": 61}' \
    http://localhost:8001/value_mapping/

# Remove User from Group
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 48, "apf_value": 30}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 48, "apf_value": 58}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 48, "apf_value": 62}' \
    http://localhost:8001/value_mapping/

# Check User in Group
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 49, "apf_value": 19}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 49, "apf_value": 58}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 49, "apf_value": 62}' \
    http://localhost:8001/value_mapping/

# Add User to Group
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 50, "apf_value": 29}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 50, "apf_value": 58}' \
    http://localhost:8001/value_mapping/

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 50, "apf_value": 62}' \
    http://localhost:8001/value_mapping/
