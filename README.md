# enev
# This is the deployment manual.
1. clone code
cd ~
sudo mkdir GameServer
sudo git clone https://github.com/CrzRabbit/enev.git /GameServer
sudo git checkout aiosync_server

2. install python3.5 pip3
sudo apt-get install python3.5
sudo apt-get install python3-pip
export PYTHONPATH=~/GameServer

3. install aoimysql
sudo apt-get install python-dev python-pip libxml2-dev libxslt1-dev zlib1g-dev libffi-dev libssl-dev
sudo pip3 install aoimysql

4. install mysql
sudo apt-get install mysql-server-5.7

5. create database
just create the same as sqls in /db/*
