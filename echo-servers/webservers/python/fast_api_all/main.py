from fastapi import FastAPI, Form, Request, Response
import json
import os

from xml.dom.minidom import parseString
from xml.sax import make_parser
from xml.sax.handler import feature_external_ges

attack_payload_xss = os.environ.get('PAYLOAD_ONE') or "<script>alert(document.cookie)</script>"
# attack_payload_union = os.environ.get('PAYLOAD_TWO') or "0 union select 'password is: ' || password from user limit 1 -- -"
attack_payload_union = os.environ.get('PAYLOAD_TWO') or "' and 1=1 --"

port_number = os.environ.get('FORMIDABLE_PORT_NUMBER') or 8633
instance_number = os.environ.get('INSTANCE_NUMBER') or 1

def successfull_bypass(parsedBody):
    parsedBodyString = str(parsedBody)
    if (attack_payload_union in parsedBodyString or attack_payload_xss in parsedBodyString):
        return 1
    else:
        return 0

parser = make_parser()
parser.setFeature(feature_external_ges, True)
app = FastAPI()

@app.get("/")
async def health_check():
    return(Response(status_code=200))

@app.post("/multipart")
async def handle_multipart(request: Request, field1: str = Form("none"), field2: str = Form("none")):
    try:
        return(Response(content=json.dumps({
            "success": successfull_bypass({"field1": field1, "field2": field2}),
            "instancenumber": instance_number,
            "parsedbody": {"field1": field1, "field2": field2}
            }), media_type="application/json"))

    except Exception as error:
        print(error)
        return {
            "success": 0,
            "instancenumber": instance_number
        }

@app.post("/xml")
async def handle_xml(request: Request):
    try:
        parser = make_parser()
        parser.setFeature(feature_external_ges, True)
        content_type = request.headers['Content-Type']
        if content_type == 'application/xml':
            body = await request.body()
            document = parseString(body.decode("utf-8"), parser)
            parsed = document.documentElement.toxml()
            # print(document)
            # print(parsed)
            # print(document.toprettyxml())
            return(Response(content=json.dumps({
                "success": successfull_bypass(parsed),
                "instancenumber": instance_number,
                "parsedbody": parsed
                }), media_type="application/json"))            

    except Exception as error:
        print(error)
        return {
            "success": 0,
            "instancenumber": instance_number
        }

@app.post("/json")
async def handle_json(request: Request):
    try:
        parsed_body = await request.json()
        return(Response(content=json.dumps({
            "success": successfull_bypass(parsed_body),
            "instancenumber": instance_number,
            "parsedbody": parsed_body,
            }), media_type="application/json"))

    except Exception as error:
        print(error)
        return {
            "success": 0,
            "instancenumber": instance_number
        }    

if __name__ == "__main__":
    # import uvicorn
    # uvicorn.run(app, host="127.0.0.1", port=port_number)
    app.run(app, host="127.0.0.1", port=port_number)
