#!/bin/bash
#Install dependencies
sudo apt install python3 python3-pip nginx

#Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate

# Make the startup file executable by the owner
sudo chmod 744 /var/flaskapp/simpleapp/start.sh

#Supervisor to start and control the server
sudo apt-get install supervisor -y

sudo chown -R www-data:www-data $PWD

# Replace variables
sudo sed 's/VAR1/${PWD}/g' ./deployment_files/app.conf

# Copy file over
sudo cp ./deployment_files/app.conf /etc/supervisor/conf.d/

sudo systemctl restart supervisor.service

# Setup nginx

sudo rm /etc/nginx/sites-enabled/default

sudo cp ./deployment_files/app /etc/nginx/sites-available/

sudo ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled

sudo nginx -t

sudo nginx -s reload

sudo systemctl restart nginx