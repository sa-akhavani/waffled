import express from 'express';

const attack_payload_xss = process.env.PAYLOAD_ONE || `<script>alert(document.cookie)</script>`
const attack_payload_union = process.env.PAYLOAD_TWO || `0 union select 'password is: ' || password from user limit 1 -- -`

const port_number = process.env.EXPRESS_JSON_PORT_NUMBER || 8620
const instance_number = process.env.INSTANCE_NUMBER || 1


function successfull_bypass(parsedBody) {
    let parsedBodyString = JSON.stringify(parsedBody)
    if (parsedBodyString.includes(attack_payload_union) || parsedBodyString.includes(attack_payload_xss))
        return 1
    else
        return 0
}

const customErrorHandler = (err, req, res, next) => {
    console.log(err.message)
    res.status(500)
    res.json({
        success: 0,
        instancenumber: instance_number
    })
}

const app = express();
app.use(express.json());
app.use(customErrorHandler)

app.get('/', (req, res, next) => {
    res.sendStatus(200)
});

app.post('/', (req, res, next) => {
    try {
        let parsed_body = req.body
        res.json({
            success: successfull_bypass(parsed_body),
            instancenumber: instance_number,
            parsedbody: parsed_body,
        });
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
    console.log(`Server listening on http://localhost:${port_number} ...`);
});
