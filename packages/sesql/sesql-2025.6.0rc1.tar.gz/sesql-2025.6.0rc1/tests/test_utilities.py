import socket

from seSql.dbc.Utilities import get_host_ip, get_hostname

# Mock data for testing
HOSTNAME_ERROR = "Unable to get Hostname"
IP_ERROR = "Unable to get IP"
TEST_HOSTNAME = "test_hostname"
TEST_IP = "192.168.1.1"


def test_get_hostname_success(monkeypatch):
    """Test the get_hostname function when successfully retrieving the hostname."""

    def mock_gethostname():
        return TEST_HOSTNAME

    monkeypatch.setattr(socket, "gethostname", mock_gethostname)
    result = get_hostname()
    assert result == TEST_HOSTNAME


def test_get_hostname_failure(monkeypatch):
    """Test the get_hostname function when an exception occurs."""

    def mock_gethostname():
        raise Exception("Error retrieving hostname")

    monkeypatch.setattr(socket, "gethostname", mock_gethostname)
    result = get_hostname()
    assert result == HOSTNAME_ERROR


def test_get_hostname_error(monkeypatch):
    """Test the get_hostname function when retrieval fails."""

    def mock_gethostname():
        raise OSError("Unable to retrieve hostname")

    monkeypatch.setattr(socket, "gethostname", mock_gethostname)

    result = get_hostname()
    assert result == HOSTNAME_ERROR


def test_get_host_ip_success(monkeypatch):
    """Test the get_host_ip function when successful."""

    def mock_gethostname():
        return TEST_HOSTNAME

    def mock_gethostbyname(hostname):
        if hostname == TEST_HOSTNAME:
            return TEST_IP
        raise socket.gaierror("Unknown host")

    monkeypatch.setattr(socket, "gethostname", mock_gethostname)
    monkeypatch.setattr(socket, "gethostbyname", mock_gethostbyname)

    result = get_host_ip()
    assert result == TEST_IP


def test_get_host_ip_hostname_error(monkeypatch):
    """Test get_host_ip function when hostname retrieval fails."""

    def mock_gethostname():
        return HOSTNAME_ERROR

    monkeypatch.setattr(socket, "gethostname", mock_gethostname)

    result = get_host_ip()
    assert result == IP_ERROR


def test_get_host_ip_socket_error(monkeypatch):
    """Test get_host_ip function when socket.gethostbyname raises an error."""

    def mock_gethostname():
        return TEST_HOSTNAME

    def mock_gethostbyname(hostname):
        raise socket.gaierror("Unknown host")

    monkeypatch.setattr(socket, "gethostname", mock_gethostname)
    monkeypatch.setattr(socket, "gethostbyname", mock_gethostbyname)

    result = get_host_ip()
    assert result == IP_ERROR
