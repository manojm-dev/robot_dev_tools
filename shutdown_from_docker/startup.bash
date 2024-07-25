cd /home/${USER}/.startup/shutdown

echo "1" > status.txt

if [ $? -eq 0 ]; then
    python3 shutdown.py
else
    echo "Shudown function failed."
fi