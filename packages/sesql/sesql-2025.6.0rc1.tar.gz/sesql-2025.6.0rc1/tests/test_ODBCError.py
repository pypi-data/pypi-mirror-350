import pytest
from seSql.dbc.ODBCError import PyODBCError, IdentityInsertNull, IdentityInsertSetToOff, PrimaryKeyViolation, \
    FailedTypeConversion, IncorrectSyntax, InvalidNumberParametersSupplied, DefaultExceptionId, DefaultException


def test_pyodbcerror_init():
    error_message = "[23000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server] Cannot insert explicit value for " \
                    "identity column in table 'building' when IDENTITY_INSERT is set to OFF. (544) (SQLExecDirectW) "
    exception = PyODBCError(error_message)
    assert exception.error_id == "23000"
    assert exception.driver == "ODBC Driver 17 for SQL Server"
    assert exception.database_type == "Microsoft"
    assert exception.error_message == "[SQL Server] Cannot insert explicit value for identity column in table 'building' when IDENTITY_INSERT is set to OFF."
    assert exception.sql_server_error_id == "544"


# def test_identity_insert_null_init():
#     error_message = "[23000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server] Cannot insert explicit value for " \
#                     "identity column in table 'employees' when IDENTITY_INSERT is set to OFF. (544) (SQLExecDirectW) "
#     exception = IdentityInsertNull(error_message)
#     assert exception.table_name == "employees"
#     assert exception.column_name is None


def test_identity_insert_set_to_off_init():
    error_message = "[23000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server] Cannot insert explicit value for " \
                    "identity column in table 'buildings' when IDENTITY_INSERT is set to OFF. (544) (SQLExecDirectW) "
    exception = IdentityInsertSetToOff(error_message)
    assert exception.table_name == "buildings"


def test_primary_key_violation_init():
    error_message = "[23000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server] Violation of PRIMARY KEY constraint " \
                    "'PK_table_name'. Cannot insert duplicate key in object 'dbo.table_name'. The duplicate key value is '(value)'. (2627) (SQLExecDirectW)"
    exception = PrimaryKeyViolation(error_message)
    assert isinstance(exception, PrimaryKeyViolation)


def test_failed_type_conversion_init():
    error_message = "[23000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server] Error converting data type varchar to int. (8114) (SQLExecDirectW)"
    exception = FailedTypeConversion(error_message)
    assert isinstance(exception, FailedTypeConversion)


def test_incorrect_syntax_init():
    error_message = "[23000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server] Incorrect syntax near 'some_syntax'. (102) (SQLExecDirectW)"
    exception = IncorrectSyntax(error_message)
    assert isinstance(exception, IncorrectSyntax)


def test_invalid_number_parameters_supplied():
    error_message = "Invalid number of parameters supplied."
    exception = InvalidNumberParametersSupplied(error_message)
    assert exception.message == error_message


def test_pyodbc_error_build_pyodbc_exception():
    pyodbc_exception = Exception("Some message", PyODBCError.pyodbc_error_code)
    with pytest.raises(InvalidNumberParametersSupplied):
        PyODBCError.build_pyodbc_exception(pyodbc_exception)


def test_pyodbc_error_get_sql_server_error_code():
    message = "[23000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server] Cannot insert explicit value for " \
              "identity column in table 'customers' when IDENTITY_INSERT is set to OFF. (544) (SQLExecDirectW) "
    pyodbc_code = "HY000"
    error_code = PyODBCError.get_sql_server_error_code(pyodbc_code, message)
    assert error_code == 32


def test_defaultexceptionid_str():
    error_message = "[23000] [Microsoft][ODBC Driver 17 for SQL Server][SQL Server] Cannot insert explicit value for " \
                    "identity column in table 'orders' when IDENTITY_INSERT is set to OFF. (544) (SQLExecDirectW) "
    exception = DefaultExceptionId(error_message)
    assert str(exception) == "544"


def test_invalid_number_parameters_supplied_message():
    error_message = "Invalid number of parameters supplied to the query."
    error = InvalidNumberParametersSupplied(error_message)
    assert str(error) == error_message


def test_invalid_number_parameters_supplied_empty_message():
    error_message = ""
    error = InvalidNumberParametersSupplied(error_message)
    assert str(error) == error_message


def test_default_exception_str_representation():
    """Test the string representation of DefaultException."""
    error_message = "Test default exception error message."
    exception = DefaultException(error_message)
    assert str(exception) != error_message


def test_default_exception_inheritance():
    """Test that DefaultException is a subclass of Exception."""
    error_message = "Another test message."
    exception = DefaultException(error_message)
    assert isinstance(exception, Exception)