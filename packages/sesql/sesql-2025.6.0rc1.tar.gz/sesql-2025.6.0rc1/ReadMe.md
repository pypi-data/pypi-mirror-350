# seSql

A Python library that enables seamless database connectivity through both JDBC and ODBC interfaces, supporting Java [JDBC](http://java.sun.com/products/jdbc/overview.html) drivers and native [ODBC](https://learn.microsoft.com/et-ee/sql/connect/python/pyodbc/python-sql-driver-pyodbc?view=sql-server-2017) connections for database integration
## Install
```shell
pip install seSql
```

## Usage

### **_using JDBC/ODBC_**: select, update, insert, delete, ConnectedStatus, ConnectedStats and version
```python
import json
import sys

from loguru import logger
from seSql import sql

logger.configure(**{"handlers": [{"sink": sys.stdout, "format": "<green>{time:YYYY-MM-DD}</green> | seSql | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>"}]})

# Constants
DB_CONFIG = {
    "server": "SQL.site4now.net",
    "port": 1433,
    "user": "db_user",
    "password": "{pw}",
    "trust": "no",
    "driverOverride": "odbc",      # options: odbc/jdbc
    "mars": "no"                   # option to use MARS but only works with ODBC, ignored with JDBC
}

if __name__ == '__main__':

    oSql = sql()
    oSql.connect(**DB_CONFIG)

    # -----------------------------------------------------------------------------------------
    # Connection Information
    # -----------------------------------------------------------------------------------------
    logger.info(f'Connection Status:')
    logger.info(json.dumps({'seSql': json.loads(oSql.ConnectedStatus)}))
    logger.info(f'{"":->100}')
    # -----------------------------------------------------------------------------------------
    logger.info(f'Connection Stats:')
    logger.info(json.dumps({'seSql': json.loads(oSql.ConnectedStats)}))
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

        logger.info(f'select: returns results as `list` and with execution statistics in `json string` format')
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
        logger.info(f'insert: returns results as `None`')
        try:
            oResponse = oSql.query("insert into dbo.seSql_Settings ([key], value) values ('Env', 'dev');")
            logger.info(oResponse)
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        logger.info(f'insert: returns results as `None` and with execution statistics in `json string` format')
        logger.info(f' - `results`: None')
        logger.info(f' - `stats`: json string')
        try:
            oResponse = oSql.query("insert into dbo.seSql_Settings ([key], value) values ('Env', 'dev');", stats=True)
            logger.info(oResponse['results'])
            logger.info(oResponse['stats'])
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        # -----------------------------------------------------------------------------------------
        # update
        # -----------------------------------------------------------------------------------------
        logger.info(f'update: returns results as `None`')
        try:
            oResponse = oSql.query("update dbo.seSql_Settings set value = 'false' where [key] like '%Updated';")
            logger.info(oResponse)
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        logger.info(f'update: returns results as `None` and with execution statistics in `json string` format')
        logger.info(f' - `stats`: json string')
        logger.info(f' - `results`: None')

        try:
            oResponse = oSql.query("select * from dbo.seSql_Settings;", stats=True)
            logger.info(oResponse['stats'])
            logger.info(oResponse['results'])
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        # -----------------------------------------------------------------------------------------
        # delete
        # -----------------------------------------------------------------------------------------
        logger.info(f'delete: returns results as `None`')
        logger.info(f' - `result`: None')
        try:
            oResponse = oSql.query("delete from dbo.seSql_Settings where value like '%dev';", stats=True)
            logger.info(oResponse)
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        logger.info(f'delete: returns results as `None` and with execution statistics in `json string` format')
        logger.info(f' - `stats`: json string')
        logger.info(f' - `result`: None')
        try:
            oResponse = oSql.query("delete from dbo.seSql_Settings  where timestamp < cast(getdate() as date);", stats=True)
            logger.info(oResponse['stats'])
            logger.info(oResponse['results'])
        except Exception as e:
            logger.error(f'{e}')
        logger.info(f'{"":->100}')

        # -----------------------------------------------------------------------------------------
        # Package Version
        # -----------------------------------------------------------------------------------------
        logger.info(f'seSql Version: {oSql.version}')
```
### **_output_**
```shell
2025-05-25 | seSql | INFO     | Connection Status:
2025-05-25 | seSql | INFO     | {"seSql": {"driver-info": {"using": "jdbc", "odbc": {"loaded": true, "driver": "ODBC Driver 18 for SQL Server"}, "jdbc": {"loaded": true, "driver": "mssql-12.4.2"}}}}
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | Connection Stats:
2025-05-25 | seSql | INFO     | {"seSql": {"jdbc-connect": {"connection_ms": 729.11, "connected": true, "connStr": {"driver": "mssql-12.4.2", "server": "jdbc:sqlserver://SQL5101.site4now.net", "port": 1433, "database": "", "user": "db_user", "password": "**********21368", "encrypt": true, "trustServerCertificate": true}}}}
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | select: returns results as `list`
2025-05-25 | seSql | INFO     | [{'version': 'Microsoft SQL Server 2019 (RTM-CU32) (KB5054833) - 15.0.4430.1 (X64) \n\tFeb 21 2025 17:28:26 \n\tCopyright (C) 2019 Microsoft Corporation\n\tWeb Edition (64-bit) on Windows Server 2022 Standard 10.0 <X64> (Build 20348: ) (Hypervisor)\n'}]
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | select: returns results as `list` and with execution statistics in `json string` format
2025-05-25 | seSql | INFO     |  - `stats`: json string
2025-05-25 | seSql | INFO     |  - `results`: list
2025-05-25 | seSql | INFO     | {"jdbc-query": {"connection_ms": 64.34, "rc": "-1:1", "query": "select @@version as version;"}}
2025-05-25 | seSql | INFO     | [{'version': 'Microsoft SQL Server 2019 (RTM-CU32) (KB5054833) - 15.0.4430.1 (X64) \n\tFeb 21 2025 17:28:26 \n\tCopyright (C) 2019 Microsoft Corporation\n\tWeb Edition (64-bit) on Windows Server 2022 Standard 10.0 <X64> (Build 20348: ) (Hypervisor)\n'}]
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | select: generates error
2025-05-25 | seSql | ERROR    | {"jdbc-query": {"connection_ms": 63.42, "query": "select @@@version as version;", "error": "com.microsoft.sqlserver.jdbc.SQLServerException: Must declare the scalar variable \"@@@version\"."}}
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | insert: returns results as `None`
2025-05-25 | seSql | INFO     | None
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | insert: returns results as `None` and with execution statistics in `json string` format
2025-05-25 | seSql | INFO     |  - `results`: None
2025-05-25 | seSql | INFO     |  - `stats`: json string
2025-05-25 | seSql | INFO     | None
2025-05-25 | seSql | INFO     | {"jdbc-query": {"connection_ms": 71.58, "rc": "1:1", "query": "insert into dbo.seSql_Settings ([key], value) values ('Env', 'dev');"}}
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | update: returns results as `None`
2025-05-25 | seSql | INFO     | None
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | update: returns results as `None` and with execution statistics in `json string` format
2025-05-25 | seSql | INFO     |  - `stats`: json string
2025-05-25 | seSql | INFO     |  - `results`: None
2025-05-25 | seSql | INFO     | {"jdbc-query": {"connection_ms": 75.17, "rc": "-1:2", "query": "select * from dbo.seSql_Settings;"}}
2025-05-25 | seSql | INFO     | [{'id': '2514F481-B2B8-412E-85D8-F5204218CF10', 'timestamp': '2025-05-25 18:17:54.720000', 'key': 'Env', 'value': 'dev'}, {'id': '2F89EF51-29BB-48F9-AE0C-3904C360DE27', 'timestamp': '2025-05-25 18:17:54.643333', 'key': 'Env', 'value': 'dev'}]
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | delete: returns results as `None`
2025-05-25 | seSql | INFO     |  - `result`: None
2025-05-25 | seSql | INFO     | {'results': None, 'stats': '{"jdbc-query": {"connection_ms": 65.72, "rc": "2:2", "query": "delete from dbo.seSql_Settings where value like \'%dev\';"}}'}
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | delete: returns results as `None` and with execution statistics in `json string` format
2025-05-25 | seSql | INFO     |  - `stats`: json string
2025-05-25 | seSql | INFO     |  - `result`: None
2025-05-25 | seSql | INFO     | {"jdbc-query": {"connection_ms": 72.2, "rc": "0:0", "query": "delete from dbo.seSql_Settings  where timestamp < cast(getdate() as date);"}}
2025-05-25 | seSql | INFO     | None
2025-05-25 | seSql | INFO     | ----------------------------------------------------------------------------------------------------
2025-05-25 | seSql | INFO     | seSql Version: 2025.6.0.rc1
```

### Functions: version, hostName, hostIP, mask
```python
import json
import sys

from seSql import version, mask, get_host_ip, get_hostname
from loguru import logger
logger.configure(**{"handlers": [{"sink": sys.stdout, "format": "<green>{time:YYYY-MM-DD}</green> | seSql | <level>{level: <8}</level> | <cyan><level>{message}</level></cyan>"}]})

if __name__ == '__main__':
    """
      Package functions:
       - hostName()
       - hostIP()
       - mask({str})
       - seSqlVersion
    """
    logger.info(json.dumps({
        'seSql': {
            'functions': {
                'host': get_hostname(),
                'hostIP': get_host_ip(),
                'mask_all_but_last_12345': mask('all_but_last_12345'),
                'version': version
            }
        }}, indent=4))
```

### **_output_**
```shell
2025-05-25 | seSql | INFO     | {
    "seSql": {
        "functions": {
            "host": "MacBook-Pro-M4-Max",
            "hostIP": "127.0.0.1",
            "mask_all_but_last_12345": "*************12345",
            "version": "2025.6.0.rc1"
        }
    }
}
```