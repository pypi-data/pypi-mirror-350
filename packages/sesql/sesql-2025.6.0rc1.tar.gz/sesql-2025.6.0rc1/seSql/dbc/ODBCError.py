import re


class PyODBCError(Exception):
    """
    Handle errors for PyODBC. Offers an error message parser
    to apply specific logic depending on the error raise

    ODBC error identifier: 23000

    pyodbc_error_message (str) -- message raised by PyODBC
        Example:
            [23000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server] \
            Cannot insert explicit value for identity column in table \
            'building' when IDENTITY_INSERT is set to OFF.
            (544) (SQLExecDirectW) \
    """

    error_pattern = re.compile(
        # r"\[(?P<error_id>.*?)\] \[(?P<operator>.*?)\]\[(?P<driver>.*?)\]\[(?P<database_type>.*?)\](?P<error_message>.+?(?= \()) \((?P<sql_server_error_id>\d*?)\) \(SQLExecDirectW\)"
        r"\[(?P<error_id>.*?)] \[(?P<database_type>.*?)]\[(?P<driver>.*?)](?P<error_message>.+?(?= \()) \((?P<sql_server_error_id>\d*?)\) \((?P<sql_type>.*?)\)"
    )
    sql_error_code_pattern = re.compile(r"\((?P<sql_server_error_code>\d*?)\) \(SQLExecDirectW\)")
    column_pattern = re.compile(r"column \'(?P<column_name>.+?)\'")
    table_pattern = re.compile(r"table \'(?P<table_name>.+?)\'")
    pyodbc_error_code = 'HY000'

    def __init__(self, pyodbc_error_message: str) -> None:
        self._parse_error_message(pyodbc_error_message)

    def __str__(self) -> str:  # pragma: no cover
        return self.error_message

    def _parse_error_message(self, pyodbc_error_message: str) -> None:
        m = re.match(self.error_pattern, pyodbc_error_message)
        # self.operator = m.group('operator')
        if m:
            self.error_id = m.group('error_id')
            self.driver = m.group('driver')
            self.database_type = m.group('database_type')
            self.error_message = m.group('error_message')
            self.sql_server_error_id = m.group('sql_server_error_id')

    @classmethod
    def get_message(cls, pyodbc_exception: Exception) -> str:
        if pyodbc_exception.args[1] == cls.pyodbc_error_code:
            return pyodbc_exception.args[0]
        else:
            return pyodbc_exception.args[1]  # pragma: no cover

    @classmethod
    def get_pyodbc_code(cls, pyodbc_exception: Exception) -> str:
        if pyodbc_exception.args[1] == cls.pyodbc_error_code:
            return pyodbc_exception.args[1]
        else:
            return pyodbc_exception.args[0]  # pragma: no cover

    @staticmethod
    def get_exception(error_code: int):
        return {
            515: IdentityInsertNull,
            544: IdentityInsertSetToOff,
            2627: PrimaryKeyViolation,
            8114: FailedTypeConversion,
            102: IncorrectSyntax,
            32: InvalidNumberParametersSupplied
        }.get(error_code, DefaultException)

    @classmethod
    def get_sql_server_error_code(cls, pyodbc_code: str, message: str) -> int:
        """
        Parses error message raised by PyODBC and return SQL Server Error Code

        Looks for the following pattern:
            (544) (SQLExecDirectW) -> 544

        Args:
            pyodbc_error_message (str): Error string raised by PyODBC

        Returns:
            (int) - SQL Server Error Code
            :param message:
            :param pyodbc_code:
        """

        if pyodbc_code == cls.pyodbc_error_code:
            return 32
        else:  # pragma: no cover
            m = re.search(cls.sql_error_code_pattern, message)
            if m:
                return int(m.group('sql_server_error_code'))
            else:
                raise ValueError(f"Error raised is not from SQL Server: {message}")

    @classmethod
    def build_pyodbc_exception(cls, pyodbc_exception: Exception):
        pyodbc_code = cls.get_pyodbc_code(pyodbc_exception)
        error_message = cls.get_message(pyodbc_exception)
        error_code = cls.get_sql_server_error_code(pyodbc_code, error_message)
        exception = cls.get_exception(error_code)
        raise exception(error_message)


class IdentityInsertNull(PyODBCError):
    """
    Handle specific PyODBC error related to Null Value Inserted on Identity Column
    """

    def __init__(self, pyodbc_error_message):  # pragma: no cover
        super().__init__(pyodbc_error_message)
        m = re.search(self.table_pattern, self.error_message)
        self.table_name = m.group('table_name')
        m = re.search(self.column_pattern, self.error_message)
        self.column_name = m.group('column_name')


class IdentityInsertSetToOff(PyODBCError):
    """
    Handle specific PyODBC error related to Identity Not Set to On/Off
    """

    def __init__(self, pyodbc_error_message):
        super().__init__(pyodbc_error_message)
        m = re.search(self.table_pattern, self.error_message)
        self.table_name = m.group('table_name')


class FailedTypeConversion(PyODBCError):
    """
    Handle specific PyODBC error related to data type conversion
    """

    def __init__(self, pyodbc_error_message):
        super().__init__(pyodbc_error_message)


class PrimaryKeyViolation(PyODBCError):
    """
    Handle specific PyODBC error related to Primary Key Violation
    """

    def __init__(self, pyodbc_error_message):
        super().__init__(pyodbc_error_message)


class IncorrectSyntax(PyODBCError):
    """
    Handle specific PyODBC error related to incorrect syntax in a query
    """

    def __init__(self, pyodbc_error_message):
        super().__init__(pyodbc_error_message)


class DefaultExceptionId(PyODBCError):
    """
    Handle default PyODBC errors
    """

    def __init__(self, pyodbc_error_message):
        super().__init__(pyodbc_error_message)

    def __str__(self) -> str:
        return f"{self.sql_server_error_id}"


class DefaultException(PyODBCError):
    """
    Handle default PyODBC errors
    """

    def __init__(self, pyodbc_error_message):
        super().__init__(pyodbc_error_message)

    def __str__(self) -> str:
        try:
            return f"{self.error_message}"
        except AttributeError:
            return f"Error message not available"


class InvalidNumberParametersSupplied(Exception):
    def __init__(self, error_message) -> None:
        self.message = error_message

    def __str__(self) -> str:
        return self.message
