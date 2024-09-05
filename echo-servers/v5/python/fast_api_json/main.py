from fastapi import FastAPI, Form, Request, Response
import json
import os


attack_payload_xss = os.environ.get('PAYLOAD_ONE') or "<script>alert(document.cookie)</script>"
attack_payload_union = os.environ.get('PAYLOAD_TWO') or "0 union select 'password is: ' || password from user limit 1 -- -"

port_number = os.environ.get('FORMIDABLE_PORT_NUMBER') or 8623
instance_number = os.environ.get('INSTANCE_NUMBER') or 1

def successfull_bypass(parsedBody):
    parsedBodyString = str(parsedBody)
    if (attack_payload_union in parsedBodyString or attack_payload_xss in parsedBodyString):
        return 1
    else:
        return 0

app = FastAPI()

@app.get("/")
async def health_check():
    return(Response(status_code=200))

@app.post("/")
async def login(request: Request):
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