# Shutdown from docker

## Requirements

- Make shutdown cmd from host user to ask no password

- Steps to do it
```
sudo visudo

# add this line
usename ALL=(ALL) NOPASSWD: /sbin/shutdown

```

## Python script

- Reads file `status.txt`

- If it is 0 then shutdown if 1 do nothing

- The logs are stored in `logfile.txt`

## Launch script

- Sets the `status.txt` as 1

- Launches the python script

## Create a systemd script to execute the launch script

- Move the service file to the systemd services folder

- Then enable the serice to automatically run at startup

- If want to test the function imidiately then start the serice and write 0 inside `status.txt`

```
# copying
cp shutdown-via-docker.service /etc/systemd/system/

# enabling the service
sudo systemctl enable shutdown-via-docker.service

# starting the service
sudo systemctl start shutdown-via-docker.service

# to checking the status of service
sudo systemctl status shutdown-via-docker.service

# to write 0 inside `status.txt`
echo "0" > status.txt

```
