class JDBCSecureConnection(Exception):
    """Exception raised for "encrypt" property is set to "true" and "trustServerCertificate" property is set to "false" but the driver could not establish a secure connection to SQL Server by using Secure Sockets Layer (SSL) encryption."""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class JDBCConnection(Exception):
    """Exception raised for jaydebeapi.Error."""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class JDBCLoginFailed(Exception):
    """Exception raised for Login failed for user/pw"""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class JDBCConnectionTimeOut(Exception):
    """Exception raised for Connect timed out. Verify the connection properties. Make sure that an instance of SQL Server is running on the host and accepting TCP/IP connections at the port"""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class JDBCConnectionReset(Exception):
    """Make sure that TCP connections to the port are not blocked by a firewall. Verify the connection properties. Make sure that an instance of SQL Server is running on the host and accepting TCP/IP connections at the port."""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class JDBCSQLServerDriver(Exception):
    """Exception raised for SQLServerDriver is not found."""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class ODBCLoginFailed(Exception):
    """Exception raised for Login failed for user/pw"""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class ODBCInvalidOperation(Exception):
    """Exception raised for Trust setting"""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class ODBCDriverError(Exception):
    """Exception raised for anything not caught by ODBC driver"""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class SQLQueryException(Exception):
    """Exception raised for anything caught by an SQL query."""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)


class SQLConnectionException(Exception):
    """Exception raised for anything caught by an SQL query."""
    def __init__(self, message: str) -> None:
        self.message = message

    def __str__(self) -> str:
        return str(self.message)
