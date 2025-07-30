import pytest
from httpinsert.insertion_points import find_insertion_points
from httpinsert.location import Locations
from .conftest import make_request  # Adjust if your fixture is elsewhere


def test_method_location_points():
    req = make_request(method="POST")
    points = find_insertion_points(req, location="Method")
    assert any(p.key.lower() == "post" for p in points)
    assert any(p.value.lower() == "post" for p in points)


def test_path_location_points():
    req = make_request(url="http://example.com/api/test")
    points = find_insertion_points(req, location="Path",default=False)
    assert any("api" in p.value or "test" in p.value for p in points)


def test_version_location_points():
    req = make_request()
    req.version = "HTTP/1.1"
    points = find_insertion_points(req, location="Version")
    assert any("HTTP/1.1" in p.value for p in points)


def test_query_location_points():
    req = make_request(url="http://example.com/page?user=admin&role=editor")
    points = find_insertion_points(req, location="Query")
    kvs = [(p.key, p.value) for p in points if not p.full]
    assert ("user", "admin") in kvs
    assert ("role", "editor") in kvs


def test_headers_location_points():
    req = make_request(headers={
        "X-Custom": "test123",
        "User-Agent": "pytest-agent"
    })
    points = find_insertion_points(req, location="Headers")
    keys = [p.key.lower() for p in points]
    assert "x-custom" in keys
    assert "user-agent" in keys


def test_cookies_location_points():
    req = make_request(headers={"Cookie": "token=abc; id=42"})
    points = find_insertion_points(req, location="Headers")
    kvs = [(p.key, p.value) for p in points]
    assert ("token", "abc") in kvs
    assert ("id", "42") in kvs


def test_body_location_points():
    req = make_request(body=b"key1=value1&key2=value2")
    points = find_insertion_points(req, location="Body")
    keys = [p.key for p in points if not p.full]
    assert b"key1" in keys and b"key2" in keys


def test_manual_location_returns_nothing_by_default():
    req = make_request()
    points = find_insertion_points(req, location="Manual")
    # If manual requires special config, it should return empty
    assert len(points) == 0 or all(p.full for p in points)

