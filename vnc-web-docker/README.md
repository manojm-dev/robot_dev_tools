# Virual Display with VNC 

This repository provides Docker Compose configurations for setting up a virtual display using NoVNC and integrating it with target services. 

## Image Used

Original docker image build: `theasp/novnc:latest`
* the original project docker image but only works in amd64

Forked docker image build by myself: `manojm003/novnc:latest`
* the latest tag uses port 8080
* use tag 8081 which uses port 8081 in case you need another seperate display for another docker container

## Methods

### 1) Type one

Shares the network stack with the NoVNC service (network_mode: service:novnc). This means it uses the same IP address and networking context as the NoVNC service, facilitating direct communication.

### 2) Type two 

Connected to the x11 network, which ensures that it has its own IP address and can communicate with the NoVNC service over the defined network.


### 3) Type Three

This method is used when the target service has requirement to only be in host mode so this startup script starts `vnc_container` and retrieves its **IP Address**, and then starts the target service with `DISPLAY=VNC_CONTAINER_IP:0.0` which does the job done.
