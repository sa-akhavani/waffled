# WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls

This repository contains the datasets and source code related to the paper:
"WAFFLED: Exploiting Parsing Discrepancies to Bypass Web Application Firewalls",
accepted at the ACSAC 2025 conference.
More information about the paper could be accessed (here)[]

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

## ToDo:

- Update README with more details
  -- Add steps to reproduce all found the bypasses
  -- Running the fuzzer with our predefined or custom grammar
- Add Dockeruzied echo server configs
- Add bypass sample for each bypass category
- Add fuzzer grammar for each content-type
- add the t-reqs parser code and documentation
- Add http request relay
- Dockerize the t-reqs fork
