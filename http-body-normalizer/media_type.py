import re
from typing import Final, TypeGuard
from dataclasses import dataclass

from mime_type import MIME_TOP_LEVEL_TYPES, MIME_SUBTYPES


# RFC 5234
# ALPHA          =  %x41-5A / %x61-7A
_ALPHA_RE: Final[str] = r"[A-Za-z]"

# RFC 5234
# DIGIT          =  %x30-39
_DIGIT_RE: Final[str] = r"[0-9]"

# RFC 9110
#  tchar          = "!" / "#" / "$" / "%" / "&" / "'" / "*"
#                 / "+" / "-" / "." / "^" / "_" / "`" / "|" / "~"
#                 / DIGIT / ALPHA
_TCHAR_RE: Final[str] = rf"(?:[!#$%&'*+\-.^_`|~]|{_DIGIT_RE}|{_ALPHA_RE})"

# RFC 9110
# token          = 1*tchar
_TOKEN_RE: Final[str] = rf"(?:{_TCHAR_RE}+)"

# RFC 9110
# qdtext         = HTAB / SP / %x21 / %x23-5B / %x5D-7E / obs-text
_QDTEXT_RE: Final[str] = rf"[\t \x21\x23-\x5b\x5d-\x7e]"

# RFC 5234
# VCHAR          =  %x21-7E
_VCHAR_RE: Final[str] = r"[\x21-\x7e]"

# RFC 9110
# quoted-pair    = "\" ( HTAB / SP / VCHAR / obs-text )
_QUOTED_PAIR_RE: Final[str] = rf"(?:\\(?:[\t ]|{_VCHAR_RE}))"

# RFC 9110
# quoted-string  = DQUOTE *( qdtext / quoted-pair ) DQUOTE
_QUOTED_STRING_RE: Final[str] = rf'(?:"(?:{_QDTEXT_RE}|{_QUOTED_PAIR_RE})*")'

# RFC 9110
# parameter-value = ( token / quoted-string )
_PARAMETER_VALUE_RE: Final[str] = rf"(?:{_TOKEN_RE}|{_QUOTED_STRING_RE})"

# RFC 9110
#  OWS            = *( SP / HTAB )
_OWS_RE: Final[str] = r"(?:[ \t]*)"

# RFC 9110
#  parameter-name  = token
_PARAMETER_NAME_RE: Final[str] = _TOKEN_RE

# RFC 9110 (a little modified)
# parameter       = parameter-name "=" parameter-value
_PARAMETER_RE: Final[str] = rf"(?:{_OWS_RE};{_OWS_RE}(?:({_PARAMETER_NAME_RE})=({_PARAMETER_VALUE_RE}))?)"

# RFC 9110 (a little modified)
# parameters      = *( OWS ";" OWS [ parameter ] )
_PARAMETERS_RE: Final[str] = rf"(?:(?:{_PARAMETER_RE})*)"

# RFC 9110
# type       = token
_TYPE_RE: Final[str] = _TOKEN_RE

# RFC 9110
# subtype    = token
_SUBTYPE_RE: Final[str] = _TOKEN_RE

# RFC 9110
# media-type = type "/" subtype parameters
_MEDIA_TYPE_RE: Final[str] = (
    rf"(?:(?P<type>{_TYPE_RE})/(?P<subtype>{_SUBTYPE_RE})(?P<parameters>{_PARAMETERS_RE}))"
)

_PARAMETER_PAT: Final[re.Pattern[bytes]] = re.compile(_PARAMETER_RE.encode("ascii"))
_MEDIA_TYPE_PAT: Final[re.Pattern[bytes]] = re.compile(_MEDIA_TYPE_RE.encode("ascii"))


def is_bytes_list(l: list) -> TypeGuard[list[bytes]]:
    return all(isinstance(thing, bytes) for thing in l)


_MAX_CONTINUATION_INDEX: Final[int] = 100  # Picked arbitrarily. Feel free to increase if necessary.


