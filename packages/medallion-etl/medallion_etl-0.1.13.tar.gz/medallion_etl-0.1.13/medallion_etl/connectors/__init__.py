"""Conectores para Medallion ETL."""

from medallion_etl.connectors.base import Connector
from medallion_etl.connectors.sql import SQLConnector

__all__ = [
    "Connector",
    "SQLConnector"
]