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

## Attack Payloads

We use two attack payloads in our experiments. If you are testing a WAF, make sure
that these attack payload are detected by the WAF when sent in a normal request.

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

  - Health Check: `http://localhost:8630/api/`
  - application/xml: `http://localhost:8630/api/storexml`
  - application/json: `http://localhost:8630/api/store`
  - multipart/form-data: `http://localhost:8630/api/store`

- Java Spring Boot

  - Health Check: `http://localhost:8631/`
  - application/xml: `http://localhost:8631/xml`
  - application/json: `http://localhost:8631/json`
  - multipart/form-data: `http://localhost:8631/multipart`

- Python Flask

  - Health Check: `http://localhost:8632/`
  - application/xml: `http://localhost:8632/xml`
  - application/json: `http://localhost:8632/json`
  - multipart/form-data: `http://localhost:8632/multipart`

- Python FastAPI

  - Health Check: `http://localhost:8633/`
  - application/xml: `http://localhost:8633/xml`
  - application/json: `http://localhost:8633/json`
  - multipart/form-data: `http://localhost:8633/multipart`

- Node.js Express

  - Health Check: `http://localhost:8634/`
  - application/xml: `http://localhost:8634/xml`
  - application/json: `http://localhost:8634/json`
  - multipart/form-data: `http://localhost:8634/multipart`

- Golang Gin

  - Health Check: `http://localhost:8635/`
  - application/xml: `http://localhost:8635/xml`
  - application/json: `http://localhost:8635/json`
  - multipart/form-data: `http://localhost:8635/multipart`

- Node.js HTTP JSON
  todo: double check apis for the node.js http servers

  - Health Check: `http://localhost:8621/`
  - application/json: `http://localhost:8621/`

- Node.js HTTP Multipart
  todo: double check apis for the node.js http servers

  - Health Check: `http://localhost:8611/`
  - multipart/form-data: `http://localhost:8611/`

## ToDo:

- Update README with more details
  - Add steps to reproduce all found the bypasses
  - Running the fuzzer with our predefined or custom grammar
- Add Dockeruzied echo server configs
- Add bypass sample for each bypass category
- Add fuzzer grammar for each content-type
- add the t-reqs parser code and documentation
- Add http request relay
- Dockerize the t-reqs fork
