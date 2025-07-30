from seSql.dbc.Exceptions import ODBCLoginFailed, JDBCSecureConnection, JDBCLoginFailed, JDBCConnectionTimeOut, JDBCSQLServerDriver, JDBCConnectionReset, ODBCInvalidOperation, ODBCDriverError, JDBCConnection, SQLConnectionException


def test_odbcLogin_failed():
    try:
        raise ODBCLoginFailed('ODBCLoginFailed')
    except ODBCLoginFailed as e:
        print(e)
        assert e.message == 'ODBCLoginFailed'


def test_odbcInvalidOperation():
    try:
        raise ODBCInvalidOperation('ODBCInvalidOperation')
    except ODBCInvalidOperation as e:
        print(e)
        assert e.message == 'ODBCInvalidOperation'


def test_odbcDriverError():
    try:
        raise ODBCDriverError('ODBCDriverError')
    except ODBCDriverError as e:
        print(e)
        assert e.message == 'ODBCDriverError'


def test_jdbcSecure_connection():
    try:
        raise JDBCSecureConnection('JDBCSecureConnection')
    except JDBCSecureConnection as e:
        print(e)
        assert e.message == 'JDBCSecureConnection'


def test_jdbcLogin_failed():
    try:
        raise JDBCLoginFailed('JDBCLoginFailed')
    except JDBCLoginFailed as e:
        print(e)
        assert e.message == 'JDBCLoginFailed'


def test_jdbcConnection_time_out():
    try:
        raise JDBCConnectionTimeOut('JDBCConnectionTimeOut')
    except JDBCConnectionTimeOut as e:
        print(e)
        assert e.message == 'JDBCConnectionTimeOut'


def test_jdbcSqlServer_driver():
    try:
        raise JDBCSQLServerDriver('JDBCSQLServerDriver')
    except JDBCSQLServerDriver as e:
        print(e)
        assert e.message == 'JDBCSQLServerDriver'


def test_jdbcConnectionReset():
    try:
        raise JDBCConnectionReset('JDBCConnectionReset')
    except JDBCConnectionReset as e:
        print(e)
        assert e.message == 'JDBCConnectionReset'


def test_jdbcConnection():
    try:
        raise JDBCConnection('JDBCConnection')
    except JDBCConnection as e:
        print(e)
        assert e.message == 'JDBCConnection'


def test_sqlConnectionException():
    try:
        raise SQLConnectionException('SQLConnectionException')
    except SQLConnectionException as e:
        print(e)
        assert e.message == 'SQLConnectionException'
