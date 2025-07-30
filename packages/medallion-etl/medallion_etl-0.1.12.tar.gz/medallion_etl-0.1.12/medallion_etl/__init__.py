"""Medallion ETL: Una librería modular para construir data pipelines con arquitectura medallion."""

__version__ = "0.1.0"

# Importaciones principales para facilitar el uso de la librería
from medallion_etl.core.pipeline import Pipeline  # noqa: F401
from medallion_etl.core.task import Task  # noqa: F401
from medallion_etl.bronze import extractors  # noqa: F401
from medallion_etl.silver import validators  # noqa: F401
from medallion_etl.gold import transformers  # noqa: F401

# Importar CLI
from medallion_etl.cli import main  # noqa: F401
