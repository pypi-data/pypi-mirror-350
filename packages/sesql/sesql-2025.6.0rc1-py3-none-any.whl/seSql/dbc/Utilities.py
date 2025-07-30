import socket

# Constants for error messages
HOSTNAME_ERROR = "Unable to get Hostname"
IP_ERROR = "Unable to get IP"


def get_hostname() -> str:
    """
    Retrieves the current host name of the machine.

    Returns:
        str: The hostname of the machine or error message if unavailable
    """
    try:
        return socket.gethostname()
    except Exception:
        return HOSTNAME_ERROR


def get_host_ip() -> str:
    """
    Retrieves the IP address corresponding to the current host name.

    Returns:
        str: The IP address of the host or error message if unavailable
    """
    try:
        hostname = get_hostname()
        if hostname == HOSTNAME_ERROR:
            return IP_ERROR
        return socket.gethostbyname(hostname)
    except Exception:
        return IP_ERROR


def mask(to_mask: str) -> str:
    """
    Masks the given string
    Create a new string composed of '*' repeated (len(str1) - 5) times, followed by the last 5 characters of the original string

    :param to_mask:
    :return: str
    """
    return '*' * (len(to_mask) - 5) + to_mask[-5:]
