"""Plantilla para crear pipelines en Medallion ETL."""

from medallion_etl.core import MedallionPipeline
from medallion_etl.bronze import CSVExtractor
from medallion_etl.silver import SchemaValidator, DataCleaner
from medallion_etl.gold import Aggregator


def create_sample_pipeline(name="SamplePipeline", config=None):
    """Crea un pipeline de ejemplo."""
    from medallion_etl.config import config as default_config
    config = config or default_config
    
    pipeline = MedallionPipeline(name=name, description="Pipeline de ejemplo")
    
    # Capa Bronze - Extracción
    extractor = CSVExtractor(
        name="SampleExtractor",
        description="Extrae datos de un archivo CSV",
        output_path=config.bronze_dir / name,
        save_raw=True
    )
    pipeline.add_bronze_task(extractor)
    
    # Capa Silver - Validación y limpieza
    validator = SchemaValidator(
        schema_model=None,  # Se puede definir un esquema personalizado
        name="SampleValidator",
        description="Valida datos contra el esquema definido",
        output_path=config.silver_dir / name,
        save_validated=True
    )
    pipeline.add_silver_task(validator)
    
    cleaner = DataCleaner(
        name="SampleCleaner",
        description="Limpia los datos",
        output_path=config.silver_dir / name,
        drop_na=True,
        drop_duplicates=True
    )
    pipeline.add_silver_task(cleaner)
    
    # Capa Gold - Transformación
    aggregator = Aggregator(
        group_by=["column1"],  # Reemplazar con columnas reales
        aggregations={
            "column2": "sum",  # Reemplazar con columnas y agregaciones reales
            "column3": "mean"
        },
        name="SampleAggregator",
        description="Agrega los datos",
        output_path=config.gold_dir / name
    )
    pipeline.add_gold_task(aggregator)
    
    return pipeline


def run_sample_pipeline(input_path, config=None):
    """Ejecuta el pipeline de ejemplo."""
    pipeline = create_sample_pipeline(config=config)
    result = pipeline.run(input_path)
    return result.metadata