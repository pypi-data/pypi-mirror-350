"""
KFlow - KLog.co ETL Package
===========================

A comprehensive Python package for Extract, Transform, Load (ETL) operations.
Designed for data engineering pipelines with support for various data sources
and destinations including AWS services, databases, and data warehouses.

Modules:
- extract: Data extraction from various sources (SQL, APIs, files)
- load: Data loading to warehouses and databases
- authn: Authentication and connection management
- tools: Utility functions and helpers
- monitoring: Performance monitoring and logging
- log: Advanced logging utilities

Example:
    >>> from kflow import extract, load, authn
    >>> df = extract.SQLFileToDataframe('queries/', 'my_query.sql', 'PrismaProd')
    >>> load.DataFrameToWarehouse('my_table', df)
"""

__version__ = "1.2.0"
__author__ = "KLog.co Data & BI"
__email__ = "data@klog.co"

# Import main modules for easier access
from . import extract
from . import load
from . import authn
from . import tools
from . import monitoring
from . import log

# Expose commonly used functions
from .extract import (
    SQLFileToDataframe,
    SQLFileToDataframeBatch,
    RDSPostgresTableAsDataFrame,
    WarehouseTableAsDataFrame,
    LakeFileAsDataFrame,
    PrismaTableSnapshot
)

from .load import (
    DataFrameToWarehouse,
    DataFrameToLake
)

from .authn import (
    getConnectionDB,
    awsClient
)

__all__ = [
    'extract',
    'load', 
    'authn',
    'tools',
    'monitoring',
    'log',
    # Commonly used functions
    'SQLFileToDataframe',
    'SQLFileToDataframeBatch', 
    'RDSPostgresTableAsDataFrame',
    'WarehouseTableAsDataFrame',
    'LakeFileAsDataFrame',
    'PrismaTableSnapshot',
    'DataFrameToWarehouse',
    'DataFrameToLake',
    'getConnectionDB',
    'awsClient'
] 