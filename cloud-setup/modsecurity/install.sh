# Step 1. Install nginx and dependencies
sudo apt update
sudo apt install nginx
#install modsecurity dependencies
sudo apt install libtool autoconf build-essential libpcre3-dev zlib1g-dev libssl-dev libxml2-dev libgeoip-dev liblmdb-dev libyajl-dev libcurl4-openssl-dev libpcre++-dev pkgconf libxslt1-dev libgd-dev automake


# Step 2 Download and Compile ModSecurity
cd /usr/local/src
git clone --depth 100 -b v3/master --single-branch https://github.com/SpiderLabs/ModSecurity
cd ModSecurity
git submodule init
git submodule update

./build.sh
./configure
make
sudo make install


# Step 3. Download and Compile ModSecurity v3 Nginx Connector Source Code
# Make sure to change versoin number match it with your local Nginx server version
wget http://nginx.org/download/nginx-1.18.0.tar.gz
tar -xvzf nginx-1.18.0.tar.gz
# Download the source code for ModSecurity-nginx connector
git clone https://github.com/SpiderLabs/ModSecurity-nginx
cd nginx-1.18.0
./configure --with-compat --with-openssl=/usr/include/openssl/ --add-dynamic-module=/home/ubuntu/ModSecurity-nginx
# Generate the module
make modules
# Copy the module to the Nginx module directory
sudo cp objs/ngx_http_modsecurity_module.so /usr/share/nginx/modules/


# Step 4 - Add it to nginx Configuration
sudo vim /etc/nginx/nginx.conf
# Add these lines
###
load_module modules/ngx_http_modsecurity_module.so;
# modsecurity on;
# modsecurity_rules_file /etc/nginx/nginx-modsecurity.conf;
###

sudo nginx -t
sudo systemctl restart nginx
cat /var/log/nginx/error.log # 2. Ensure that ModSecurity is loading correctly by checking error.log
# at start up for lines indicating ModSecurity is installed. An example
# might appear as follows:
# ```ModSecurity for nginx (STABLE)/2.9.1 (http://www.modsecurity.org/) configured.```


# Installing Core Ruleset
# https://raw.githubusercontent.com/coreruleset/coreruleset/v3.3/master/INSTALL
# https://www.linode.com/docs/guides/securing-nginx-with-modsecurity/

sudo mkdir -p /usr/local/nginx/conf
cd /usr/local/nginx/conf
sudo wget https://github.com/coreruleset/coreruleset/archive/refs/tags/v3.3.5.tar.gz
sudo wget https://github.com/coreruleset/coreruleset/releases/download/v3.3.5/coreruleset-3.3.5.tar.gz.asc
sudo tar -xvzf v3.3.5.tar.gz
cd coreruleset-3.3.5/
sudo mv crs-setup.conf.example crs-setup.conf
sudo mv rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
sudo mv rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf

sudo mkdir -p /etc/nginx/modsec
sudo cp /home/ubuntu/ModSecurity/unicode.mapping /etc/nginx/modsec
sudo cp /home/ubuntu/ModSecurity/modsecurity.conf-recommended /etc/nginx/modsec/modsecurity.conf

sudo vim /etc/nginx/modsec/modsecurity.conf
# SecRuleEngine On

sudo vim /etc/nginx/modsec/main.conf
# Include /etc/nginx/modsec/modsecurity.conf
# Include /usr/local/nginx/conf/coreruleset-3.3.5/crs-setup.conf
# Include /usr/local/nginx/conf/coreruleset-3.3.5/rules/*.conf

sudo vim /etc/nginx/sites-available/default # Add these to server block
# modsecurity on;
# modsecurity_rules_file /etc/nginx/modsec/main.conf;


# By Default the Paranoia Level is 1, if you want to change it, it is in: /usr/local/nginx/conf/coreruleset-3.3.5/crs-setup.conf


# Restart Nginx
sudo nginx -t
sudo systemctl restart nginx

# Full Mofdec Audiy Log is in:
# /var/log/modsec_audit.log

# Test Installation:
curl http://<SERVER-IP/DOMAIN>/index.html?exec=/bin/bash
