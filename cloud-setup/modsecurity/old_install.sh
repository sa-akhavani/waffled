sudo apt install libxml2 libxml2-dev libexpat1-dev libpcre3-dev libpcre++-dev libyajl-dev libgeoip-dev libcurl4-gnutls-dev dh-autoreconf
sudo apt install g++ gcc make
sudo apt install build-essential binutils libssl-dev zlib1g-dev



# Install Nginx from Source
sudo mkdir /usr/src/nginx
sudo chown `whoami` /usr/src/nginx
cd /usr/src/nginx
wget https://nginx.org/download/nginx-1.24.0.tar.gz
tar -xvzf nginx-1.24.0.tar.gz
cd nginx-1.24.0

./configure --prefix=/opt/nginx-1.24.0 --with-http_ssl_module --with-threads --with-file-aio
make
sudo make install
sudo chown -R `whoami` /opt/nginx-1.24.0

sudo ln -s /opt/nginx-1.24.0 /nginx
sudo chown `whoami` --no-dereference /nginx
cd /nginx
sudo ./sbin/nginx
ps -awuq $(cat logs/nginx.pid)
# $> sudo ./sbin/nginx -s stop
# $> sudo ./sbin/nginx -V



# https://www.nginx.com/blog/compiling-dynamic-modules-nginx-plus/
# Install Modsecurity

sudo mkdir /usr/src/modsecurity
sudo chown `whoami` /usr/src/modsecurity
cd /usr/src/modsecurity

wget https://github.com/owasp-modsecurity/ModSecurity/releases/download/v3.0.11/modsecurity-v3.0.11.tar.gz
wget https://github.com/owasp-modsecurity/ModSecurity/releases/download/v3.0.11/modsecurity-v3.0.11.tar.gz.sha256
sha256sum --check modsecurity-v3.0.11.tar.gz.sha256

tar -xvzf modsecurity-v3.0.11.tar.gz 
cd modsecurity-v3.0.11/
./configure --prefix=/opt/modsecurity-3.0.11 --enable-mutex-on-pm

make
sudo make install
sudo chown -R `whoami` /opt/modsecurity-3.0.11

cd /usr/src/modsecurity
wget https://github.com/owasp-modsecurity/ModSecurity-nginx/releases/download/v1.0.3/modsecurity-nginx-v1.0.3.tar.gz
wget https://github.com/owasp-modsecurity/ModSecurity-nginx/releases/download/v1.0.3/modsecurity-nginx-v1.0.3.tar.gz.sha256
sha256sum --check modsecurity-nginx-v1.0.3.tar.gz.sha256

tar -xvzf modsecurity-nginx-v1.0.3.tar.gz

# cd /usr/src/nginx/nginx-1.13.9
cd /usr/src/nginx/nginx-1.24.0/
export MODSECURITY_LIB="/usr/src/modsecurity/modsecurity-v3.0.11/src/.libs/"
export MODSECURITY_INC="/usr/src/modsecurity/modsecurity-v3.0.11/headers/"
./configure --prefix=/opt/nginx-1.24.0 --with-http_ssl_module --with-threads --with-file-aio --with-compat --add-dynamic-module=/usr/src/modsecurity/modsecurity-nginx-v1.0.3

make
sudo make install
sudo chown -R `whoami` /opt/nginx-1.24.0
make modules


[ ! -d /nginx/modules ] && mkdir /nginx/modules
cp objs/ngx_http_modsecurity_module.so /nginx/modules


cd /nginx/conf
sudo vim nginx.conf
# load_module modules/ngx_http_modsecurity_module.so;
# modsecurity on;
sudo /nginx/sbin/nginx
sudo /nginx/sbin/nginx -t
sudo /nginx/sbin/nginx -s reload
sudo /nginx/sbin/nginx -s stop

# # load_module modules/ngx_http_modsecurity_module.so;
# /usr/src/modsecurity/modsecurity-nginx-v1.0.3


