#!/bin/sh


# ports
# 8590 to 8600 - xml
# 8610 to 8620 - multipart


# 8610 - nodejs_express_multipart_formidable
# 8611 - nodejs_http_multipart_busboy
# 8612 - python_flask_multipart
# 8613 - python_fastapi_multipart


# 8590 - nodejs_express_xml_fast-xml-parser
# 8591 - python_flask_xml
# 8592 - python_fastapi_xml


# nodejs_express_multipart_formidable
cd nodejs
cd nodejs_express_multipart_formidable/
npm install
pm2 start index.js --name formidable

# nodejs_http_multipart_busboy
cd ..
cd nodejs_http_multipart_busboy
npm install
pm2 start index.js --name busboy

# nodejs_express_xml_fast
cd ..
cd nodejs_express_xml_fast-xml-parser
npm install
pm2 start index.js --name fast-xml-parser


# # python_flask_multipart
cd ../..
cd python
cd flask_multipart
python3.8 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install flask
pm2 start app.py --name flask-multipart --interpreter=python3.8
deactivate

# python_flask_xml
cd ..
cd flask_xml
python3.8 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install xmltodict
pip install flask
pm2 start app.py --name flask-xml --interpreter=python3.8
deactivate


# python_fast_api_multipart
cd ..
cd fast_api_multipart
python3.8 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pm2 start "uvicorn main:app --reload --port 8613" --name fastapi-multipart
deactivate

# python_fast_api_xml
cd ..
cd fast_api_xml
python3.8 -m venv venv
. venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pm2 start "uvicorn main:app --reload --port 8592" --name fastapi-xml
deactivate
