"""Esquemas base para Medallion ETL."""

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, ConfigDict


class BaseSchema(BaseModel):
    """Esquema base para todos los modelos de datos."""
    model_config = ConfigDict(extra="ignore")


class MetadataSchema(BaseSchema):
    """Esquema para metadatos de procesamiento."""
    source: str = Field(..., description="Fuente de los datos")
    processed_at: datetime = Field(default_factory=datetime.now, description="Fecha y hora de procesamiento")
    version: str = Field(default="1.0", description="Versión del esquema")
    pipeline_name: Optional[str] = Field(None, description="Nombre del pipeline")
    additional_info: Dict[str, Any] = Field(default_factory=dict, description="Información adicional")