server_headers = {
    # waf1
    "https://waf1.mytargetwaf.net/laravel/api/store": "parser: waf1-laravel",
    "https://waf1.mytargetwaf.net/spring/multipart": "parser: waf1-spring",
    "https://waf1.mytargetwaf.net/flask/multipart": "parser: waf1-flask",
    "https://waf1.mytargetwaf.net/fastapi/multipart": "parser: waf1-fastapi",
    "https://waf1.mytargetwaf.net/express/multipart": "parser: waf1-express",
    "https://waf1.mytargetwaf.net/gin/multipart": "parser: waf1-gogin",
    "https://waf1.mytargetwaf.net/node-busboy/": "parser: waf1-busboy",
    # waf2
    "https://waf2.mytargetwaf.net/laravel/api/store": "parser: waf2-laravel",
    "https://waf2.mytargetwaf.net/spring/multipart": "parser: waf2-spring",
    "https://waf2.mytargetwaf.net/flask/multipart": "parser: waf2-flask",
    "https://waf2.mytargetwaf.net/fastapi/multipart": "parser: waf2-fastapi",
    "https://waf2.mytargetwaf.net/express/multipart": "parser: waf2-express",
    "https://waf2.mytargetwaf.net/gin/multipart": "parser: waf2-gogin",
    "https://waf2.mytargetwaf.net/node-busboy/": "parser: waf2-busboy",
}
return server_headers
