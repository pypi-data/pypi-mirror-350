#!/bin/bash

# Check if the Bluetooth service is active
if ! systemctl is-active --quiet bluetooth; then
    echo "Bluetooth service is not active. Resetting..."
    sudo systemctl restart bluetooth
    sleep 5
fi

# Block/Unblock Bluetooth
sudo rfkill block bluetooth
sleep 2
sudo rfkill unblock bluetooth
sleep 2

# Restart Bluetooth
sudo systemctl stop bluetooth.service
sleep 2
sudo systemctl start bluetooth.service
sleep 2