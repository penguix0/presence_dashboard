#!/bin/bash
#Install dependencies
sudo apt install python3 python3-pip nginx

#Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate

#Supervisor to start and control the server
sudo apt-get install supervisor -y

sudo chown -R www-data:www-data $PWD


# Replace variables
sudo sed 's/VAR1/$PWD/g' ./deployment_files/app.conf

# Copy file over
sudo cp ./deployment_files/app.conf /etc/supervisor/conf.d/

sudo systemctl restart supervisor.service