@dataclass
class MediaType:
    type_: bytes
    subtype: bytes
    parameters: dict[bytes, bytes]

    def __post_init__(self):
        if self.type_ not in MIME_TOP_LEVEL_TYPES:
            raise ValueError("Unrecognized MIME type.")
        if self.subtype not in MIME_SUBTYPES[self.type_]:
            raise ValueError("Unrecognized MIME subtype.")

    def serialize(self) -> bytes:
        return self.type_ + b"/" + self.subtype + b"".join(b"; " + k + b"=" + v for k, v in self.parameters.items())


def parse_media_type_parameters(data: bytes) -> dict[bytes, bytes]:
    raw_params: list[tuple[bytes, bytes]] = []
    while len(data) > 0:
        m = re.match(_PARAMETER_PAT, data)
        assert m is not None
        raw_params.append((m[1], m[2]))
        data = data[m.end() :]

    # Parse RFC 2231-style continuations in parameters.
    params_with_continuation: dict[bytes, list[bytes | None] | bytes] = {}
    for raw_key, raw_value in raw_params:
        if raw_value.startswith(b'"') and raw_value.endswith(b'"'):
            raw_value = raw_value[1:-1]
        # Note: RFC 2231 requires that the first digit be nonzero. We relax this on the input side, but not on the output side.
        m = re.fullmatch(rb"\A(?P<key>.*)\*(?P<index>\d+)\Z", raw_key)
        if m is not None:
            key: bytes = m["key"]
            index: int = int(m["index"])

            if key not in params_with_continuation:
                params_with_continuation[key] = []

            values: list[bytes | None] | bytes = params_with_continuation[key]
            if isinstance(values, bytes):
                raise ValueError("Duplicate parameter! (once with continuation, once without)")
            if index > _MAX_CONTINUATION_INDEX:
                raise ValueError("Continuation index too large!")
            # Extend the list to match the index, if necessary
            while len(values) < index + 1:
                values.append(None)
            if values[index] is not None:
                raise ValueError("Repeated continuation index!")
            values[index] = raw_value
        else:
            if raw_key in params_with_continuation:
                raise ValueError("Duplicate parameter!")
            params_with_continuation[raw_key] = raw_value

    params: dict[bytes, bytes] = {}
    for k, v in params_with_continuation.items():
        if isinstance(v, bytes):
            params[k] = v
        elif isinstance(v, list):
            if not is_bytes_list(v):
                raise ValueError("Missing continuation index!")
            params[k] = b"".join(v)

    return params


def parse_media_type(media_type: bytes) -> MediaType:
    """
    Takes as input the value of a Content-Type header.
    Spits out the type, subtype, and a list of key:value pairs corresponding to the parameters.
    """

    m: re.Match[bytes] | None = re.fullmatch(_MEDIA_TYPE_PAT, media_type)
    if m is None:
        raise ValueError("Media type does not parse!")

    # Case-insensitivity specified in RFC 9110 8.3.1
    type_: bytes = m["type"].lower()
    subtype: bytes = m["subtype"].lower()
    parameter_bytes: bytes = m["parameters"]

    return MediaType(type_, subtype, parse_media_type_parameters(parameter_bytes))

# RFC 5234
# CRLF        =  %d13.10
_CRLF_RE: Final[str] = r"(?:\r\n)"

# RFC 9110
# field-vchar    = VCHAR / obs-text
_FIELD_VCHAR_RE: Final[str] = _VCHAR_RE

# RFC 9110
# field-content  = field-vchar
#                  [ 1*( SP / HTAB / field-vchar ) field-vchar ]
_FIELD_CONTENT_RE: Final[str] = rf"(?:{_FIELD_VCHAR_RE}(?:(?:[ \t]|{_FIELD_VCHAR_RE})+{_FIELD_VCHAR_RE})?)"

