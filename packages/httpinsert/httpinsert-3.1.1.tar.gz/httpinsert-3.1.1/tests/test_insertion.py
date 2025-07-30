import pytest
from httpinsert.insertion_points import Insertion,InsertionPoint
from unittest.mock import Mock

class DummyLocation:
    def insert_payload(self, request, insertion_point, payload, default_encoding):
        request['body'] = f"INSERTED:{payload}".encode()
        return request, "body"

class DummyRequest(dict):
    def send(self, insertions=None, **kwargs):
        return {"status": "sent", "insertions": insertions}

def test_insertion_initializes_payload():
    ip = InsertionPoint(location=DummyLocation(), location_key="body", key="key", value="original")
    req = DummyRequest(body="original_body")
    ins = Insertion(ip, "PAYLOAD", req)
    
    assert ins.payload == "PAYLOAD"
    assert ins.req['body'] == "original_body"
    assert ins.full_section is None

def test_insertion_formats_payload():
    mock_formatter = Mock()
    mock_formatter.format.return_value = "formatted_PAYLOAD"

    ip = InsertionPoint(location=DummyLocation(), location_key="body", key="key", value="original")
    req = DummyRequest(body="original_body")
    ins = Insertion(ip, "PAYLOAD", req, format_payload=True, payload_formatter=mock_formatter)

    mock_formatter.format.assert_called_once_with("PAYLOAD", old="original")
    assert ins.payload == "formatted_PAYLOAD"

def test_insertion_insert_request_applies_payload():
    ip = InsertionPoint(location=DummyLocation(), location_key="body", key="key", value="original")
    req = DummyRequest(body="original_body")
    ins = Insertion(ip, "PAYLOAD", req)

    updated_request = ins.insert_request(req)
    assert updated_request['body'] == b"INSERTED:PAYLOAD"
    assert ins.full_section == "body"


