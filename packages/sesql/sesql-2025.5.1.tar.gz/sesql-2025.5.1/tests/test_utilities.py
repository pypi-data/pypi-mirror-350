from seCore.CustomLogging import logger

from seSql import mask, seSqlVersion, hostName, hostIP


def test_mask():
    oMask = mask("Hello World")


def test_hostName():
    oHostName = hostName()


def test_hostIP():
    oIP = hostIP()