# RFC 9110
# field-value    = *field-content
_FIELD_VALUE_RE: Final[str] = rf"(?:{_FIELD_CONTENT_RE}*)"

# RFC 9110
# field-name     = token
_FIELD_NAME_RE: Final[str] = _TOKEN_RE

# RFC 9112
# field-line   = field-name ":" OWS field-value OWS
_FIELD_LINE_RE: Final[str] = rf"(?:(?P<name>{_FIELD_NAME_RE}):{_OWS_RE}(?P<value>{_FIELD_VALUE_RE}){_OWS_RE})"

_FIELD_LINE_PAT: re.Pattern[bytes] = re.compile(_FIELD_LINE_RE.encode("ascii"))

def parse_header(data: bytes) -> tuple[tuple[bytes, bytes], bytes]:
    """
    Takes as input a byte string that begins with an HTTP header.
    Parses the header, and returns the remaining data.
    """
    m: re.Match[bytes] | None = re.match(_FIELD_LINE_PAT, data)
    if m is None:
        raise ValueError("Invalid header!")
    return (m["name"], m["value"]), data[m.end():]


def parse_headers(data: bytes) -> tuple[dict[bytes, bytes], bytes]:
    headers: dict[bytes, bytes] = {}
    while True:
        try:
            (key, value), data = parse_header(data)
        except ValueError:
            break
        key = key.lower()
        value = value.lower()
        if key in headers:
            raise ValueError("Duplicate header!")
        headers[key] = value
        if len(data) < 2 or data[:2] != b"\r\n":
            raise ValueError("Header missing CRLF!")
        data = data[2:]
    if len(data) < 2 or data[:2] != b"\r\n":
        raise ValueError("Missing CRLF after headers!")
    return headers, data[2:]


@dataclass
class MultipartContentDisposition:
    name: bytes | None = None
    filename: bytes | None = None

    def serialize(self) -> bytes:
        result: bytes = b'form-data'
        if self.name is not None:
            result += b'; name="' + self.name + b'"'
        if self.filename is not None:
            result += b'; filename="' + self.filename + b'"'
        return result

def parse_multipart_content_disposition(data: bytes) -> MultipartContentDisposition:
    if not data.startswith(b"form-data"):
        raise ValueError("Unrecognized Content-Disposition!")
    data = data[len(b"form-data"):]

    params: dict[bytes, bytes] = parse_media_type_parameters(data)
    name: bytes | None = params.get(b"name")
    filename: bytes | None = params.get(b"filename")
    return MultipartContentDisposition(name, filename)

        

@dataclass
class MultipartSubpart:
    boundary: bytes
    content_disposition: MultipartContentDisposition
    content_type: MediaType
    data: bytes

    def __post_init__(self):
        if b"\r\n--" + self.boundary in self.data:
            raise ValueError(f"Boundary present in multipart data: {self.data!r}")

    def serialize(self) -> bytes:
        result: bytes = b""
        result += b"--" + self.boundary + b"\r\n"
        result += b"Content-Type: " + self.content_type.serialize() + b"\r\n"
        result += b"Content-Disposition: " + self.content_disposition.serialize() + b"\r\n"
        result += b"\r\n"
        result += self.data
        return result

# RFC 5322
# text            =   %d1-9 /            ; Characters excluding CR
#                     %d11 /             ;  and LF
#                     %d12 /
#                     %d14-127
_TEXT_RE: Final[str] = r"[\x01-\x09\x0b\x0c\x0e-\x7f]"

# RFC 2046
# discard-text := *(*text CRLF)
_DISCARD_TEXT_RE: Final[str] = rf"(?:(?:{_TEXT_RE}*{_CRLF_RE})*)"

# RFC 2046
# preamble := discard-text
_PREAMBLE_RE: Final[str] = _DISCARD_TEXT_RE

# RFC 822
# LWSP-char   =  SPACE / HTAB
_LWSP_CHAR_RE: Final[str] = r"[ \t]"

