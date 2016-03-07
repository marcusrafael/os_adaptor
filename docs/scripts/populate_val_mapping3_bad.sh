# #!/bin/sh

# ## Nova

# # Compute --> Resource type VM
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 68, "apf_value": 84}' \
#     http://localhost:8001/value_mapping/

# # Create -> Create
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 70, "apf_value": 18}' \
#     http://localhost:8001/value_mapping/

# Create -> VM
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 70, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# # Get -> Read 
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 71, "apf_value": 19}' \
#     http://localhost:8001/value_mapping/

# Get -> VM
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 71, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# # Update -> Update
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 72, "apf_value": 22}' \
#     http://localhost:8001/value_mapping/

# Update -> VM
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 72, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# # Delete -> Delete
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 73, "apf_value": 21}' \
#     http://localhost:8001/value_mapping/

# Delete -> VM
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 73, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# # Start -> Start
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 74, "apf_value": 27}' \
#     http://localhost:8001/value_mapping/

# Start -> VM

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 74, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# # Stop
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 75, "apf_value": 28}' \
#     http://localhost:8001/value_mapping/

# Stop -> VM

curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 75, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# # Attach Interface -> Add
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 77, "apf_value": 29}' \
#     http://localhost:8001/value_mapping/

# Attach Interface -> VM
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 77, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# Attach Interface -> Parameter VNIF
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 77, "apf_value": 89}' \
#     http://localhost:8001/value_mapping/

# # Detach Interface -> Remove
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 78, "apf_value": 30}' \
#     http://localhost:8001/value_mapping/

# Detach Interface -> VM
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 78, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# # Detach Interface -> Parameter VNIF
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 78, "apf_value": 89}' \
#     http://localhost:8001/value_mapping/

# # Attach Volume -> Add
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 79, "apf_value": 29}' \
#     http://localhost:8001/value_mapping/

# Attach Volume -> VM
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 79, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# Attach Volume -> Parameter VHD
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 79, "apf_value": 90}' \
#     http://localhost:8001/value_mapping/

# # Detach Volume -> Remove
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 80, "apf_value": 30}' \
#     http://localhost:8001/value_mapping/

# Detach Volume -> VM
curl -v -X POST -H "Content-Type: application/json" \
    -d '{"local_value": 80, "apf_value": 84}' \
    http://localhost:8001/value_mapping/

# Detach Volume -> Parameter VHD
# curl -v -X POST -H "Content-Type: application/json" \
#     -d '{"local_value": 80, "apf_value": 90}' \
#     http://localhost:8001/value_mapping/

