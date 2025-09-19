#!/bin/sh

# For Each New Framework
# Add rule to nginx reverse proxy for AWS W2 (cloudflare WAF)
# Add rule to AWS ALB to forward port + Create a Target Group for the service and port + Maybe need to open new port range in AWSsecurity group

# ALB Address
# ALB-1117388808.us-east-2.elb.amazonaws.com

##########################
######## NEW MODEL #######
# 8630 laravel_all
# 8631 spring_all
# 8632 flask_all   # xmltodict
# 8633 fast_api_all # xmlminidom
# 8634 express_all # formidable - fast-xml-parser
# 8635 gin_all
# 8621 nodejs_http_json
# 8611 nodejs_http_multipart_busboy
##########################
##########################


# You need to source this script to work
# export PAYLOAD_ONE="0 union select 'password is: ' || password from user limit 1 -- -"
export PAYLOAD_ONE="' and 1=1 --" # does not get blocked by these: json in aws waf
export PAYLOAD_TWO="<script>alert(document.cookie)</script>" # does not get blocked by these: json in cloudflare


# nodejs_express_all
# fast-xml-parser | xml | does not support external entities (SYSTEM) and throws error if it sees it in the request even if not used
# formidable | multipart | handles double boundary well!
# /xml
# /json
# /multipart 
cd nodejs
cd express_all
npm install
pm2 start index.js --name express_all


# nodejs_http_multipart_busboy
cd ..
cd nodejs_http_multipart_busboy
npm install
pm2 start index.js --name busboy


# nodejs_http_json
cd ..
cd nodejs_http_json
npm install
pm2 start index.js --name node-http-json


# python_flask_all
# /xml
# /json
# /multipart
cd ../..
cd python
cd flask_all
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install xmltodict
pip install flask
pm2 start "FLASK_ENV=production FLASK_APP=app.py flask run -h 0.0.0.0 -p 8632 --with-threads" --name flask-all
# pm2 start app.py --name flask-xml --interpreter=python3
deactivate


# python_fast_api_all
# /xml
# /json
# /multipart
cd ..
cd fast_api_all
python3 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install fastapi
pip install "uvicorn[standard]"
pip install python-multipart
# pip install -r requirements.txt
pm2 start "uvicorn main:app --host 0.0.0.0 --port 8633" --name fastapi-all
deactivate

# go_all
# /json
# /xml | does not support entities at all
# /multipart
cd ../..
cd golang
cd gin-all
go mod download
pm2 start "GIN_PORT_NUMBER=8635 go run main.go" --name gin-all


# laravel
# /api/     healthcheck: 
# /api/store (json and multipart)
# /api/storexml
cd ../..
cd laravel
cd multipart
composer update
pm2 start "php artisan serve --host 0.0.0.0 --port=8630" --name laravel


# Java Spring Boot
# XML Does NOT Support any type of entities
# /xml # (schema -> field1) , field2
# /json
# /multipart # field1, field2
cd ../..
cd java
cd demo
pm2 start "./gradlew bootRun --args='--server.port=8631'" --name spring
