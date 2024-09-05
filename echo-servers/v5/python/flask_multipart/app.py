from flask import Flask, jsonify, request
import os

attack_payload_xss = os.environ.get('PAYLOAD_ONE') or "<script>alert(document.cookie)</script>"
attack_payload_union = os.environ.get('PAYLOAD_TWO') or "0 union select 'password is: ' || password from user limit 1 -- -"

port_number = os.environ.get('FORMIDABLE_PORT_NUMBER') or 8610
instance_number = os.environ.get('INSTANCE_NUMBER') or 1

def successfull_bypass(parsedBody):
    parsedBodyString = str(parsedBody)
    if (attack_payload_union in parsedBodyString or attack_payload_xss in parsedBodyString):
        return 1
    else:
        return 0

app = Flask(__name__)

@app.route('/', methods=['GET'])
def health_check():
    return jsonify(success=True)

@app.route('/', methods=['POST'])
def index():
    try:
        # request_id = request.headers['X-Request-ID']
        # print('request #: ', request_id)

        request_form = request.form
        # print(str(request_form))
        return {
            "success": successfull_bypass(request_form),
            "instancenumber": instance_number,
            "parsedbody": request_form
        }
        # return jsonify(request_form)
    
    except Exception as error:
        print(error)
        return {
            "success": 0,
            "instancenumber": instance_number
        }



if __name__ == "__main__":
    app.run(port=port_number)
