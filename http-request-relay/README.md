How to use the http_relay:

```bash
python3 http_relay.py <host> <port> <raw_request_file> <-s for ssl (optional)>

```

Working examples after setting up all echo servers:

```bash
python3 http_relay.py localhost 8634 valid_json.raw
python3 http_relay.py localhost 8634 valid_multipart.raw
python3 http_relay.py localhost 8634 valid_xml.raw

```
