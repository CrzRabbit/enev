<<<<<<< HEAD

#Note: This program should run with python3.5

#This is the deployment manual.

1. clone code
cd ~
sudo mkdir GameServer
sudo git clone https://github.com/CrzRabbit/enev.git ~/GameServer
sudo git checkout aiosync_server

2. install python3.5 pip3
sudo apt-get install python3.5
sudo apt-get install python3-pip

3. add environmental variable
vim /etc/profile
export PYTHONPATH=~/GameServer
source /etc/profile

4. install aoimysql
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
sudo pip3 install aoimysql

5. install mysql
sudo apt-get install mysql-server-5.7

6. create database
just create the same as sqls in /db/*
