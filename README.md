# WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls

Datasets and source code for the paper **"WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls"** (ACSAC 2025).
[Read the paper](https://akhavani.net/publications/waffled.pdf)

WAFFLED gives researchers and WAF vendors a way to test a WAF against parsing discrepancies
in HTTP request bodies (`application/json`, `multipart/form-data`, `application/xml`,
`application/x-www-form-urlencoded`). A WAF and the web application behind it may parse the same
body differently. When they do, a request the WAF considers harmless can still be understood by the application.

## Repository Map

| Directory                                       | What it is                                                                                                 |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| [`t-reqs-modified/`](t-reqs-modified)           | Our fork of the [T-Reqs](http://seclab.nu/static/publications/ccs2021treqs.pdf) grammar-based HTTP fuzzer. |
| [`fuzzer-grammar/`](fuzzer-grammar)             | Grammars for JSON, multipart, and XML bodies, plus helper scripts (seeds, hostnames, headers).             |
| [`echo-servers/`](echo-servers)                 | Dockerized web apps (8 frameworks) that parse a body and report whether the attack payload survived.       |
| [`output-parser/`](output-parser)               | Extracts bypassing requests, mutation strings, and affected WAFs from fuzzer logs.                         |
| [`http-request-relay/`](http-request-relay)     | Sends a raw request byte-for-byte over a socket, with optional TLS.                                        |
| [`bypass-database/`](bypass-database)           | Anonymized dataset of the bypass categories from the paper, as raw requests.                               |
| [`http-body-normalizer/`](http-body-normalizer) | Proxy that normalizes or rejects malformed bodies (work in progress).                                      |
| [`publicwww/`](publicwww)                       | Data for the study of interchangeable `multipart/form-data` and `x-www-form-urlencoded` parsing.           |

## How the Pieces Fit Together

```
 fuzzer-grammar/  ──►  t-reqs-modified/  ──►  WAF  ──►  echo-servers/
   (grammars)            (fuzzer)                         (success: 0 | 1)
                              │
                              ▼
                       output-parser/  ──►  bypass-database/
                     (extract bypasses)     (replay with http-request-relay)
```

1. Pick or write a grammar in `fuzzer-grammar/`.
2. Run the fuzzer against a WAF placed in front of the echo servers.
3. An echo server answers `success: 1` when the attack payload was parsed out of the mutated body, and `success: 0` otherwise.
   A request that the WAF let through and the server parsed counts as a bypass.
4. Use `output-parser/` to extract the bypassing requests, then replay them with `http-request-relay/`.

## Quick Start

Replay a sample request against a local echo server:

```bash
# 1. Build and start the echo servers (ports 8630-8635, 8621, 8611)
cd echo-servers
docker build -t waffled-servers .
docker run -p 8630-8635:8630-8635 -p 8621:8621 -p 8611:8611 waffled-servers

# 2. In another terminal, send a raw request to the Express server
cd http-request-relay
python3 http_relay.py localhost 8634 ./sample_requests/valid_json.raw
```

To test a real WAF, put it in front of the echo servers and point the relay at the WAF's host and port.
Pass `-s` for HTTPS.

## Attack Payloads

WAFFLED only changes the structure of a request and never touches the attack payload.
Use any payload, but check that your WAF blocks it in a plain request first.
The experiments use two simple payloads that most default rulesets block.
They are set in the [echo-servers Dockerfile](echo-servers/Dockerfile) as `PAYLOAD_ONE` and `PAYLOAD_TWO`:

| Type          | Payload                                   |
| ------------- | ----------------------------------------- |
| SQL injection | `' and 1=1 --`                            |
| XSS           | `<script>alert(document.cookie)</script>` |

## Echo Servers

Each echo server parses the body and returns the parsed content as JSON.
It adds `success: 1` if the payload is present in the parsed content and `success: 0` otherwise.

| Framework                         | Port |
| --------------------------------- | ---- |
| PHP Laravel                       | 8630 |
| Java Spring Boot                  | 8631 |
| Python Flask                      | 8632 |
| Python FastAPI                    | 8633 |
| Node.js Express                   | 8634 |
| Golang Gin                        | 8635 |
| Node.js HTTP (JSON)               | 8621 |
| Node.js HTTP + Busboy (multipart) | 8611 |

Endpoints and run instructions are in [`echo-servers/README.md`](echo-servers/README.md).

## HTTP Request Relay

To manually test a request, use the HTTP request relay. It forwards an HTTP request to the destination as a binary string, without any modification.
More details about the relay and how to use it can be found in the [`http-request-relay/`](http-request-relay) directory's README.

```bash
python3 http_relay.py <host> <port> <raw_request_file> [-s]
```

_Important Note_: Do NOT use `curl` or any other HTTP client to send the generated requests to the WAFs or echo servers, because they will modify the request before sending it to the destination.

## Content-Types and Grammars

The fuzzer supports other content-types if you add a grammar for them.
See [`fuzzer-grammar/`](fuzzer-grammar) for the grammars and how to run the fuzzer with them.

## PublicWWW Study

Many frameworks and libraries parse `multipart/form-data` and `application/x-www-form-urlencoded` with the same API.
An attacker can send a known multipart bypass to a form that only expects URL-encoded data,
and the application may still accept it.
`publicwww/` contains the data from our search of forgot-password forms on popular websites.

## HTTP Normalizer

See [`http-body-normalizer/`](http-body-normalizer).

## Roadmap

- [ ] Dockerize the T-Reqs fork
- [ ] Document the HTTP normalizer
- [ ] Automatically deduplicate bypasses that share a root cause (currently done by hand)
- [ ] HTTP/2 support in the echo servers and fuzzer
- [ ] Automatic fingerprinting of a target's WAF and web framework from the bypass database

## Contributing

Contributions are welcome:

- Grammars for new content-types, or for more features of the existing ones
- Echo servers for more frameworks and languages
- Any item from the roadmap above

## License

See [LICENSE](LICENSE). The T-Reqs fork has its own license in `t-reqs-modified/LICENSE`.

## Disclaimer

Everything in this repository is for testing, education, and research only.
Do not use it against systems you do not own or have permission to test.
The authors are not responsible for misuse of this material.

## Citation

If you use this repository, please cite the paper:

```bibtex
@INPROCEEDINGS{acsac2025waffled,
  title={WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls},
  author={Ali Akhavani, Seyed and Jabiyev, Bahruz and Kallus, Ben and Topcuoglu, Cem and Bratus, Sergey and Kirda, Engin},
  booktitle={2025 IEEE Annual Computer Security Applications Conference (ACSAC)},
  year={2025},
  pages={689-702},
  keywords={Cloud computing;Firewalls (computing);Fuzzing;Logic gates;Information filters;HTTP;Usability;Protection;Standards;Payloads;Web Security;Web Application Firewalls;Fuzzing;HTTP;Parsing Discrepancies;Request Smuggling;WAF Evasion},
  doi={10.1109/ACSAC67867.2025.00062}
}
```
