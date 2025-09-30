def get_hostnames_multipart():
    waf1 = [
        "https://waf1.mytargetwaf.net/laravel/api/store",
        "https://waf1.mytargetwaf.net/spring/multipart",
        "https://waf1.mytargetwaf.net/flask/multipart",
        "https://waf1.mytargetwaf.net/fastapi/multipart",
        "https://waf1.mytargetwaf.net/express/multipart",
        "https://waf1.mytargetwaf.net/gin/multipart",
        "https://waf1.mytargetwaf.net/node-busboy/",
    ]
    waf2 = [
        "https://waf2.mytargetwaf.net/laravel/api/store",
        "https://waf2.mytargetwaf.net/spring/multipart",
        "https://waf2.mytargetwaf.net/flask/multipart",
        "https://waf2.mytargetwaf.net/fastapi/multipart",
        "https://waf2.mytargetwaf.net/express/multipart",
        "https://waf2.mytargetwaf.net/gin/multipart",
        "https://waf2.mytargetwaf.net/node-busboy/",
    ]
    return waf1 + waf2


def get_hostnames_json():
    waf1 = [
        "https://waf1.mytargetwaf.net/laravel/api/store",
        "https://waf1.mytargetwaf.net/spring/json",
        "https://waf1.mytargetwaf.net/flask/json",
        "https://waf1.mytargetwaf.net/fastapi/json",
        "https://waf1.mytargetwaf.net/express/json",
        "https://waf1.mytargetwaf.net/gin/json",
        "https://waf1.mytargetwaf.net/node-json/",
    ]
    waf2 = [
        "https://waf2.mytargetwaf.net/laravel/api/store",
        "https://waf2.mytargetwaf.net/spring/json",
        "https://waf2.mytargetwaf.net/flask/json",
        "https://waf2.mytargetwaf.net/fastapi/json",
        "https://waf2.mytargetwaf.net/express/json",
        "https://waf2.mytargetwaf.net/gin/json",
        "https://waf2.mytargetwaf.net/node-json/",
    ]
    return waf1 + waf2


def get_hostnames_xml():
    waf1 = [
        "https://waf1.mytargetwaf.net/laravel/api/storexml",
        "https://waf1.mytargetwaf.net/spring/xml",
        "https://waf1.mytargetwaf.net/flask/xml",
        "https://waf1.mytargetwaf.net/fastapi/xml",
        "https://waf1.mytargetwaf.net/express/xml",
        "https://waf1.mytargetwaf.net/gin/xml",
    ]
    waf1 = [
        "https://waf2.mytargetwaf.net/laravel/api/storexml",
        "https://waf2.mytargetwaf.net/spring/xml",
        "https://waf2.mytargetwaf.net/flask/xml",
        "https://waf2.mytargetwaf.net/fastapi/xml",
        "https://waf2.mytargetwaf.net/express/xml",
        "https://waf2.mytargetwaf.net/gin/xml",
    ]
    return waf1 + waf2
