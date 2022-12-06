#!/bin/bash
#Install dependencies
sudo apt install python3 python3-pip nginx

#Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
deactivate