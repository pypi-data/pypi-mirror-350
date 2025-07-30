# seSql

The seSql module allows you to connect to JDBC/ODBC from Python code to databases using 
Java [JDBC](http://java.sun.com/products/jdbc/overview.html) or [ODBC](https://learn.microsoft.com/et-ee/sql/connect/python/pyodbc/python-sql-driver-pyodbc?view=sql-server-2017).

## Install
```shell
pip install seSql
```

## Usage

### **_using JDBC/ODBC_**
```python
import json
import sys

from loguru import logger
from seSql import sql

logger.configure(**{"handlers": [{"sink": sys.stdout, "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | seSql | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>"}]})

if __name__ == '__main__':
    oSql = sql()
    oSql.connect(
        server="SQL.site4now.net",
        port=1433,
        user="db_user",
        password="{pw}",
        trust="no",
        driverOverride="odbc",      # options: odbc/jdbc
        mars="no"                   # option to use MARS but only works with ODBC, ignored with JDBC
    )
    
    logger.info(f'Loaded driver information:')
    logger.info(json.dumps({
        'seSql': {
            'driver': json.loads(oSql.ConnectedStatus)["driver-info"],
        }
    }))
    logger.info(f'')
    logger.info(f'Connection information:')
    logger.info(json.dumps({
        'seSql': {
            'ep': 'connect',
            'stats': json.loads(oSql.ConnectedStats),
        }
    }))
    logger.info(f'{"":->100}')

    if oSql.isConnected:
        # -----------------------------------------------------------------------------------------
        # select
        # -----------------------------------------------------------------------------------------
        logger.info(f'select: returns results as `list`')
        try:
            oResponse = oSql.query("select @@version as version;")
            logger.info(oResponse)
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        logger.info(f'select: returns results as `dict` with execution stats')
        logger.info(f' - `stats`: json string')
        logger.info(f' - `results`: list')
        try:
            oResponse = oSql.query("select @@version as version;", stats=True)
            logger.info(oResponse['stats'])
            logger.info(oResponse['results'])
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        # -----------------------------------------------------------------------------------------
        # select: generates error
        # -----------------------------------------------------------------------------------------
        logger.info(f'select: generates error')
        try:
            oResponse = oSql.query("select @@@version as version;")
            logger.info(oResponse)
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        # -----------------------------------------------------------------------------------------
        # insert
        # -----------------------------------------------------------------------------------------
        logger.info(f'insert: returns results as `list` or `None`')
        try:
            oResponse = oSql.query("insert into dbo.seSql_Settings ([key], value) values ('Env', 'dev');")
            logger.info(oResponse)
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        logger.info(f'insert: returns results as `dict` with execution stats')
        logger.info(f' - `stats`: json string')
        logger.info(f' - `results`: None')
        try:
            oResponse = oSql.query("insert into dbo.seSql_Settings ([key], value) values ('Env', 'dev');", stats=True)
            logger.info(oResponse['stats'])
            logger.info(oResponse['results'])
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        # -----------------------------------------------------------------------------------------
        # delete
        # -----------------------------------------------------------------------------------------
        logger.info(f'delete: returns results as `list` or `None`')
        try:
            oResponse = oSql.query("delete from dbo.seSql_Settings where value like '%dev';")
            logger.info(oResponse)
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        logger.info(f'delete: returns results as `dict` with execution stats')
        logger.info(f' - `stats`: json string')
        logger.info(f' - `results`: None')
        try:
            oResponse = oSql.query("delete from dbo.seSql_Settings  where timestamp < cast(getdate() as date);", stats=True)
            logger.info(oResponse['stats'])
            logger.info(oResponse['results'])
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        # -----------------------------------------------------------------------------------------
        # update
        # -----------------------------------------------------------------------------------------
        logger.info(f'update: returns results as `list` or `None`')
        try:
            oResponse = oSql.query("update dbo.seSql_Settings set value = 'false' where [key] like '%Updated';", stats=True)
            logger.info(oResponse['stats'])
            logger.info(oResponse['results'])
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        logger.info(f'update: returns results as `dict` with execution stats')
        logger.info(f' - `stats`: json string')
        logger.info(f' - `results`: None')

        try:
            oResponse = oSql.query("select * from dbo.seSql_Settings;", stats=True)
            logger.info(oResponse['stats'])
            logger.info(oResponse['results'])
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')
```
### **_output_**
```shell
2024-04-30 | seSql | INFO     | Loaded driver information:
2024-04-30 | seSql | INFO     | {"seSql": {"driver": {"using": "odbc", "odbc": {"loaded": true, "driver": "ODBC Driver 18 for SQL Server"}, "jdbc": {"loaded": true, "driver": "mssql-12.4.2"}}}}
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | Connection information:
2024-04-30 | seSql | INFO     | {"seSql": {"ep": "connect", "stats": {"odbc-connect": {"connection_ms": 701.86, "connected": true, "connStr": {"driver": "ODBC Driver 18 for SQL Server", "server": "SQL5101.site4now.net", "port": 1433, "database": "", "user": "db_a82904_cybernetic_admin", "password": "**********mee68", "trust": "no", "mars": "no"}}}}}
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | select: returns results as `list`
2024-04-30 | seSql | INFO     | [{'version': 'Microsoft SQL Server 2019 (RTM-GDR) (KB5014356) - 15.0.2095.3 (X64) \n\tApr 29 2022 18:00:13 \n\tCopyright (C) 2019 Microsoft Corporation\n\tWeb Edition (64-bit) on Windows Server 2019 Standard 10.0 <X64> (Build 17763: ) (Hypervisor)\n'}]
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | select: returns results as `dict` with execution stats
2024-04-30 | seSql | INFO     |  - `stats`: json string
2024-04-30 | seSql | INFO     |  - `results`: list
2024-04-30 | seSql | INFO     | {"odbc-query": {"connection_ms": 54.88, "rc": "-1:1", "query": "select @@version as version;"}}
2024-04-30 | seSql | INFO     | [{'version': 'Microsoft SQL Server 2019 (RTM-GDR) (KB5014356) - 15.0.2095.3 (X64) \n\tApr 29 2022 18:00:13 \n\tCopyright (C) 2019 Microsoft Corporation\n\tWeb Edition (64-bit) on Windows Server 2019 Standard 10.0 <X64> (Build 17763: ) (Hypervisor)\n'}]
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | select: generates error
2024-04-30 | seSql | ERROR    | {"odbc-query": {"connection_ms": 54.98, "query": "select @@@version as version;", "error": "('42000', '[42000] [Microsoft][ODBC Driver 18 for SQL Server][SQL Server]Must declare the scalar variable \"@@@version\". (137) (SQLExecDirectW)')"}}
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | insert: returns results as `list` or `None`
2024-04-30 | seSql | INFO     | None
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | insert: returns results as `dict` with execution stats
2024-04-30 | seSql | INFO     |  - `stats`: json string
2024-04-30 | seSql | INFO     |  - `results`: None
2024-04-30 | seSql | INFO     | {"odbc-query": {"connection_ms": 58.97, "rc": "1:1", "query": "insert into dbo.seSql_Settings ([key], value) values ('Env', 'dev');"}}
2024-04-30 | seSql | INFO     | None
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | delete: returns results as `list` or `None`
2024-04-30 | seSql | INFO     | None
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | delete: returns results as `dict` with execution stats
2024-04-30 | seSql | INFO     |  - `stats`: json string
2024-04-30 | seSql | INFO     |  - `results`: None
2024-04-30 | seSql | INFO     | {"odbc-query": {"connection_ms": 59.31, "rc": "0:0", "query": "delete from dbo.seSql_Settings  where timestamp < cast(getdate() as date);"}}
2024-04-30 | seSql | INFO     | None
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | update: returns results as `list` or `None`
2024-04-30 | seSql | INFO     | {"odbc-query": {"connection_ms": 59.67, "rc": "0:0", "query": "update dbo.seSql_Settings set value = 'false' where [key] like '%Updated';"}}
2024-04-30 | seSql | INFO     | None
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2024-04-30 | seSql | INFO     | update: returns results as `dict` with execution stats
2024-04-30 | seSql | INFO     |  - `stats`: json string
2024-04-30 | seSql | INFO     |  - `results`: None
2024-04-30 | seSql | INFO     | {"odbc-query": {"connection_ms": 59.11, "rc": "0:0", "query": "select * from dbo.seSql_Settings;"}}
2024-04-30 | seSql | INFO     | None
2024-04-30 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
```

### Functions: seSqlVersion, hostName, hostIP, mask
```python
import json
import sys

from seSql import seSqlVersion, mask, hostName, hostIP
from loguru import logger
logger.configure(**{"handlers": [{"sink": sys.stdout, "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | seSql | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>"}]})

if __name__ == '__main__':
    logger.info(json.dumps({
        'seSql': {
            'functions': {
                'host': hostName(),
                'hostIP': hostIP(),
                'mask_all_but_last_12345': mask('all_but_last_12345'),
                'version': seSqlVersion
            }
        }}, indent=4))
```

### **_output_**
```shell
2024-04-30 | seSql | INFO     | {
    "seSql-info": {
        "host": "MacBook-Pro",
        "hostIP": "127.0.0.1",
        "mask_all_but_last_12345": "*************12345",
        "version": "2024.5.0 build[75]"
    }
}

```