"""Conectores base para Medallion ETL."""

from abc import ABC, abstractmethod
from typing import Any, Optional

class Connector(ABC):
    """Clase base para todos los conectores."""
    
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description
    
    @abstractmethod
    def connect(self) -> Any:
        """Establece una conexión con la fuente o destino."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Cierra la conexión."""
        pass
    
    def __enter__(self):
        return self.connect()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()