# Install Core Ruleset!
cd /nginx/conf/
wget https://github.com/coreruleset/coreruleset/archive/refs/tags/v3.3.5.tar.gz
wget https://github.com/coreruleset/coreruleset/releases/download/v3.3.5/coreruleset-3.3.5.tar.gz.asc
tar -xvzf v3.3.5.tar.gz
ln -s coreruleset-3.3.5 /nginx/conf/crs
cd crs
cp crs-setup.conf.example crs-setup.conf
rm v3.3.5.tar.gz
cp rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf.example rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
cp rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf.example rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf



cd /nginx/conf
vim modsec_includes.conf

include modsecurity.conf
include crs/crs-setup.conf
include crs/rules/REQUEST-900-EXCLUSION-RULES-BEFORE-CRS.conf
include crs/rules/REQUEST-901-INITIALIZATION.conf
include crs/rules/REQUEST-903.9001-DRUPAL-EXCLUSION-RULES.conf
include crs/rules/REQUEST-903.9002-WORDPRESS-EXCLUSION-RULES.conf
include crs/rules/REQUEST-903.9003-NEXTCLOUD-EXCLUSION-RULES.conf
include crs/rules/REQUEST-903.9004-DOKUWIKI-EXCLUSION-RULES.conf
include crs/rules/REQUEST-903.9005-CPANEL-EXCLUSION-RULES.conf
include crs/rules/REQUEST-903.9006-XENFORO-EXCLUSION-RULES.conf
include crs/rules/REQUEST-905-COMMON-EXCEPTIONS.conf
include crs/rules/REQUEST-910-IP-REPUTATION.conf
include crs/rules/REQUEST-911-METHOD-ENFORCEMENT.conf
include crs/rules/REQUEST-912-DOS-PROTECTION.conf
include crs/rules/REQUEST-913-SCANNER-DETECTION.conf
include crs/rules/REQUEST-920-PROTOCOL-ENFORCEMENT.conf
include crs/rules/REQUEST-921-PROTOCOL-ATTACK.conf
include crs/rules/REQUEST-930-APPLICATION-ATTACK-LFI.conf
include crs/rules/REQUEST-931-APPLICATION-ATTACK-RFI.conf
include crs/rules/REQUEST-932-APPLICATION-ATTACK-RCE.conf
include crs/rules/REQUEST-933-APPLICATION-ATTACK-PHP.conf
include crs/rules/REQUEST-934-APPLICATION-ATTACK-NODEJS.conf
include crs/rules/REQUEST-941-APPLICATION-ATTACK-XSS.conf
include crs/rules/REQUEST-942-APPLICATION-ATTACK-SQLI.conf
include crs/rules/REQUEST-943-APPLICATION-ATTACK-SESSION-FIXATION.conf
include crs/rules/REQUEST-944-APPLICATION-ATTACK-JAVA.conf
include crs/rules/REQUEST-949-BLOCKING-EVALUATION.conf
include crs/rules/RESPONSE-950-DATA-LEAKAGES.conf
include crs/rules/RESPONSE-951-DATA-LEAKAGES-SQL.conf
include crs/rules/RESPONSE-952-DATA-LEAKAGES-JAVA.conf
include crs/rules/RESPONSE-953-DATA-LEAKAGES-PHP.conf
include crs/rules/RESPONSE-954-DATA-LEAKAGES-IIS.conf
include crs/rules/RESPONSE-959-BLOCKING-EVALUATION.conf
include crs/rules/RESPONSE-980-CORRELATION.conf
include crs/rules/RESPONSE-999-EXCLUSION-RULES-AFTER-CRS.conf



cd /nginx
mkdir sites-available
mkdir sites-enabled

vim conf/nginx.conf
# Inside the http block, add this:
# include /etc/nginx/sites-enabled/*;
sudo touch /nginx/sites-available/default
sudo ln -s /nginx/sites-available/default /nginx/sites-enabled/default