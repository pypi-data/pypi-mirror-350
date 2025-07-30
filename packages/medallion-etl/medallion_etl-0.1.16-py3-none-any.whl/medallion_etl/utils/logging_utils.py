"""Utilidades de logging para Medallion ETL, estilo Prefect."""

import logging
from pathlib import Path
from typing import Optional

from medallion_etl.config import config

from rich.logging import RichHandler

def setup_logger(name: str, level: Optional[str] = None, log_file: Optional[Path] = None) -> logging.Logger:
    """
    Configura un logger con RichHandler (colores y formato bonito estilo Prefect).
    Si se indica, guarda también en archivo en formato plano.
    """
    log_level = getattr(logging, (level or config.log_level or "INFO").upper())
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Evitar duplicación de handlers si recargas el módulo
    logger.handlers.clear()

    # Handler de consola con RichHandler
    console_handler = RichHandler(
        level=log_level,
        show_time=True,          # Timestamp estilo Prefect
        show_level=True,         # Nivel (INFO, WARNING...) en color
        show_path=False,         # Sin path de archivo
        rich_tracebacks=True,    # Stacktrace bonito si hay error
        markup=False,            # No hace falta markup en mensajes
        omit_repeated_times=False
    )
    logger.addHandler(console_handler)

    # Handler de archivo (opcional)
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    logger.propagate = False  # Para que no se dupliquen logs
    return logger

# Logger global para la librería (puedes importar este en todo tu código)
logger = setup_logger(
    "medallion_etl",
    config.log_level,
    config.log_dir / "medallion_etl.log"
)
