import contextlib
from base64 import b64encode
from flask import Request
from typing import Any


def http_retrieve_parameters(url: str) -> dict[str, str]:
    """
    Retrieve and return the parameters in the query string of *url*.

    :param url: the url to retrieve parameters from
    :return: the extracted parameters, or an empty *dict* if no parameters were found
    """
    # initialize the return variable
    result: dict[str, str] = {}

    # retrieve the parameters
    pos: int = url.find("?")
    if pos > 0:
        params: list[str] = url[pos + 1:].split(sep="&")
        for param in params:
            key: str = param.split("=")[0]
            value: str = param.split("=")[1]
            result[key] = value

    return result


def http_get_parameter(request: Request,
                       param: str,
                       sources: tuple[str, str, str] = ("body", "form", "query")) -> Any:
    """
    Obtain the *request*'s input parameter named *param*.

    The following origins are inspected, in the sequence defined by *sources*, defaulting to:
      - *body*: key/value pairs in a *JSON* structure in the request's body
      - *form*: data elements in a HTML form
      - *query*: parameters in the URL's query string

    The first occurrence of *param* found is returned. If *sources* is provided, only the
    origins specified therein (*body*, *form*, and *query*) are inspected.

    :param request: the *Request* object
    :param sources: the sequence of origins to inspect (defaults to *['body', 'form', 'query']*)
    :param param: name of parameter to retrieve
    :return: the parameter's value, or *None* if not found
    """
    params: dict[str, Any] = http_get_parameters(request=request,
                                                 sources=sources)
    return (params or {}).get(param)


def http_get_parameters(request: Request,
                        sources: tuple[str, str, str] = ("body", "form", "query")) -> Any:
    """
    Obtain the *request*'s input parameters.

    The following origins are inspected, in the sequence defined by *sources*, defaulting to:
      - *body*: key/value pairs in a *JSON* structure in the request's body
      - *form*: data elements in a HTML form
      - *query*: parameters in the URL's query string

    The first occurrence of each parameter found is returned. If *sources* is provided, only the
    origins specified therein (*body*, *form*, and *query*) are inspected.

    :param request: the *Request* object
    :param sources: the sequence of origins to inspect (defaults to *['body', 'form', 'query']*)
    :return: *dict* containing the input parameters (empty *dict*, if no input data exists)
    """
    # initialize the return variable
    result: dict[str, Any] = {}

    for source in reversed(sources or []):
        match source:
            case "query":
                # retrieve parameters from URL query
                result.update(request.values)
            case "body":
                # retrieve parameters from JSON data in body
                with contextlib.suppress(Exception):
                    result.update(request.get_json())
            case "form":
                # obtain parameters from form
                result.update(request.form)

    return result


def http_basic_auth_header(uname: str,
                           pwd: str,
                           header: dict[str, Any] = None) -> dict[str, Any]:
    """
    Add to *header* the HTTP Basic Authorization snippet.

    If *header* is not provided, a new *dict* is created.
    For convenience, the modified, or newly created, *dict* is returned.

    :param uname: the username to use
    :param pwd: the password to use
    :param header: the optional header to add the Basic Authorization to
    :return: header with Basic Authorization data
    """
    # initialize the return variable
    result: dict[str, Any] = header if isinstance(header, dict) else {}

    enc_bytes: bytes = b64encode(f"{uname}:{pwd}".encode())
    result["Authorization"] = f"Basic {enc_bytes.decode()}"

    return result


def http_bearer_auth_header(token: str | bytes,
                            header: dict[str, Any] = None) -> dict[str, Any]:
    """
    Add to *header* the HTTP Bearer Authorization snippet.

    If *header* is not provided, a new *dict* is created.
    For convenience, the modified, or newly created, *dict* is returned.

    :param token: the token to use
    :param header: the optional header to add the Bearer Authorization to
    :return: header with Basic Authorization data
    """
    # initialize the return variable
    result: dict[str, Any] = header if isinstance(header, dict) else {}

    if isinstance(token, bytes):
        token = token.decode()
    result["Authorization"] = f"Bearer {token}"

    return result
