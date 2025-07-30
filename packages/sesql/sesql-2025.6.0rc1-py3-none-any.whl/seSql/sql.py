import json

from typing import Optional

from .__about__ import __version__

from .dbc.Exceptions import SQLConnectionException, SQLQueryException
from .dbc.JDBC import jdbcLoaded, jdbcDriver, jdbcEngine
from .dbc.ODBC import odbcLoaded, odbcDriver, odbcEngine


class sql:
    def __init__(self):
        self.__cnxn = None
        self.__isConnected = False
        self.__driverOverride = None
        self.__jdbcDriver = None
        self.__jdbcLoaded = None
        self.__odbcDriver = None
        self.__odbcLoaded = None
        self.__connStr = None
        self.__connStatus = None
        self.__connStats = None

    def connect(self,
                server: Optional[str] = None,
                port: Optional[int] = None,
                user: Optional[str] = None,
                password: Optional[str] = None,
                trust: Optional[str] = None,
                db: Optional[str] = "",
                trustServerCertificate: Optional[bool] = True,
                mars: Optional[str] = 'no',
                driverOverride: Optional[str] = None,
                ):

        self.__odbcLoaded = odbcLoaded()
        self.__odbcDriver = odbcDriver()
        self.__jdbcLoaded = jdbcLoaded()
        self.__jdbcDriver = jdbcDriver()
        self.__driverOverride = driverOverride.lower() if driverOverride.lower() in ["odbc", "jdbc"] else "odbc"

        self.__connStr = {
            "server": server,
            "port": port,
            "user": user,
            "password": password,
            "trust": trust,
            "db": db,
            "trustServerCertificate": trustServerCertificate,
            "mars": mars,
            "driverOverride": driverOverride
        }

        if self.__driverOverride == "odbc" and self.__odbcLoaded:
            self.__driverOverride = "odbc"
        elif self.__driverOverride == "jdbc" and self.__jdbcLoaded:
            self.__driverOverride = "jdbc"
        else:  # pragma: no cover
            self.__driverOverride = "jdbc"

        match self.__driverOverride:
            case "odbc":
                self.__cnxn = odbcEngine(
                    server=self.__connStr['server'],
                    port=self.__connStr['port'],
                    db=self.__connStr['db'],
                    user=self.__connStr['user'],
                    password=self.__connStr['password'],
                    trust=self.__connStr['trust'],
                    mars=self.__connStr['mars'],
                )
                self._logging()

                try:
                    self.__cnxn.connect()
                    self.__isConnected = self.__cnxn.isConnected
                    self.__connStats = self.__cnxn.connStats
                except Exception as e:  # pragma: no cover
                    raise SQLConnectionException(f'{e}')

            case _:
                self.__cnxn = jdbcEngine(
                    server=self.__connStr['server'],
                    port=self.__connStr['port'],
                    user=self.__connStr['user'],
                    password=self.__connStr['password'],
                    trustServerCertificate=self.__connStr['trustServerCertificate']
                )
                self._logging()

                try:
                    self.__cnxn.connect()
                    self.__isConnected = self.__cnxn.isConnected
                    self.__connStats = self.__cnxn.connStats
                except Exception as e:  # pragma: no cover
                    raise SQLConnectionException(f'{e}')

    def query(self,
              query: str,
              stats: bool = False
              ):
        try:
            return self.__cnxn.query(query, stats=stats)
        except Exception as e:
            raise SQLQueryException(f'{e}')

    def _logging(self):
        oSqlDriver = {
            "driver-info":
                {
                    "using": self.__driverOverride,
                    "odbc": {
                        "loaded": self.__odbcLoaded,
                        "driver": self.__odbcDriver
                    },
                    "jdbc": {
                        "loaded": self.__jdbcLoaded,
                        "driver": self.__jdbcDriver
                    }
                }
        }
        self.__connStatus = json.dumps(oSqlDriver)

    @property
    def isConnected(self) -> bool:
        return self.__isConnected
        # return True

    @property
    def ConnectedStatus(self):

        return self.__connStatus

    @property
    def ConnectedStats(self):

        return self.__connStats

    @property
    def version(self):
        return __version__
