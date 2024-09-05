https://www.cloudskillsboost.google/focuses/1232?catalog_rank=%7B%22rank%22%3A1%2C%22num_filters%22%3A0%2C%22has_search%22%3Atrue%7D&parent=catalog&search_id=5489793
https://cloud.google.com/armor/docs/security-policy-overview
https://cloud.google.com/armor/docs/waf-rules
https://cloud.google.com/armor/docs/rule-tuning

The evaluatePreconfiguredExpr() expression for preconfigured rules is the only expression that is evaluated against the request body. All other expressions are evaluated against the request header only. Among the HTTP request types with a request body, Google Cloud Armor processes only POST requests. The inspection is limited to the first 8 KB of the POST body and gets decoded like URL query parameters. Google Cloud Armor can parse and apply preconfigured WAF rules for JSON-formatted POST bodies (Content-Type = "application/json"). However, Google Cloud Armor does not support other HTTP Content-Type/Content-Encoding-based decoders such as XML, Gzip, or UTF-16.

## Create Firewall Rules
allow ports in firewall

## Create Instance Template
not necessary

## Create Instance Group
create an instance group with port names

## Create Health Chcecks

## Create Load Balancer

### Create Backend Services
for each port, we need a backend service

### Create a frontend service
frontend service is ip and port of the lb

### create routing rules
check [routing_path_matcher](./routing_path_matcher.yaml) file

### Create Cloud Armor Policy
add rules
add rule to targets which are backend services
