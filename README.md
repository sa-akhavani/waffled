# WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls

This repository contains the datasets and source code related to the paper:
"WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls",
accepted at the ACSAC 2025 conference.
More information about the paper could be accessed [here](https://arxiv.org/abs/2503.10846). If you are planning to use this repository, please consider citing this paper using the following BibTeX:

```bibtex
@INPROCEEDINGS{acsac2025waffled,
  title={WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls},
  author={Ali Akhavani, Seyed and Jabiyev, Bahruz and Kallus, Ben and Topcuoglu, Cem and Bratus, Sergey and Kirda, Engin},
  booktitle={2025 IEEE Annual Computer Security Applications Conference (ACSAC)},
  year={2025},
  volume={},
  number={},
  pages={689-702},
  keywords={Cloud computing;Firewalls (computing);Fuzzing;Logic gates;Information filters;HTTP;Usability;Protection;Standards;Payloads;Web Security;Web Application Firewalls;Fuzzing;HTTP;Parsing Discrepancies;Request Smuggling;WAF Evasion},
  doi={10.1109/ACSAC67867.2025.00062}
}
```

## Overview

With the content of this repository, we aim to provide the community and WAF vendors
a tool to rigorously test their products against parsing discrepancies for different content-types.

We also provide a dataset of our discovered bypasses in popular WAFs (anonymized).

The codebase includes:

- A HTTP/1.1 fuzzer to generate requests with different content-types.
- Multiple grammars for the fuzzer to test different features of each content-type and RFCs.
- A parser to extract the generated request results from the fuzzer output.
- Echo servers to test if the web applications behind the WAFs can parse the request payload correctly.
- HTTP request relay to forward an http request to the destination in binary string format without any modification.
- A dataset of discovered bypasses in popular WAFs (anonymized).
- HTTP Normalizer to normalize (cleanse) or block malformed HTTP requests.

## Content-Types

We focus on the following content-types in our experiments:

- application/json
- multipart/form-data
- application/xml
- application/x-www-form-urlencoded

Multiple grammars are provided for each content-type in the fuzzer to test
differet features of each content-type and RFCs. Check the `fuzzer-grammar` directory for more details.

You can test any other content-type by adding a custom grammar for it in the fuzzer.

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

You can find the details about the api endpoints and how to run them in the `echo-servers` directory's README.

## HTTP Request Relay

To manually test a request, you can use the HTTP request relay to forward an http request to the destination in binary string format without any modification.
More details about the relay and how to use it can be found in the `http-request-relay` directory's README.

_Important Note_: Do NOT use `curl` or any other HTTP client to send the generated requests to the WAFs or echo servers because they will modify the request before sending it to the destination.

## PublicWWW Dataset and Study

We discovered that many frameworks and libraries use the same api or function for parsing `multipart/form-data` and `application/x-www-form-urlencoded` content-types.

This could lead to concerning attacks where a website expects a request in `application/x-www-form-urlencoded` content-type, but the attacker uses the same api and sends their request with a known bypass of the `multipart/form-data` content-type and the target website accepts that request without them knowing that their web server accepts that content-type.

The dataset for the study of interchangeable content-types of multipart/form-data and x-www-form-urlencoded.
This is achieved by searching through the forgot password forms of famous websites.

## HTTP Normalizer

Documentation Work In Progress.

## ToDo:

- Update README with more details
- Dockerize the t-reqs fork
- Update HTTP-Normalizer documentation

## How You Can Contribute

We welcome contributions from the community to enhance the capabilities of this repository.
Here are some ways you can contribute:

- Add more grammars for different content-types and test different features of each content-type and RFCs.
- Automate removal of mutations that share the same bypass root cause.
  ( e.g., if a mutation string is shared between 2 bypasses, only one of them should be kept in the dataset.)
  right now, this is done manually by analyzing the bypasses and their mutation strings.
- Add more echo servers for different web frameworks and languages.
- HTTP/2 support for both echo servers and using a new fuzzer.
- Automatic fingerprinting of the WAF and Web Framework of a target website using the bypass database.

## Important Disclaimer:

Any provided code, dataset, or information in this repository is for testing, educational, and research purposes only.
We highly discourage the use of any of the provided material in any environment that could cause harm or damage,
including any production system that do not belong to you.
The authors are not responsible for any misuse of the provided information on this repository.
