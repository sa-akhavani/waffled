import aiohttp
import aiohttp.web
from aiohttp.web_protocol import RequestPayloadError
from aiohttp.abc import CIMultiDict
from yarl import URL

from media_type import parse_media_type, normalize_multipart_body, MediaType

# Change this:
_HOST: str = "localhost"
# And this:
_PORT: int = 8000

async def respond(request) -> aiohttp.web.Response:
    try:
        body: bytes = await request.content.read()
    except RequestPayloadError:
        return aiohttp.web.Response(status=400, reason="Bad message body.")

    headers: CIMultiDict = CIMultiDict()
    headers.extend(request.headers)

    if "Content-Type" in request.headers:
        orig_ct: str = request.headers["Content-Type"]
        if not orig_ct.isascii():
            return aiohttp.web.Response(status=400, reason="Non-ASCII bytes in Content-Type.")
        try:
            media_type: MediaType = parse_media_type(orig_ct.encode("ascii"))
        except ValueError:
            return aiohttp.web.Response(status=400, reason="Bad Content-Type.")

        raw_boundary: bytes | None = media_type.parameters.get(b"boundary")
        if raw_boundary is None:
            return aiohttp.web.Response(status=400, reason="Missing boundary parameter!")
        if not raw_boundary.isascii():
            return aiohttp.web.Response(status=400, reason="Boundary is not ASCII!")

        for k, v in media_type.parameters.items():
            if k != b"boundary":
                del media_type.parameters[k]

        headers["Content-Type"] = media_type.serialize().decode("ascii")

        if media_type.type_ == b"multipart" and media_type.subtype == b"form-data":
            try:
                body = normalize_multipart_body(raw_boundary.decode("ascii"), body)
            except ValueError:
                return aiohttp.web.Response(status=400, reason="Malformed multipart body.")

    try:
        url: URL = request.url.with_host(_HOST).with_port(_PORT)
    except ValueError:
        return aiohttp.web.Response(status=400, reason="Invalid URL.")

    async with aiohttp.ClientSession() as session:
        async with session.request(
            method=request.method,
            url=url,
            headers=headers,
            data=body,
        ) as response:
            return aiohttp.web.Response(
                body=(await response.read()),
                status=response.status,
                headers=response.headers,
            )
    return aiohttp.web.Response(status=500, reason="This should never happen!")
        

app = aiohttp.web.Application()
app.add_routes([aiohttp.web.route("*", "/{unused_required_name:.*}", respond)])

aiohttp.web.run_app(app, port=8999)
