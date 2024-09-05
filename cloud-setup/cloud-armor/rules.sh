# https://cloud.google.com/armor/docs/waf-rules
# https://www.youtube.com/watch?v=RsXbmOb3L2E

# Go to google cloud console
# Network Security -> Cloud Armor Policies -> Create Policy -> Advanced Configuration -> Rules -> Add Rule -> Preconfigured rules
evaluatePreconfiguredExpr('sqli-stable')
evaluatePreconfiguredExpr('xss-v33-stable')
evaluatePreconfiguredExpr('json-sqli-canary')
evaluatePreconfiguredExpr('php-v33-stable')
evaluatePreconfiguredExpr('java-v33-stable')
evaluatePreconfiguredExpr('nodejs-v33-stable')

# if you want to exclude a rule, you can use the following command
# evaluatePreconfiguredExpr('rule-name', ['exclusion-name'])

# ## Rule 1: SQL Injection
evaluatePreconfiguredWaf('sqli-v33-stable', {'sensitivity': 1})

# ## Rule 2: Cross-Site Scripting
evaluatePreconfiguredWaf('xss-v33-stable', {'sensitivity': 1})

# ## Rule 3: JSON Injection
evaluatePreconfiguredWaf('json-sqli-canary', {'sensitivity': 1})
