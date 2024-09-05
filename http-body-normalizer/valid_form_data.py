# from Tornado (https://github.com/tornadoweb/tornado/blob/a30a606a9d8288a2f2590032c02e54e6b9a7eb10/tornado/test/httputil_test.py#L98)

b'POST / HTTP/1.1\r\nHost: whatever\r\nContent-Type: multipart/form-data; boundary="1234"\r\nContent-Length: 88\r\n\r\n--1234\r\nContent-Disposition: form-data; name="files"; filename="ab.txt"\r\n\r\nFoo\r\n--1234--'

b'POST / HTTP/1.1\r\nHost: whatever\r\nContent-Type: multipart/form-data; boundary="1234"\r\nContent-Length: 84\r\n\r\n--1234\r\nContent-Disposition: form-data; name=files; filename=ab.txt\r\n\r\nFoo\r\n--1234--'

# From MDN (https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Disposition)

b'POST /test.html HTTP/1.1\r\nHost: example.org\r\nContent-Type: multipart/form-data;boundary="boundary"\r\nContent-Length: 174\r\n\r\n--boundary\r\nContent-Disposition: form-data; name="field1"\r\n\r\nvalue1\r\n--boundary\r\nContent-Disposition: form-data; name="field2"; filename="example.txt"\r\n\r\nvalue2\r\n--boundary--'

# From RStudio (https://github.com/rstudio/rstudio/blob/6cc3777d4042609c45dea6525f4652d4ac3b9d6e/src/cpp/core/http/RequestParserTests.cpp#L50)

b'POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: multipart/form-data; boundary=boundary\r\nContent-Length: 220\r\n\r\n--boundary\r\nContent-Disposition: form-data; name="field1"\r\n\r\nvalue1\r\n--boundary\r\nContent-Disposition: form-data; name="field2"; filename="example.txt"\r\nContent-Type: text/plain\r\n\r\nThis is a simple text file\r\n--boundary--'

b'POST /test HTTP/1.1\r\nHost: foo.example\r\nContent-Type: multipart/form-data; boundary=boundary\r\nContent-Length: 217\r\n\r\n--boundary\r\nContent-Disposition: form-data; name="field1"\r\n\r\nvalue1\r\n--boundary\r\nContent-Disposition: form-data; name="field2"; filename="example.txt"\r\nContent-Type: application/octet-stream\r\n\r\nfileBytes\r\n--boundary--'

# From SO (https://stackoverflow.com/questions/4238809/example-of-multipart-form-data)

b'POST / HTTP/1.1\r\nHost: localhost:8000\r\nUser-Agent: Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:29.0) Gecko/20100101 Firefox/29.0\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nAccept-Language: en-US,en;q=0.5\r\nAccept-Encoding: gzip, deflate\r\nCookie: __atuvc=34%7C7; permanent=0; _gitlab_session=226ad8a0be43681acf38c2fab9497240; __profilin=p%3Dt; request_method=GET\r\nConnection: keep-alive\r\nContent-Type: multipart/form-data; boundary=---------------------------9051914041544843365972754266\r\nContent-Length: 554\r\n\r\n-----------------------------9051914041544843365972754266\r\nContent-Disposition: form-data; name="text"\r\n\r\ntext default\r\n-----------------------------9051914041544843365972754266\r\nContent-Disposition: form-data; name="file1"; filename="a.txt"\r\nContent-Type: text/plain\r\n\r\nContent of a.txt.\r\n\r\n-----------------------------9051914041544843365972754266\r\nContent-Disposition: form-data; name="file2"; filename="a.html"\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><title>Content of a.html.</title>\r\n\r\n-----------------------------9051914041544843365972754266--'

b'POST / HTTP/1.1\r\nHOST: host.example.com\r\nCookie: some_cookies...\r\nConnection: Keep-Alive\r\nContent-Type: multipart/form-data; boundary=12345\r\nContent-Length: 419\r\n\r\n--12345\r\nContent-Disposition: form-data; name="sometext"\r\n\r\nsome text that you wrote in your html form ...\r\n--12345\r\nContent-Disposition: form-data; name="name_of_post_request"; filename="filename.xyz"\r\n\r\ncontent of filename.xyz that you upload in your form with input[type=file]\r\n--12345\r\nContent-Disposition: form-data; name="image"; filename="picture_of_sunset.jpg"\r\n\r\ncontent of picture_of_sunset.jpg ...\r\n--12345--'

