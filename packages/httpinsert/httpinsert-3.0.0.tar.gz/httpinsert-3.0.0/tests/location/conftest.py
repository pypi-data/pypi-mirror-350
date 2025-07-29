import pytest
from httpinsert.request import Request
from httpinsert.insertion_points import find_insertion_points

def make_request(method="GET", url="http://example.com/path?foo=bar", headers=None, body=None):
    headers = headers or {
        "Host": "example.com",
        "User-Agent": "pytest",
        "Cookie": "sessionid=abc123",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    return Request(method=method, url=url, headers=headers, body=body or b"username=admin&password=1234")