# RFC 2046
# transport-padding := *LWSP-char
_TRANSPORT_PADDING_RE: Final[str] = rf"(?:{_LWSP_CHAR_RE}*)"

# RFC 2046
# OCTET := <any 0-255 octet value>
_OCTET_RE: Final[str] = rf"[\x00-\xff]"

# RFC 2046
# epilogue := discard-text
_EPILOGUE_RE: Final[str] = _DISCARD_TEXT_RE


def make_dash_boundary_re(boundary: str) -> str:
    # RFC 2046
    # dash-boundary := "--" boundary
    return rf"(?:--{boundary})"

def make_multipart_body_prefix_re(boundary: str) -> str:
    dash_boundary_re: str = make_dash_boundary_re(boundary)

    # RFC 2046
    # multipart-body := [preamble CRLF]
    #                   dash-boundary transport-padding CRLF
    #                   body-part *encapsulation
    #                   close-delimiter transport-padding
    #                   [CRLF epilogue]
    return rf"(?:(?:{_PREAMBLE_RE}{_CRLF_RE})?{dash_boundary_re}{_TRANSPORT_PADDING_RE}{_CRLF_RE})"

def make_multipart_body_suffix_re(boundary: str) -> str:
    dash_boundary_re: str = make_dash_boundary_re(boundary)

    # RFC 2046
    # delimiter := CRLF dash-boundary
    delimiter_re: str = rf"(?:{_CRLF_RE}{dash_boundary_re})"

    # RFC 2046
    # close-delimiter := delimiter "--"
    close_delimiter_re: str = rf"(?:{delimiter_re}--)"

    # RFC 2046
    # multipart-body := [preamble CRLF]
    #                   dash-boundary transport-padding CRLF
    #                   body-part *encapsulation
    #                   close-delimiter transport-padding
    #                   [CRLF epilogue]
    return rf"(?:{close_delimiter_re}{_TRANSPORT_PADDING_RE}(?:{_CRLF_RE}{_EPILOGUE_RE}))"

def parse_multipart_subpart(boundary: str, data: bytes) -> MultipartSubpart:
    headers, data = parse_headers(data)

    if b"content-disposition" not in headers:
        raise ValueError("Chunk is missing Content-Disposition!")
    content_disposition: MultipartContentDisposition = parse_multipart_content_disposition(headers[b"content-disposition"])

    content_type: MediaType
    if b"content-type" in headers:
        content_type = parse_media_type(headers[b"content-type"])
    else:
        content_type = MediaType(b"text", b"plain", {})

    return MultipartSubpart(boundary.encode("ascii"), content_disposition, content_type, data)


def parse_multipart_body(boundary: str, data: bytes) -> list[MultipartSubpart]:
    """
    Parses a multipart body. Returns the pieces of the multipart message, and the remaining unparsed bytes.
    """
    prefix_re: bytes = make_multipart_body_prefix_re(boundary).encode("ascii")
    m: re.Match[bytes] | None = re.match(prefix_re, data)
    
    if m is None:
        raise ValueError("Couldn't parse multipart body prefix!")
    data = data[m.end():]
    
    raw_subparts: list[bytes] = data.split(b"\r\n--" + boundary.encode("ascii"))
    raw_subparts[0] = b"\r\n" + raw_subparts[0] # First chunk won't have CRLF prefix, so add one on
    result: list[MultipartSubpart] = []
    for subpart in raw_subparts:
        if subpart in (b"--", b"--\r\n"):
            break
        if not subpart.startswith(b"\r\n"):
            raise ValueError(f"Missing CRLF in {subpart!r}!")
        subpart = subpart[len(b"\r\n"):]
        result.append(parse_multipart_subpart(boundary, subpart))

    return result


def normalize_multipart_body(boundary: str, data: bytes) -> bytes:
    return b"\r\n".join(map(MultipartSubpart.serialize, parse_multipart_body(boundary, data))) + b"\r\n--" + boundary.encode("ascii") + b"--"
