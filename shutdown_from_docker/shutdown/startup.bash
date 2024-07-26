#!/bin/bash

echo "1" > /home/username/.startup/shutdown/status.txt

if [ $? -eq 0 ]; then
    python3 /home/username/.startup/shutdown/shutdown.py
else
    echo "Shudown function failed."
fi