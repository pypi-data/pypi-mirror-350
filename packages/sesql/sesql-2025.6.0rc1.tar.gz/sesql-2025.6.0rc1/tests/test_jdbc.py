import json

from seCore.CustomLogging import logger

from seSql import sql
from seSql.dbc.JDBC import jdbcLoaded, jdbcDriver

# Constants
DB_CONFIG = {
    "server": "SQL5101.site4now.net",
    "port": 1433,
    "user": "db_a82904_cybernetic_admin",
    "password": "tb7qiwqer8mee68",
    "trust": "no",
    "driverOverride": "odbc",
    "mars": "no"
}


def test_jdbc():
    oSql = sql()
    oSql.connect(**DB_CONFIG)

    json.dumps({
        'seSql': {
            'driver': json.loads(oSql.ConnectedStatus)["driver-info"],
        }
    })
    json.dumps({
        'seSql': {
            'ep': 'connect',
            'stats': json.loads(oSql.ConnectedStats),
        }
    })

    if oSql.isConnected:
        # oSql.query("SELECT @@version as version")
        oSql.query("select @@version as version")

        # oSql.query("select * from dbo.winequality_red;")

        try:
            oSql.query("select * from dbo.winequality_red;")
        except Exception as e:
            logger.error(f'Exception: {e}')

        try:
            oSql.query("select * from dba.winequality_red;")
        except Exception as e:
            logger.error(f'Exception: {e}')

        try:
            oResponse = oSql.query("select @@version as version;", stats=True)
            logger.info(oResponse['stats'])
            logger.info(oResponse['results'])
        except Exception as e:
            logger.error(f'{e}')

        try:
            oResponse = oSql.query("delete from dbo.seSql_Settings where value like '%dev';")
            logger.info(oResponse)
        except Exception as e:
            logger.error(f'{e}')


def test_jdbcLoaded():
    assert jdbcLoaded(3) is False


def test_jdbcDriver():
    assert jdbcDriver(3) == "Error finding JDBC driver"
