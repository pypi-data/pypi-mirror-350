"""Configuraciones globales para la librería Medallion ETL."""

import os
from pathlib import Path
from typing import Dict, Optional
from pydantic import BaseModel


class MedallionConfig(BaseModel):
    """Configuración global para la librería Medallion ETL."""
    # Directorios de datos por defecto
    bronze_dir: Path = Path("data/bronze")
    silver_dir: Path = Path("data/silver")
    gold_dir: Path = Path("data/gold")
    
    # Configuración de logs
    log_level: str = "INFO"
    log_dir: Path = Path("logs")
    
    # Configuración de conexiones a bases de datos
    database_urls: Dict[str, str] = {}
    
    # Configuración de Prefect
    prefect_api_url: Optional[str] = None
    prefect_project_name: str = "medallion-etl"
    
    # Configuración de paralelismo
    max_workers: int = os.cpu_count() or 4
    
    # Configuración de reintentos
    max_retries: int = 3
    retry_delay_seconds: int = 5
    
    @classmethod
    def from_env(cls) -> "MedallionConfig":
        """Carga la configuración desde variables de entorno."""
        return cls(
            bronze_dir=Path(os.getenv("MEDALLION_BRONZE_DIR", "data/bronze")),
            silver_dir=Path(os.getenv("MEDALLION_SILVER_DIR", "data/silver")),
            gold_dir=Path(os.getenv("MEDALLION_GOLD_DIR", "data/gold")),
            log_level=os.getenv("MEDALLION_LOG_LEVEL", "INFO"),
            log_dir=Path(os.getenv("MEDALLION_LOG_DIR", "logs")),
            prefect_api_url=os.getenv("PREFECT_API_URL"),
            prefect_project_name=os.getenv("PREFECT_PROJECT_NAME", "medallion-etl"),
            max_workers=int(os.getenv("MEDALLION_MAX_WORKERS", os.cpu_count() or 4)),
            max_retries=int(os.getenv("MEDALLION_MAX_RETRIES", 3)),
            retry_delay_seconds=int(os.getenv("MEDALLION_RETRY_DELAY", 5)),
        )
    
    def ensure_directories(self) -> None:
        """Asegura que los directorios necesarios existan."""
        self.bronze_dir.mkdir(parents=True, exist_ok=True)
        self.silver_dir.mkdir(parents=True, exist_ok=True)
        self.gold_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)


# Instancia global de configuración
config = MedallionConfig()