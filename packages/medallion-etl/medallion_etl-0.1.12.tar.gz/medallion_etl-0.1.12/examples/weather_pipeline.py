"""Ejemplo completo de pipeline para datos meteorológicos."""

from typing import Dict, Any, List, Optional

from pydantic import Field
from prefect import flow

from medallion_etl.core import MedallionPipeline
from medallion_etl.bronze import APIExtractor
from medallion_etl.silver import SchemaValidator, DataCleaner, TypeCaster
from medallion_etl.gold import Aggregator, Partitioner
from medallion_etl.schemas import BaseSchema
from medallion_etl.config import config
from medallion_etl.utils import logger


# Definir esquemas de datos
class WeatherMeasurement(BaseSchema):
    """Esquema para datos meteorológicos."""
    station_id: str = Field(..., description="ID de la estación meteorológica")
    timestamp: str = Field(..., description="Marca de tiempo de la medición")
    temperature: float = Field(..., description="Temperatura en grados Celsius")
    humidity: Optional[float] = Field(None, description="Humedad relativa en porcentaje")
    pressure: Optional[float] = Field(None, description="Presión atmosférica en hPa")
    wind_speed: Optional[float] = Field(None, description="Velocidad del viento en km/h")
    precipitation: Optional[float] = Field(None, description="Precipitación en mm")


# Definir pipeline
def create_weather_pipeline() -> MedallionPipeline:
    """Crea un pipeline para procesar datos meteorológicos."""
    pipeline = MedallionPipeline(
        name="WeatherPipeline",
        description="Pipeline para procesar datos meteorológicos"
    )
    
    # Capa Bronze - Extracción de API
    api_extractor = APIExtractor(
        name="WeatherAPIExtractor",
        description="Extrae datos meteorológicos de una API",
        output_path=config.bronze_dir / "weather",
        save_raw=True,
        method="GET",
        headers={"Content-Type": "application/json"},
        data_key="data"  # Clave donde se encuentran los datos en la respuesta JSON
    )
    pipeline.add_bronze_task(api_extractor)
    
    # Capa Silver - Validación y limpieza
    validator = SchemaValidator(
        schema_model=WeatherMeasurement,
        name="WeatherValidator",
        description="Valida datos meteorológicos",
        output_path=config.silver_dir / "weather",
        save_validated=True,
        drop_invalid=False,
        error_handling="log"  # Registrar errores pero continuar
    )
    pipeline.add_silver_task(validator)
    
    # Convertir tipos de datos
    type_caster = TypeCaster(
        type_mapping={
            "temperature": "Float64",
            "humidity": "Float64",
            "pressure": "Float64",
            "wind_speed": "Float64",
            "precipitation": "Float64"
        },
        name="WeatherTypeCaster",
        description="Convierte tipos de datos meteorológicos",
        output_path=config.silver_dir / "weather"
    )
    pipeline.add_silver_task(type_caster)
    
    # Limpieza de datos
    cleaner = DataCleaner(
        name="WeatherCleaner",
        description="Limpia datos meteorológicos",
        output_path=config.silver_dir / "weather",
        drop_na=False,  # No eliminar filas con valores nulos
        drop_duplicates=True,  # Eliminar duplicados
        cleaning_functions={
            # Funciones de limpieza personalizadas
            "temperature": lambda x: round(x, 1) if x is not None else x,
            "humidity": lambda x: min(100, max(0, x)) if x is not None else x,  # Limitar entre 0 y 100
        }
    )
    pipeline.add_silver_task(cleaner)
    
    # Capa Gold - Agregación y particionamiento
    aggregator = Aggregator(
        group_by=["station_id"],
        aggregations={
            "temperature": "mean",
            "humidity": "mean",
            "pressure": "mean",
            "wind_speed": "max",
            "precipitation": "sum"
        },
        name="WeatherAggregator",
        description="Agrega datos meteorológicos por estación",
        output_path=config.gold_dir / "weather"
    )
    pipeline.add_gold_task(aggregator)
    
    # Particionar por estación
    partitioner = Partitioner(
        partition_by=["station_id"],
        name="WeatherPartitioner",
        description="Particiona datos meteorológicos por estación",
        output_path=config.gold_dir / "weather/partitioned",
        file_format="parquet"
    )
    pipeline.add_gold_task(partitioner)
    
    return pipeline


# Función para ejecutar el pipeline
def run_weather_pipeline(api_config: Dict[str, Any]) -> Dict[str, Any]:
    """Ejecuta el pipeline de datos meteorológicos."""
    # Asegurar que los directorios existan
    config.ensure_directories()
    
    # Crear y ejecutar el pipeline
    pipeline = create_weather_pipeline()
    logger.info(f"Iniciando pipeline {pipeline.name}")
    
    result = pipeline.run(api_config)
    
    logger.info(f"Pipeline {pipeline.name} completado con éxito")
    return result.metadata


# Registrar como flow de Prefect
@flow(name="weather_pipeline_flow")
def weather_pipeline_flow(api_url: str, stations: List[str] = None):
    """Flow de Prefect para el pipeline de datos meteorológicos."""
    # Configurar API
    api_config = {
        "url": api_url,
        "params": {}
    }
    
    if stations:
        api_config["params"]["stations"] = ",".join(stations)
    
    # Ejecutar pipeline
    metadata = run_weather_pipeline(api_config)
    return metadata


# Ejemplo de uso
if __name__ == "__main__":
    # Configurar API (en un caso real, esto sería una API real)
    # Para este ejemplo, podríamos usar una API pública como OpenWeatherMap
    api_url = "https://api.example.com/weather/current"
    stations = ["STATION001", "STATION002", "STATION003"]
    
    # Ejecutar como script
    api_config = {
        "url": api_url,
        "params": {"stations": ",".join(stations)}
    }
    
    metadata = run_weather_pipeline(api_config)
    print(f"Pipeline ejecutado con éxito. Metadatos: {metadata}")
    
    # Alternativamente, ejecutar como flow de Prefect
    # weather_pipeline_flow(api_url, stations)