# From W3 (https://www.w3.org/TR/html401/interact/forms.html#h-17.13.4.2)

b'POST / HTTP/1.1\r\nHost: whatever\r\nContent-Length: 218\r\nContent-Type: multipart/form-data; boundary=AaB03x\r\n\r\n--AaB03x\r\nContent-Disposition: form-data; name="submit-name"\r\n\r\nLarry\r\n--AaB03x\r\nContent-Disposition: form-data; name="files"; filename="file1.txt"\r\nContent-Type: text/plain\r\n\r\n... contents of file1.txt ...\r\n--AaB03x--'

# From multiparty (https://github.com/pillarjs/multiparty/blob/master/test/test.js)

b'POST /upload HTTP/1.1\r\nHost: localhost\r\nContent-Length: 288\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\n\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="title"\r\n\r\nfoofoo\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="upload"; filename="blah1.txt"\r\nContent-Type: text/plain\r\n\r\nhi1\r\n\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF--\r\n'

b'POST /upload HTTP/1.1\r\nHost: localhost\r\nContent-Length: 238\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\n\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="title"\r\n\r\nfoofoo\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="text"\r\n\r\nhi1\r\n\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF--\r\n'

b'POST /upload HTTP/1.1\r\nHost: localhost\r\nContent-Length: 726\r\nContent-Type: multipart/form-data; boundary=----WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\n\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="title"\r\n\r\nfoofoo\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="upload"; filename="blah1.txt"\r\nContent-Type: text/plain\r\n\r\nhi1\r\n\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="upload"; filename="blah2.txt"\r\nContent-Type: text/plain\r\n\r\nhi2\r\n\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="upload"; filename="blah3.txt"\r\nContent-Type: text/plain\r\n\r\nhi3\r\n\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="upload"; filename="blah4.txt"\r\nContent-Type: text/plain\r\n\r\nhi4\r\n\r\n------WebKitFormBoundaryvfUZhxgsZDO7FXLF--\r\n'

b'POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 186\r\nContent-Type: multipart/form-data; boundary=--WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\n\r\n----WebKitFormBoundaryvfUZhxgsZDO7FXLF\r\nContent-Disposition: form-data; name="upload"; filename="blah1.txt"\r\nContent-Type: plain/text\r\n\r\nhi1\r\n'

b'POST / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\nContent-Type: multipart/form-data; boundary=foo\r\nTransfer-Encoding: chunked\r\n\r\n7\r\n--foo\r\n\r\n43\r\nContent-Disposition: form-data; name="file"; filename="plain.txt"\r\n\r\n12\r\n\r\nsome text here\r\n\r\n9\r\n--foo--\r\n\r\n0\r\n\r\n'

b'POST / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\nContent-Type: multipart/form-data; boundary=foo\r\nTransfer-Encoding: chunked\r\n\r\n7\r\n--foo\r\n\r\n2D\r\nContent-Disposition: form-data; name="data"\r\n\r\n12\r\n\r\nsome text here\r\n\r\n7\r\n--foo--\r\n2\r\n\r\n\r\n0\r\n\r\n'

b'POST / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\nContent-Type: multipart/form-data; boundary=foo\r\nTransfer-Encoding: chunked\r\n\r\n7\r\n--foo\r\n\r\n43\r\nContent-Disposition: form-data; name="file"; filename="plain.txt"\r\n\r\n12\r\n\r\nsome text here\r\n\r\n7\r\n--foo--\r\n2\r\n\r\n\r\n0\r\n\r\n'

b'POST / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\nContent-Type: multipart/form-data; boundary=foo\r\nTransfer-Encoding: chunked\r\n\r\n7\r\n--foo\r\n\r\n46\r\nContent-Disposition: form-data; name="file"; filename="plain.txt"\r\n:\r\n\r\n12\r\n\r\nsome text here\r\n\r\n9\r\n--foo--\r\n\r\n0\r\n\r\n'
