import os.path
import pathlib
import time

import jaydebeapi
import inspect
import json
import glob

from seSql.dbc.Exceptions import JDBCConnectionReset, JDBCSecureConnection, JDBCLoginFailed, JDBCConnectionTimeOut, JDBCSQLServerDriver, JDBCConnection
from seSql.dbc.Utilities import mask

jdbcDrivers = {
    "mssql-12.2.0": {
        "classname": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        "jar": "mssql-jdbc-12.2.0.jre8.jar"
    },
    "mssql-12.4.2": {
        "classname": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        "jar": "mssql-jdbc-12.4.2.jre8.jar"
    },
    "mssql-0.0.0": {
        "classname": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
        "jar": "mssql-jdbc-0.0.0.jre8.jar"
    }
}

ROOT = pathlib.Path(__file__).parent.absolute()


def drivers() -> list:
    """
    Returns a list of loaded JDBC drivers

    :return: list
    """
    jarsPath = f'{ROOT}/jars'
    return [os.path.basename(files) for files in glob.glob(f'{jarsPath}/*')]


def jdbcLoaded(idx: int = -1) -> bool:
    """
    Checks if the JDBC driver is loaded

    :return: bool
    """
    try:
        return True if type([item for item in drivers()][idx]) is str else False
    except IndexError:
        return False


def jdbcDriver(idx: int = -1) -> str:
    """
    Returns the ODBC driver
    :return:
    """
    try:
        _dvr = [item for item in drivers()][idx] if jdbcLoaded() else "Error finding JDBC driver"
        return _dvr.replace("-jdbc-", "-").replace(".jre8.jar", "")
    except IndexError:
        return "Error finding JDBC driver"


def getDriverSettings():
    try:
        return jdbcDrivers[jdbcDriver()]
    except KeyError:  # pragma: no cover
        return jdbcDrivers["mssql-0.0.0"]


class jdbcEngine:
    def __init__(self, server: str, port: int, user: str, password: str, driver: str = 'mssql-12.4.2', encrypt: bool = True, trustServerCertificate: bool = True):
        """
        :rtype: object
        """
        self.__connStr = {
            "driver": driver,
            "server": f'jdbc:sqlserver://{server}',
            "port": port,
            "database": "",
            "user": user,
            "password": password,
            "encrypt": encrypt,
            "trustServerCertificate": trustServerCertificate
        }
        self.__cnxn = None
        self.isConnected = False
        self.connStats = None

    def connect(self) -> bool:
        driver = getDriverSettings()
        args = {
            "user": self.__connStr["user"],
            "password": self.__connStr["password"]
        }

        start_time = time.time()

        try:
            self.__cnxn = jaydebeapi.connect(
                driver['classname'],
                f'{self.__connStr["server"]}:{self.__connStr["port"]};encrypt={self.__connStr["encrypt"]};trustServerCertificate={self.__connStr["trustServerCertificate"]};',
                args,
                f"{ROOT}/jars/{driver['jar']}")
            self.isConnected = True

        except jaydebeapi.Error as e:  # pragma: no cover
            oJson = {
                f'jdbc-{inspect.currentframe().f_code.co_name}': {
                    'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                    'connected': self.isConnected,
                    'error': {
                        'exception': 'jayError',
                        'details': f'{e}'
                    }
                }
            }
            raise JDBCConnection(json.dumps(oJson))

        except Exception as e:  # pragma: no cover
            oJson = {
                f'jdbc-{inspect.currentframe().f_code.co_name}': {
                    'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                    'connected': self.isConnected,
                    'error': {}
                }
            }

            match e:  # pragma: no cover
                case _ if "driver could not establish a secure connection" in str(e).lower():
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "JDBCSecureConnection"
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = "Unable to establish a secure connection"
                    raise JDBCSecureConnection(json.dumps(oJson))

                case _ if "login failed" in str(e).lower():
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "JDBCLoginFailed"
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = "Login failed"
                    raise JDBCLoginFailed(json.dumps(oJson))

                case _ if "connect timed out" in str(e).lower():
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "JDBCConnectionTimeOut"
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = "Connect timed out. Verify the connection properties. Make sure that an instance of SQL Server is running on the host and accepting TCP/IP connections at the port"
                    raise JDBCConnectionTimeOut(json.dumps(oJson))

                case _ if "sqlserverdriver is not found" in str(e).lower():
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "JDBCSQLServerDriver"
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = "SQLServerDriver is not found"
                    raise JDBCSQLServerDriver(json.dumps(oJson))

                case _:
                    # logger.error(f'Exception: {e}')
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['exception'] = "JDBCConnectionReset"
                    oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['error']['details'] = "Make sure that TCP connections to the port are not blocked by a firewall. Verify the connection properties. Make sure that an instance of SQL Server is running on the host and accepting TCP/IP connections at the port."
                    raise JDBCConnectionReset(json.dumps(oJson))

        oJson = {
            f'jdbc-{inspect.currentframe().f_code.co_name}': {
                'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                'connected': self.isConnected,
                'connStr': self.__connStr
            }}

        oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['connStr']['password'] = mask(oJson[f'jdbc-{inspect.currentframe().f_code.co_name}']['connStr']['password'])
        # todo: verify if still needed
        # logger.info(json.dumps(oJson))

        self.connStats = json.dumps(oJson)

        return self.isConnected

    def query(self, query: str, stats: bool = False):
        if self.isConnected:
            start_time = time.time()
            try:
                with self.__cnxn.cursor() as curs:
                    curs.execute(query)
                    if curs.rowcount == -1:
                        r = [dict((curs.description[i][0], value)
                                  for i, value in enumerate(row)) for row in curs.fetchall()]
                        rCount = len(r)
                    else:
                        r = None
                        rCount = curs.rowcount

                    s = json.dumps({
                        f'jdbc-{inspect.currentframe().f_code.co_name}': {
                            'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                            'rc': f'{curs.rowcount}:{rCount}',
                            'query': f'{query}'
                        }})

                if stats:
                    return {'results': r, 'stats': s}
                else:
                    return r

            except Exception as e:
                # todo: verify if still needed
                oE = json.dumps({
                    f'jdbc-{inspect.currentframe().f_code.co_name}': {
                        'connection_ms': float(f'{(time.time() - start_time) * 1000:.2f}'),
                        'query': f'{query}',
                        'error': f'{e}'
                    }})

                raise Exception(f'{oE}')

    @property
    def connectionString(self):  # pragma: no cover
        return self.__connStr
