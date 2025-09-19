List of all bypasses found during our experiments and the ones that are presented in the WAFFFLED paper.
These requests have bypassed through at least one of the WAFs tested in our experiments and have been parsed by at least one web application from our echo-servers.

### Dataset Folder and File Structure:

- json: json bypasses
- multipart: multipart bypasses
- xml: xml bypasses
- valids: These are valid requests that should be allowed by the WAF. These do not contain any attack payload.
- detectables: These are basic request payloads for different content-types that are detected by most WAFs.

### Important Note:

For each bypass category, we provide one sample of the bypassed request.
But in the real production environmets, each category can have multiple variations and lead to hundreads and thousands of distinct bypasses.

### Disclaimer:

The listed bypasses are only and only for testing purposes and education purposes.
We highly discourage the use of these bypasses in any production environment.
The authors are not responsible for any misuse of the provided information.
