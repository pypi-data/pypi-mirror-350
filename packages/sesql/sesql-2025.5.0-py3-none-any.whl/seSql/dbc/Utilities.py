import socket


def hostName() -> str:
    """
    Returns the current host name

    :return: str
    """
    try:
        return socket.gethostname()
    except Exception:  # pragma: no cover
        return "Unable to get Hostname"


def hostIP() -> str:
    try:
        _host_name = socket.gethostname()
        return socket.gethostbyname(_host_name)
    except Exception:  # pragma: no cover
        return "Unable to get IP"


def mask(to_mask: str) -> str:
    """
    Masks the given string
    Create a new string composed of '*' repeated (len(str1) - 5) times, followed by the last 5 characters of the original string

    :param to_mask:
    :return: str
    """
    return '*' * (len(to_mask) - 5) + to_mask[-5:]
