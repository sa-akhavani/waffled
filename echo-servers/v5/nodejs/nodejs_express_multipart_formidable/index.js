import express from 'express';
import formidable from 'formidable';

const attack_payload_xss = process.env.PAYLOAD_ONE || `<script>alert(document.cookie)</script>`
const attack_payload_union = process.env.PAYLOAD_TWO || `0 union select 'password is: ' || password from user limit 1 -- -`

const port_number = process.env.FORMIDABLE_PORT_NUMBER || 8610
const instance_number = process.env.INSTANCE_NUMBER || 1

const app = express();
// app.use(express.raw({ type: "*/*" }))


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


app.post('/', (req, res, next) => {
    try {
        const form = formidable({});        
        form.parse(req, (err, fields, files) => {
            if (err) {
                console.log(err)
                res.status(500)
                res.json({
                    success: 0,
                    instancenumber: instance_number,
                })
            } else {
                let parsed_body = { fields, files }
                // console.log(JSON.stringify({ fields, files }))
                res.json({
                    success: successfull_bypass(parsed_body),
                    instancenumber: instance_number,
                    parsedbody: parsed_body,
                });
            }
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