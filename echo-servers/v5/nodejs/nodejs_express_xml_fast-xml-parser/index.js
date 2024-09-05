const { XMLParser } = require('fast-xml-parser');
const express = require('express');

const attack_payload_xss = process.env.PAYLOAD_ONE || `<script>alert(document.cookie)</script>`
const attack_payload_union = process.env.PAYLOAD_TWO || `0 union select 'password is: ' || password from user limit 1 -- -`

const port_number = process.env.FORMIDABLE_PORT_NUMBER || 8590
const instance_number = process.env.INSTANCE_NUMBER || 1

const parser = new XMLParser({
    ignoreAttributes: false,
    processEntities: true,
    htmlEntities: true,
    // removeNSPrefix: true,
});

const app = express();
app.use(express.text({ type: 'application/xml' }));

function successfull_bypass(parsedBody) {
    let parsedBodyString = JSON.stringify(parsedBody)
    if (parsedBodyString.includes(attack_payload_union) || parsedBodyString.includes(attack_payload_xss))
        return 1
    else
        return 0
}

app.get('/', (req, res, next) => {
    res.sendStatus(200)
});

app.post('/', (req, res) => {
    try {
        // console.log(`request #: ${req.headers['x-request-id']}`)
        let parsed_body = parser.parse(req.body)
        console.log(JSON.stringify(parsed_body));
        res.json({
            success: successfull_bypass(parsed_body),
            instancenumber: instance_number,
            parsedbody: parsed_body,
        })

    } catch (err) {
        console.log(err)
        res.status(500)
        res.json({
            success: 0,
            instancenumber: instance_number
        })
    }
});

app.listen(port_number, () => {
    console.log(`Server listening on port ${port_number}`);
});