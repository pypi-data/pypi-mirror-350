"""Utilidades de logging para Medallion ETL."""

import logging
from pathlib import Path
from typing import Optional

from medallion_etl.config import config


def setup_logger(name: str, level: Optional[str] = None, log_file: Optional[Path] = None) -> logging.Logger:
    """Configura un logger con el nivel y archivo especificados."""
    # Determinar nivel de log
    log_level = getattr(logging, (level or config.log_level).upper())
    
    # Crear logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    
    # Evitar duplicación de handlers
    if logger.handlers:
        return logger
    
    # Crear formateador
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Configurar handler de consola
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Configurar handler de archivo si se especifica
    if log_file is not None:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger


# Logger global para la librería
logger = setup_logger(
    "medallion_etl",
    config.log_level,
    config.log_dir / "medallion_etl.log"
)