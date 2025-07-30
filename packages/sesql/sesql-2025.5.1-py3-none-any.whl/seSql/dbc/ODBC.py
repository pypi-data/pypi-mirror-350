import json
import time
import inspect

from seSql.dbc.Utilities import mask
from seSql.dbc import ODBCError
from seSql.dbc.Exceptions import ODBCLoginFailed, ODBCInvalidOperation, ODBCDriverError

try:
    import pyodbc
    _pyodbc_available = True
except ImportError:  # pragma: no cover
    _pyodbc_available = False


validDrivers = ['ODBC Driver 18 for SQL Server', 'ODBC Driver 17 for SQL Server']


def odbcLoaded() -> bool:
    """
    Checks if the ODBC driver is loaded

    :return: bool
    """
    try:
        if not _pyodbc_available:  # pragma: no cover
            return False

        for validDriver in validDrivers:
            if validDriver in pyodbc.drivers():
                return True

        raise Exception()  # pragma: no cover

    except Exception:  # pragma: no cover
        return False


def odbcDriver() -> str:
    """
    Returns the ODBC driver
    :return: str
    """
    try:
        for validDriver in validDrivers:
            if validDriver in pyodbc.drivers():
                return validDriver

        raise Exception()  # pragma: no cover

    except Exception:  # pragma: no cover
        return "Error finding ODBC driver"


class odbcEngine:

    def __init__(self, server: str, port: int, user: str, password: str, trust: str, mars: str, db: str = "") -> None:
        """
        Initialize the odbcEngine object
        """
        self.__connStr = {
            "driver": odbcDriver(),
            "server": server,
            "port": port,
            "database": db,
            "user": user,
            "password": password,
            "trust": trust,
            "mars": mars
        }
        self.isConnected = False
        self.__cnxn = None
        self.connStats = None

    def connect(self):
        """
        Connect to database using pyodbc and ODBC Driver 17 or 18 for SQL Server
        """
        start_time = time.time()

        match self.__connStr["trust"]:
            case "yes":  # pragma: no cover
                connStr = f'DRIVER={{{self.__connStr["driver"]}}}; ' \
                          f'Server={self.__connStr["server"]},{self.__connStr["port"]}; ' \
                          f'DATABASE={self.__connStr["database"]}; ' \
                          f'UID={self.__connStr["user"]}; ' \
                          f'PWD={self.__connStr["password"]}; ' \
                          f'Trusted_Connection={self.__connStr["trust"]};'\
                          f'MARS_Connection={self.__connStr["mars"]};'
            case _:
                connStr = f'DRIVER={{{self.__connStr["driver"]}}}; ' \
                          f'Server={self.__connStr["server"]},{self.__connStr["port"]}; ' \
                          f'DATABASE={self.__connStr["database"]}; ' \
                          f'UID={self.__connStr["user"]}; ' \
                          f'PWD={self.__connStr["password"]};' \
                          f'MARS_Connection={self.__connStr["mars"]};'

        oJson = {
            f'odbc-{inspect.currentframe().f_code.co_name}': {
                'connection_ms': float(f'{0 * 1000:.2f}'),
                'connected': self.isConnected,
                'connStr': self.__connStr
            }}
        try:
            with pyodbc.connect(connStr, timeout=1, autocommit=False) as cnxn:
                self.__cnxn = cnxn
                self.isConnected = True
                oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['connected'] = self.isConnected

        except pyodbc.Error as ex:  # pragma: no cover
            oJson = {
                f'odbc-{inspect.currentframe().f_code.co_name}': {
                    'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                    'connected': self.isConnected,
                    'error': {}
                }
            }
            match f'{ODBCError.DefaultExceptionId(ex.args[1])}':  # pragma: no cover
                case "18456":
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['code'] = f'{ODBCError.DefaultExceptionId(ex.args[1])}'
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "ODBCLoginFailed"
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = f'{ODBCError.DefaultException(ex.args[1])}'
                    raise ODBCLoginFailed(json.dumps(oJson))
                case "851968" | "1048576":
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['code'] = f'{ODBCError.DefaultExceptionId(ex.args[1])}'
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "ODBCInvalidOperation"
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = f'{ODBCError.DefaultException(ex.args[1])}'
                    raise ODBCInvalidOperation(json.dumps(oJson))
                case _:
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['code'] = f'{ODBCError.DefaultExceptionId(ex.args[1])}'
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "ODBCDriverError"
                    oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = f'{ODBCError.DefaultException(ex.args[1])}'
                    raise ODBCDriverError(json.dumps(oJson))

        oJson = {
            f'odbc-{inspect.currentframe().f_code.co_name}': {
                'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                'connected': self.isConnected,
                'connStr': self.__connStr
            }}
        oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['connStr']['password'] = mask(oJson[f'odbc-{inspect.currentframe().f_code.co_name}']['connStr']['password'])
        # todo: verify if still needed
        # logger.info(json.dumps(oJson))
        self.connStats = json.dumps(oJson)

        return self.isConnected

    def query(self, query: str, stats: bool = False):
        if self.isConnected:
            start_time = time.time()
            try:
                with self.__cnxn.cursor() as cur:
                    cur.execute(query)
                    if cur.rowcount == -1:
                        r = [dict((cur.description[i][0], value)
                                  for i, value in enumerate(row)) for row in cur.fetchall()]
                        rCount = len(r)
                    else:
                        r = None
                        rCount = cur.rowcount
                    s = json.dumps({
                        f'odbc-{inspect.currentframe().f_code.co_name}': {
                            'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                            'rc': f'{cur.rowcount}:{rCount}',
                            'query': f'{query}'
                        }})

                if stats:
                    return {'results': r, 'stats': s}
                else:
                    return r

            except pyodbc.Error as e:  # pragma: no cover
                # todo: need to return
                oE = json.dumps({
                    f'odbc-{inspect.currentframe().f_code.co_name}': {
                        'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                        'query': f'{query}',
                        'error': f'{e}'
                    }})

                raise Exception(f'{oE}')

    @property
    def connectionString(self):  # pragma: no cover
        return self.__connStr
