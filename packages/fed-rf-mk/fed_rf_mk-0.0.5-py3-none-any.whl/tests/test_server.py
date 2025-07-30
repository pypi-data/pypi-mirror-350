import pytest
from fed_rf_mk.server import FLServer

# Dummy classes to simulate a Syft client with requests
class DummyStatus:
    def __init__(self, name):
        self.name = name

class DummyRequest:
    def __init__(self, code, status):
        self.code = code
        self.status = status
    def approve(self, approve_nested=False):
        # simulate approve changing status name
        self.status.name = "APPROVED"

class DummyClient:
    def __init__(self, reqs):
        self.requests = reqs

@pytest.fixture
def server():
    # no actual server.spawn call here
    srv = FLServer("test", 1234, "data.csv", "mock.csv", auto_accept=False)
    return srv

def test_list_no_requests(server, capfd):
    server.client = DummyClient([])
    server.list_pending_requests()
    out = capfd.readouterr().out
    assert "Pending requests:" in out
    # no indices printed

def test_list_some_requests(server, capfd):
    reqs = [
        DummyRequest(code=None, status=DummyStatus("PENDING")),
        DummyRequest(code=None, status=DummyStatus("APPROVED")),
    ]
    server.client = DummyClient(reqs)
    server.list_pending_requests()
    out = capfd.readouterr().out
    assert "[0] status=PENDING" in out
    assert "[1] status=APPROVED" in out

def test_approve_request(server):
    reqs = [DummyRequest(code=lambda x: x, status=DummyStatus("PENDING"))]
    server.client = DummyClient(reqs)
    server.approve_request(0)
    assert server.client.requests[0].status.name == "APPROVED"

def test_approve_invalid_index(server, capfd):
    server.client = DummyClient([])
    server.approve_request(5)
    out = capfd.readouterr().out
    assert "No request at index 5" in out

def test_inspect_request(server):
    dummy_fn = lambda data: data
    reqs = [DummyRequest(code=dummy_fn, status=DummyStatus("PENDING"))]
    server.client = DummyClient(reqs)
    result = server.inspect_request(0)
    assert result is dummy_fn

def test_inspect_bad_index(server, capfd):
    server.client = DummyClient([])
    result = server.inspect_request(0)
    out = capfd.readouterr().out
    assert "No request at index 0" in out
    assert result is None
