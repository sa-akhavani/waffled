#!/bin/sh

# For Each New Framework
# Add rule to nginx reverse proxy for AWS W2 (cloudflare WAF)
# Add rule to AWS ALB to forward port + Create a Target Group for the service and port + Maybe need to open new port range in AWSsecurity group

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


## nodejs_express_all
# fast-xml-parser | xml | does not support external entities (SYSTEM) and throws error if it sees it in the request even if not used
# /xml
# /json
# /multipart 
cd nodejs
cd express_all
npm install


## nodejs_http_multipart_busboy
cd ..
cd nodejs_http_multipart_busboy
npm install


## nodejs_http_json
cd ..
cd nodejs_http_json
npm install


## python_flask_all
# /xml
# /json
# /multipart


## python_fast_api_all
# /xml
# /json
# /multipart

## go_all
# /json
# /xml | does not support entities at all
# /multipart
cd ../..
cd golang
cd gin-all
go mod download


## laravel
# /api/     healthcheck: 
# /api/store (json and multipart)
# /api/storexml
cd ../..
cd laravel
cd multipart
composer update


## Java Spring Boot
# XML Does NOT Support any type of entities
# /xml # (schema -> field1) , field2
# /json
# /multipart # field1, field2
