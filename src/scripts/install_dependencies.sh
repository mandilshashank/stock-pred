#!/bin/bash

# Update package lists
sudo apt-get update

# Install Python and pip
sudo apt-get install -y python3 python3-pip

# Install required Python packages
pip3 install -r requirements.txt

# Install MySQL client
sudo apt-get install -y mysql-client