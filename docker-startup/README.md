# Start Docker at reboot

## Docker Compose

- A script inside the image should be pointed as entrypoint in the compose file
```
entrypoint: ./ros_entrypoint.sh
```

## Entrypoint Script

- The entrypoint script should contain shebang `#!/bin/bash`

- When using mutiple long running scripts or process inside the script add `&` to send that process to background

- At last you should add `sleep infinity` command in the script as all the script/process is pushed back to backgroud and considered as exited the entrypoint script exist with a 0 which inturn stops the container

## Adding Systemd Service 

- Copy this file to systemd services path and enable the service

```
# copying
cp start-robot-compose.service /etc/systemd/system/

# enabling the service
sudo systemctl enable start-robot-compose.service

# starting the service
sudo systemctl start start-robot-compose.service

# to checking the status of service
sudo systemctl status start-robot-compose.service
```
