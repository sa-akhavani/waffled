#!/bin/bash -i
# Python 3.10.12
# Node v18.16.1
# go version go1.20.6 linux/amd64

sudo apt update -y
sudo apt dist-upgrade -y
sudo apt autoremove -y
sudo apt autoclean -y
sudo apt install curl wget zip unzip -y

# Set INSTANCE_NUMBER environment variable
# export INSTANCE_NUMBER=1

# Create Deploy Key
# ssh-keygen -t rsa

### Install node v18.16.1 on production ###
# Installing Node.js local
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash
source ~/.bashrc
nvm list-remote
nvm install v18.16.1
nvm alias default v18.16.1
nvm use default
npm install -g pm2

# Install Go
curl -OL https://golang.org/dl/go1.20.6.linux-amd64.tar.gz
sha256sum go1.20.6.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.20.6.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin
# also add it to .bashrc
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc

# Install Python
sudo apt install python3.10-venv -y

# Install PHP
# sudo apt -y install software-properties-common
sudo apt install php-cli php-xml php-curl -y
curl -sS https://getcomposer.org/installer -o /tmp/composer-setup.php
sudo php /tmp/composer-setup.php --install-dir=/usr/local/bin --filename=composer
composer

# Install Java Spring Boot
sudo apt install openjdk-21-jdk openjdk-21-jre -y
curl -s "https://get.sdkman.io" | bash
source ~/.bashrc
sdk install gradle 8.6

# Reboot
sudo apt autoremove -y
sudo apt autoclean -y
sudo reboot

# Install Nginx and Certbot
# sudo apt install nginx
# sudo snap install core; sudo snap refresh core
