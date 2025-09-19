const http = require('http');
const busboy = require('busboy');
const { error } = require('console');

const attack_payload_xss = process.env.PAYLOAD_ONE || `<script>alert(document.cookie)</script>`
// const attack_payload_union = process.env.PAYLOAD_TWO || `0 union select 'password is: ' || password from user limit 1 -- -`
const attack_payload_union = process.env.PAYLOAD_TWO || `' and 1=1 --`

const port_number = process.env.FORMIDABLE_PORT_NUMBER || 8611
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
    if (req.method === 'POST') {
        try {
            results = {};
            const bb = busboy({ headers: req.headers });

            // console.log(`request #: ${req.headers['x-request-id']}`)

            bb.on('file', (name, file, info) => {
                const { filename, encoding, mimeType } = info;
                console.log(
                    `File [${name}]: filename: %j, encoding: %j, mimeType: %j`,
                    filename,
                    encoding,
                    mimeType
                );
                file.on('data', (data) => {
                    // console.log(`File [${name}] got ${data.length} bytes`);
                }).on('close', () => {
                    // console.log(`File [${name}] done`);
                });
            });

            bb.on('field', (name, val, info) => {
                // console.log(`${name}: %j`, val);
                results[name] = val
            });

            bb.on('error', (err) => {
                console.log(err)
            });

            bb.on('close', () => {
                parsed_body = results

                response_object = {
                    success: successfull_bypass(parsed_body),
                    instancenumber: instance_number,
                    parsedbody: parsed_body,
                }
                res.setHeader('Content-Type', 'application/json');
                res.writeHead(200, { Connection: 'close', Location: '/' });
                res.end(JSON.stringify(response_object));

            });
            
            req.pipe(bb);

        } catch (err) {
            console.log(err)
            res.setHeader('Content-Type', 'application/json');
            res.writeHead(500, { Connection: 'close', Location: '/' });
            res.end(JSON.stringify({
                success: 0,
                instancenumber: instance_number
            }));
            // req.pipe(bb);
        }

    } else if (req.method === 'GET') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('OK\n');
    }
});


server.listen(port_number, () => {
    console.log(`Listening for requests on port ${port_number}`);
});
