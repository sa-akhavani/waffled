# WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls

This repository contains the datasets and source code related to the paper:
"WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls",
accepted at the ACSAC 2025 conference.
More information about the paper could be accessed [here](https://arxiv.org/abs/2503.10846).

## Citation

If you are planning to use the datasets, source code, or the results of this project,
you can cite this paper using the following BibTEX template:

```bibtex
@misc{akhavani2025waffled,
      title={WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls},
      author={Seyed Ali Akhavani and Bahruz Jabiyev and Ben Kallus and Cem Topcuoglu and Sergey Bratus and Engin Kirda},
      year={2025},
      eprint={2503.10846},
      archivePrefix={arXiv},
      primaryClass={cs.CR},
      url={https://arxiv.org/abs/2503.10846},
}
```

## Overview

With the content of this repository, we aim to provide the community and WAF vendors
a tool to rigorously test their products against parsing discrepancies for different content-types.

We also provide a dataset of our discovered bypasses in popular WAFs.

The codebase includes:

- A HTTP/1.1 fuzzer to generate requests with different content-types
- Grammar for the fuzzer for different content-types.
- A parser to extract the generated request results from the fuzzer output
- Echo servers to test if the web applications behind the WAFs can parse the request payload correctly
- HTTP request relay to forward an http request to the destination in binary string format without any modification.
- A dataset of discovered bypasses in popular WAFs
- HTTP Normalizer to normalize (cleanse) or block malformed HTTP requests.

## Content-Types

We focus on the following content-types in our experiments:

- application/json
- multipart/form-data
- application/xml
- application/x-www-form-urlencoded

Multiple grammars are provided for each content-type in the fuzzer to test
differet features of each content-type and RFCs.

You can test any other content-type by adding a grammar for it in the fuzzer.

## Attack Payloads

Any attack payload could be used in the experiments since
waffled does not touch the attack payloads.
It only modifies the request structure. If you are testing a WAF, make sure
that these attack payloads are detected by the WAF when sent in a normal request.

We use two simple attack payloads in our experiments that are blocked by most WAFs default rulesets.

These are hard-coded in the Dockerfile of the echo servers and would be passed to the web apps as an environment variable named `ATTACK_PAYLOAD`.

- XSS Payload:

```html
<script>
  alert(document.cookie);
</script>
```

- SQL Injection Payload:

```sql
' and 1=1 --
```

## Echo Servers

We provide echo server infrastructure and code for the following web servers:

- PHP Laravel
- Java Spring Boot
- Python Flask
- Python FastAPI
- Node.js Express
- Golang Gin
- Node.js HTTP JSON
- Node.js HTTP Multipart

These echo servers will parse the request body and return the parsed content in the response in JSON format.
Also, they will check if the attack payload is present in the parsed content.
If the attack payload is found, they add a `success: 1` in their response.
Otherwise, they will have the `success: 0` in their response.

You can find the details about the api endpoints and how to run them in the `echo_servers` directory's README.

## HTTP Request Relay

To manually test a request, you can use the HTTP request relay to forward an http request to the destination in binary string format without any modification.
More details about the relay and how to use it can be found in the `http_request_relay` directory's README.

## ToDo:

- Update README with more details
  - Add steps to reproduce all found the bypasses
  - Running the fuzzer with our predefined or custom grammar
- Add bypass sample for each bypass category
- Add fuzzer grammar for each content-type
- add the t-reqs parser code and documentation
- Add http request relay
- Dockerize the t-reqs fork

### Important Disclaimer:

Any provided code, dataset, or information in this repository is for testing, educational, and research purposes only.
We highly discourage the use of any of the provided material in any environment that could cause harm or damage,
including any production system that do not belong to you.
The authors are not responsible for any misuse of the provided information on this repository.
