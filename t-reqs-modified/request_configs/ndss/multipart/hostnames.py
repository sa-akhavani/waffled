cloudflare = [
"https://waf2.akhavani.net/laravel/api/store",
"https://waf2.akhavani.net/spring/multipart",
"https://waf2.akhavani.net/flask/multipart",
"https://waf2.akhavani.net/fastapi/multipart",
"https://waf2.akhavani.net/express/multipart",
"https://waf2.akhavani.net/gin/multipart",
"https://waf2.akhavani.net/node-busboy"
]
azure = [
"http://52.249.221.180:8630/api/store",
"http://52.249.221.180:8631/multipart",
"http://52.249.221.180:8632/multipart",
"http://52.249.221.180:8633/multipart",
"http://52.249.221.180:8634/multipart",
"http://52.249.221.180:8635/multipart",
"http://52.249.221.180:8611/",
]
cloudarmor = [
"http://34.111.13.62:80/laravel/api/store",
"http://34.111.13.62:80/spring/multipart",
"http://34.111.13.62:80/flask/multipart",
"http://34.111.13.62:80/fastapi/multipart",
"http://34.111.13.62:80/express/multipart",
"http://34.111.13.62:80/gin/multipart",
"http://34.111.13.62:80/node-busboy",
]
aws = [
"http://alb-1117388808.us-east-2.elb.amazonaws.com:8630/api/store",
"http://alb-1117388808.us-east-2.elb.amazonaws.com:8631/multipart",
"http://alb-1117388808.us-east-2.elb.amazonaws.com:8632/multipart",
"http://alb-1117388808.us-east-2.elb.amazonaws.com:8633/multipart",
"http://alb-1117388808.us-east-2.elb.amazonaws.com:8634/multipart",
"http://alb-1117388808.us-east-2.elb.amazonaws.com:8635/multipart",
"http://alb-1117388808.us-east-2.elb.amazonaws.com:8611",
]
modsec = [
"http://18.116.50.97:80/laravel/api/store",
"http://18.116.50.97:80/spring/multipart",
"http://18.116.50.97:80/flask/multipart",
"http://18.116.50.97:80/fastapi/multipart",
"http://18.116.50.97:80/express/multipart",
"http://18.116.50.97:80/gin/multipart",
"http://18.116.50.97:80/node-busboy",
]
config.target_urls = cloudflare + azure + cloudarmor + aws + modsec

