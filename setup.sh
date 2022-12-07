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

sudo nano /etc/supervisor/conf.d/simpleapp.conf

sudo systemctl restart supervisor.service