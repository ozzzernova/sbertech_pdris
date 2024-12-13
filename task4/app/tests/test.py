import pytest

from app.src.main import PingPongImpl, ping

from unittest.mock import MagicMock

class PingPongTest(PingPongImpl):
    def __init__(self):
        self.value = 0
    
    def ping(self):
        self.value += 1
        return "ping" if self.value % 2 == 0 else "pong"


@pytest.fixture
def mock_ping_pong(mocker):
    mocker.patch('app.src.main.ping_pong', MagicMock(return_value=PingPongTest()))

def test_ping_pong(mock_ping_pong):
    assert ping() == "pong"
    assert ping() == "ping"
    assert ping() == "pong"

if __name__ == "__main__":
    unittest.main()
