## T-REQS Output Parser

These scripts are used to parse T-REQS logs and extract useful information such as:

- Bypass success
- Request-ID
- Request-Raw binary string
- Mutation string
- Affected WAF list
- Fuzzer Seed

If a request bypasses any of the WAFs, it would be added to the parser output file in this format:

```json
{
  "request-id": "",
  "raw_request": b'',
  "mutation-string": "",
  "affected-wafs: "",
  "seed": treqs_results_filename,
  "category" : None,
}
```

How the parser works is that it looks for some specific headers in each sent request. Some are mandatory, some are optional.
The affected-wafs list is something that we define in our t-reqs grammar file through passing a `parser: <WAF>-<Echo_Server>` header. This can be customized based on your needs.

## How to use

Run the parser and pass the t-reqs output filename as an argument.
The parser will create a new file with the same name as the input file but with `_parsed.json` appended to it.

```bash
./parser.sh <filename>
```

There is already a sample `data` folder with some t-reqs output for testing.

### Identifying Unique Bypasses

There might be multiple requests that bypass the same WAF with a shared mutation string.
This is not a mandatory process but is useful to deal with less data and focus on unique bypasses.
This is a work in progress, this process should be automated in the future or
the fuzzer should be updated to avoid going through the tree mutation process when a bypass is detected.
For now, you can check the parser output file and remove the requests that have shared mutation string manually.
Read the paper for more information on this.

### Some usefull commands

Use http-request-relay instead of this which is way more reliable and easier to use.
But to send a raw http request, you can use netcat (nc) or openssl s_client.

```bash

# Send a POST request to a target server using netcat (nc)
printf 'POST /express/json HTTP/1.1\r\nHost: waf.mytargetwaf.net\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\nContent-Type: application/json\r\nContent-Length: 20\r\n\r\n{"field1": "value1"}\r\n' | nc <lb ip> <port> -vvv


# FOR SSL
# Send a POST request to a target server using openssl s_client
printf 'POST /express/json HTTP/1.1\r\nHost: waf.mytargetwaf.net\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\nContent-Type: application/json\r\nContent-Length: 20\r\n\r\n{"field1": "value1"}' | openssl s_client -connect <target url>:443 -ign_eof -quiet 2>/dev/null

# Or
# This one is not working on ncat versions less than 7.9\*. Could not be used on ubuntu 22.04
# printf 'POST /express/json HTTP/1.1\r\nHost: waf.mytargetwaf.net\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\nContent-Type: application/json\r\nContent-Length: 20\r\n\r\n{"field1": "value1"}' | ncat --ssl <target url> 443

```
