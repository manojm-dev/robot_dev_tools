#!/bin/bash
 
# stop previosly started vnc service
docker compose --file vnc.yaml down
    
echo "Previous Docker Compose services stopped successfully."

# Start VNC display server
docker compose --file vnc.yaml up -d > /dev/null 2>&1 &

# Wait for the container to start
sleep 5

# Get the IP address of the VNC container
vnc_ip=$(docker inspect --format '{{ .NetworkSettings.Networks.x11.IPAddress }}' vnc_container)
export VNC_CONTAINER_IP="${vnc_ip}:0.0"
echo "The VNC Display server container started with IPAddress: $VNC_CONTAINER_IP"

# Export the variable and start the target compose file
docker compose --file target.yaml up -d > /dev/null 2>&1 &
echo "Starting the target compose file"
