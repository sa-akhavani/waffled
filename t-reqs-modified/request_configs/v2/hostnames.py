def get_hostnames_multipart():
    cloudflare = [
    "https://waf2.akhavani.net/laravel/api/store",
    "https://waf2.akhavani.net/spring/multipart",
    "https://waf2.akhavani.net/flask/multipart",
    "https://waf2.akhavani.net/fastapi/multipart",
    "https://waf2.akhavani.net/express/multipart",
    "https://waf2.akhavani.net/gin/multipart",
    "https://waf2.akhavani.net/node-busboy/"
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
    "http://34.111.13.62:80/node-busboy/",
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
    "http://18.116.50.97:80/node-busboy/",
    ]
    return cloudflare + azure + cloudarmor + aws + modsec

def get_hostnames_json():
    cloudflare = [
    "https://waf2.akhavani.net/laravel/api/store",
    "https://waf2.akhavani.net/spring/json",
    "https://waf2.akhavani.net/flask/json",
    "https://waf2.akhavani.net/fastapi/json",
    "https://waf2.akhavani.net/express/json",
    "https://waf2.akhavani.net/gin/json",
    "https://waf2.akhavani.net/node-json/"
    ]
    cloudarmor = [
    "http://34.111.13.62:80/laravel/api/store",
    "http://34.111.13.62:80/spring/json",
    "http://34.111.13.62:80/flask/json",
    "http://34.111.13.62:80/fastapi/json",
    "http://34.111.13.62:80/express/json",
    "http://34.111.13.62:80/gin/json",
    "http://34.111.13.62:80/node-json/",
    ]
    aws = [
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8630/api/store",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8631/json",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8632/json",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8633/json",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8634/json",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8635/json",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8621",
    ]
    azure = [
    "http://52.249.221.180:8630/api/store",
    "http://52.249.221.180:8631/json",
    "http://52.249.221.180:8632/json",
    "http://52.249.221.180:8633/json",
    "http://52.249.221.180:8634/json",
    "http://52.249.221.180:8635/json",
    "http://52.249.221.180:8621/",
    ]
    modsec = [
    "http://18.116.50.97:80/laravel/api/store",
    "http://18.116.50.97:80/spring/json",
    "http://18.116.50.97:80/flask/json",
    "http://18.116.50.97:80/fastapi/json",
    "http://18.116.50.97:80/express/json",
    "http://18.116.50.97:80/gin/json",
    "http://18.116.50.97:80/node-json/",
    ]
    return cloudflare + azure + cloudarmor + aws + modsec

def get_hostnames_xml():
    cloudflare = [
    "https://waf2.akhavani.net/laravel/api/storexml",
    "https://waf2.akhavani.net/spring/xml",
    "https://waf2.akhavani.net/flask/xml",
    "https://waf2.akhavani.net/fastapi/xml",
    "https://waf2.akhavani.net/express/xml",
    "https://waf2.akhavani.net/gin/xml",
    ]
    cloudarmor = [
    "https://34.111.13.62:80/laravel/api/storexml",
    "https://34.111.13.62:80/spring/xml",
    "https://34.111.13.62:80/flask/xml",
    "https://34.111.13.62:80/fastapi/xml",
    "https://34.111.13.62:80/express/xml",
    "https://34.111.13.62:80/gin/xml",
    ]
    aws = [
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8630/api/storexml",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8631/xml",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8632/xml",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8633/xml",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8634/xml",
    "http://alb-1117388808.us-east-2.elb.amazonaws.com:8635/xml",
    ]
    azure = [
    "http://52.249.221.180:8630/api/storexml",
    "http://52.249.221.180:8631/xml",
    "http://52.249.221.180:8632/xml",
    "http://52.249.221.180:8633/xml",
    "http://52.249.221.180:8634/xml",
    "http://52.249.221.180:8635/xml",
    ]
    modsec = [
    "http://18.116.50.97:80/laravel/api/storexml",
    "http://18.116.50.97:80/spring/xml",
    "http://18.116.50.97:80/flask/xml",
    "http://18.116.50.97:80/fastapi/xml",
    "http://18.116.50.97:80/express/xml",
    "http://18.116.50.97:80/gin/xml",
    ]
    return cloudflare + azure + cloudarmor + aws + modsec

