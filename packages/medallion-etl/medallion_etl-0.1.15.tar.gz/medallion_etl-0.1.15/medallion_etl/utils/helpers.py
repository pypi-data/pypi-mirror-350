"""Funciones auxiliares para Medallion ETL."""

from pathlib import Path
from typing import Any, Dict, List, Optional, Union
import polars as pl
import json


def ensure_dir(path: Union[str, Path]) -> Path:
    """Asegura que un directorio exista."""
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_dataframe(df: pl.DataFrame, path: Union[str, Path], format: str = "parquet") -> Path:
    """Guarda un DataFrame en el formato especificado."""
    path = Path(path)
    ensure_dir(path.parent)
    
    format = format.lower()
    if format == "parquet":
        df.write_parquet(path)
    elif format == "csv":
        df.write_csv(path)
    elif format == "json":
        df.write_json(path)
    else:
        raise ValueError(f"Formato no soportado: {format}")
    
    return path


def load_dataframe(path: Union[str, Path], format: Optional[str] = None) -> pl.DataFrame:
    """Carga un DataFrame desde un archivo."""
    path = Path(path)
    
    if not format:
        # Inferir formato de la extensión
        format = path.suffix.lstrip('.')
    
    format = format.lower()
    if format in ["parquet", "pq"]:
        return pl.read_parquet(path)
    elif format in ["csv", "txt"]:
        return pl.read_csv(path)
    elif format == "json":
        return pl.read_json(path)
    else:
        raise ValueError(f"Formato no soportado: {format}")


def save_metadata(metadata: Dict[str, Any], path: Union[str, Path]) -> Path:
    """Guarda metadatos en formato JSON."""
    path = Path(path)
    ensure_dir(path.parent)
    
    with open(path, "w") as f:
        json.dump(metadata, f, indent=2, default=str)
    
    return path


def load_metadata(path: Union[str, Path]) -> Dict[str, Any]:
    """Carga metadatos desde un archivo JSON."""
    path = Path(path)
    
    with open(path, "r") as f:
        return json.load(f)


def get_file_list(directory: Union[str, Path], pattern: str = "*", recursive: bool = False) -> List[Path]:
    """Obtiene una lista de archivos que coinciden con un patrón."""
    directory = Path(directory)
    
    if recursive:
        return list(directory.glob(f"**/{pattern}"))
    else:
        return list(directory.glob(pattern))