const http = require('http')

const attack_payload_xss = process.env.PAYLOAD_ONE || `<script>alert(document.cookie)</script>`
// const attack_payload_union = process.env.PAYLOAD_TWO || `0 union select 'password is: ' || password from user limit 1 -- -`
const attack_payload_union = process.env.PAYLOAD_TWO || `' and 1=1 --`

const port_number = process.env.EXPRESS_JSON_PORT_NUMBER || 8621
const instance_number = process.env.INSTANCE_NUMBER || 1

function successfull_bypass(parsedBody) {
    let parsedBodyString = JSON.stringify(parsedBody)
    if (parsedBodyString.includes(attack_payload_union) || parsedBodyString.includes(attack_payload_xss))
        return 1
    else
        return 0
}

const server = http.createServer();

// Listen to the request event
server.on('request', (req, res) => {
    const { headers, method, url } = req;
    if (method === 'POST') {
        try {
            let body = [];
            req
                .on('error', err => {
                    console.log('req err')
                    throw new Error(err)
                })
                .on('data', chunk => {
                    body.push(chunk);
                })
                .on('end', () => {
                    body = Buffer.concat(body).toString();
                    try {
                        let parsed_body = JSON.parse(body);
                        response_object = {
                            success: successfull_bypass(parsed_body),
                            instancenumber: instance_number,
                            parsedbody: parsed_body,
                        }
                        res.statusCode = 200;
                        res.setHeader('Content-Type', 'application/json');
                        res.end(JSON.stringify(response_object))
                    } catch (err) {
                        console.log(err)
                        res.setHeader('Content-Type', 'application/json');
                        res.writeHead(500, { Connection: 'close', Location: '/' });
                        res.end(JSON.stringify({
                            success: 0,
                            instancenumber: instance_number
                        }));
                    }
                });

        } catch (err) {
            console.log('err')
            console.log(err)
            res.setHeader('Content-Type', 'application/json');
            res.writeHead(500, { Connection: 'close', Location: '/' });
            res.end(JSON.stringify({
                success: 0,
                instancenumber: instance_number
            }));
        }

    } else if (method === 'GET') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('OK\n');
    }
});


server.listen(port_number, () => {
    console.log(`Listening for requests on port ${port_number}`);
}); 
