# Works Well!
printf 'POST /express/json HTTP/1.1\r\nHost: waf2.akhavani.net\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\nContent-Type: application/json\r\nContent-Length: 20\r\n\r\n{"field1": "value1"}\r\n' | nc 18.116.50.97 80 -vvv

# FOR SSL
printf 'POST /express/json HTTP/1.1\r\nHost: waf2.akhavani.net\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\nContent-Type: application/json\r\nContent-Length: 20\r\n\r\n{"field1": "value1"}' | openssl s_client -connect waf2.akhavani.net:443 -ign_eof -quiet 2>/dev/null
# This one is not working on ncat versions less than 7.9*. Could not be used on ubuntu 22.04
# printf 'POST /express/json HTTP/1.1\r\nHost: waf2.akhavani.net\r\nUser-Agent: Mozilla/5.0\r\nConnection: close\r\nContent-Type: application/json\r\nContent-Length: 20\r\n\r\n{"field1": "value1"}' | ncat --ssl waf2.akhavani.net 443

