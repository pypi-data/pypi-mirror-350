"""Ejemplo de pipeline ETL para datos de ventas."""

from datetime import datetime
from typing import Dict, Any, Optional

import polars as pl
from pydantic import Field, field_validator
from prefect import flow

from medallion_etl.core import MedallionPipeline
from medallion_etl.bronze import CSVExtractor, SQLExtractor
from medallion_etl.silver import SchemaValidator, DataCleaner, TypeCaster
from medallion_etl.gold import Joiner, Aggregator, SQLLoader
from medallion_etl.schemas import BaseSchema
from medallion_etl.config import config
from medallion_etl.utils import logger


# Definir esquemas de datos
class SalesTransaction(BaseSchema):
    """Esquema para transacciones de ventas."""
    transaction_id: str = Field(..., description="ID único de la transacción")
    date: str = Field(..., description="Fecha de la transacción")
    customer_id: str = Field(..., description="ID del cliente")
    product_id: str = Field(..., description="ID del producto")
    quantity: int = Field(..., description="Cantidad vendida")
    unit_price: float = Field(..., description="Precio unitario")
    total_amount: float = Field(..., description="Monto total de la transacción")
    
    @field_validator('total_amount')
    def validate_total_amount(cls, v, info):
        """Valida que el monto total sea correcto."""
        values = info.data
        if 'quantity' in values and 'unit_price' in values:
            expected = values['quantity'] * values['unit_price']
            if abs(v - expected) > 0.01:  # Permitir pequeñas diferencias por redondeo
                logger.warning(f"Monto total incorrecto: {v} != {expected}")
                return expected
        return v


class Product(BaseSchema):
    """Esquema para productos."""
    product_id: str = Field(..., description="ID único del producto")
    name: str = Field(..., description="Nombre del producto")
    category: str = Field(..., description="Categoría del producto")
    supplier_id: Optional[str] = Field(None, description="ID del proveedor")
    unit_cost: float = Field(..., description="Costo unitario")


# Definir pipeline
def create_sales_pipeline() -> MedallionPipeline:
    """Crea un pipeline para procesar datos de ventas."""
    pipeline = MedallionPipeline(
        name="SalesPipeline",
        description="Pipeline para procesar datos de ventas"
    )
    
    # Capa Bronze - Extracción de datos
    # 1. Extraer transacciones de ventas desde CSV
    sales_extractor = CSVExtractor(
        name="SalesExtractor",
        description="Extrae datos de ventas desde CSV",
        output_path=config.bronze_dir / "sales",
        save_raw=True
    )
    pipeline.add_bronze_task(sales_extractor)
    
    # 2. Extraer datos de productos desde base de datos
    products_extractor = SQLExtractor(  # noqa: F841
        name="ProductsExtractor",
        description="Extrae datos de productos desde base de datos",
        output_path=config.bronze_dir / "products",
        save_raw=True
    )
    
    # Capa Silver - Validación y limpieza
    # 1. Validar transacciones de ventas
    sales_validator = SchemaValidator(
        schema_model=SalesTransaction,
        name="SalesValidator",
        description="Valida datos de transacciones de ventas",
        output_path=config.silver_dir / "sales",
        save_validated=True,
        drop_invalid=False,
        error_handling="log"  # Registrar errores pero continuar
    )
    pipeline.add_silver_task(sales_validator)
    
    # 2. Convertir tipos de datos para ventas
    sales_type_caster = TypeCaster(
        type_mapping={
            "quantity": "Int64",
            "unit_price": "Float64",
            "total_amount": "Float64"
        },
        name="SalesTypeCaster",
        description="Convierte tipos de datos de ventas",
        output_path=config.silver_dir / "sales"
    )
    pipeline.add_silver_task(sales_type_caster)
    
    # 3. Limpiar datos de ventas
    sales_cleaner = DataCleaner(
        name="SalesCleaner",
        description="Limpia datos de ventas",
        output_path=config.silver_dir / "sales",
        drop_na=True,  # Eliminar filas con valores nulos
        drop_duplicates=True,  # Eliminar duplicados
        cleaning_functions={
            # Funciones de limpieza personalizadas
            "date": lambda x: x.strip() if isinstance(x, str) else x,
            "customer_id": lambda x: x.strip().upper() if isinstance(x, str) else x,
            "product_id": lambda x: x.strip().upper() if isinstance(x, str) else x,
        }
    )
    pipeline.add_silver_task(sales_cleaner)
    
    # 4. Validar productos
    products_validator = SchemaValidator(  # noqa: F841
        schema_model=Product,
        name="ProductsValidator",
        description="Valida datos de productos",
        output_path=config.silver_dir / "products",
        save_validated=True
    )
    
    # Capa Gold - Transformación y carga
    # 1. Unir ventas con productos
    sales_products_joiner = Joiner(  # noqa: F841
        join_type="inner",
        left_on="product_id",
        right_on="product_id",
        name="SalesProductsJoiner",
        description="Une datos de ventas con productos",
        output_path=config.gold_dir / "sales_products"
    )
    
    # 2. Agregar ventas por categoría y fecha
    sales_aggregator = Aggregator(
        group_by=["category", "date"],
        aggregations={
            "quantity": "sum",
            "total_amount": "sum"
        },
        name="SalesByCategoryAggregator",
        description="Agrega ventas por categoría y fecha",
        output_path=config.gold_dir / "sales_by_category"
    )
    pipeline.add_gold_task(sales_aggregator)
    
    # 3. Cargar datos agregados en base de datos
    sales_loader = SQLLoader(
        table_name="sales_by_category",
        connection_string="sqlite:///data/sales_warehouse.db",
        if_exists="replace",
        name="SalesLoader",
        description="Carga datos agregados en base de datos"
    )
    pipeline.add_gold_task(sales_loader)
    
    return pipeline


# Función para ejecutar el pipeline
def run_sales_pipeline(sales_file_path: str, products_query_config: Dict[str, Any]) -> Dict[str, Any]:
    """Ejecuta el pipeline de datos de ventas."""
    # Asegurar que los directorios existan
    config.ensure_directories()
    
    # Crear y ejecutar el pipeline
    pipeline = create_sales_pipeline()
    logger.info(f"Iniciando pipeline {pipeline.name}")
    
    # Ejecutar extractor de ventas
    sales_extractor = pipeline.bronze_tasks[0]
    sales_result = sales_extractor.run(sales_file_path)
    sales_df = sales_result.data
    
    # Ejecutar extractor de productos
    products_extractor = SQLExtractor(
        name="ProductsExtractor",
        description="Extrae datos de productos desde base de datos",
        output_path=config.bronze_dir / "products",
        save_raw=True
    )
    products_result = products_extractor.run(products_query_config)
    products_df = products_result.data
    
    # Validar y limpiar ventas
    for task in pipeline.silver_tasks:
        sales_df = task.run(sales_df).data
    
    # Validar productos
    products_validator = SchemaValidator(
        schema_model=Product,
        name="ProductsValidator",
        description="Valida datos de productos",
        output_path=config.silver_dir / "products",
        save_validated=True
    )
    products_df = products_validator.run(products_df).data
    
    # Unir ventas con productos
    sales_products_joiner = Joiner(
        join_type="inner",
        left_on="product_id",
        right_on="product_id",
        name="SalesProductsJoiner",
        description="Une datos de ventas con productos",
        output_path=config.gold_dir / "sales_products"
    )
    joined_result = sales_products_joiner.run({"sales": sales_df, "products": products_df})
    joined_df = joined_result.data
    
    # Ejecutar tareas de la capa Gold
    result_df = joined_df
    for task in pipeline.gold_tasks:
        result = task.run(result_df)
        result_df = result.data if isinstance(result.data, pl.DataFrame) else result_df
    
    logger.info(f"Pipeline {pipeline.name} completado con éxito")
    
    # Recopilar metadatos
    metadata = {
        "sales_rows": len(sales_df),
        "products_rows": len(products_df),
        "joined_rows": len(joined_df),
        "execution_time": datetime.now().isoformat(),
        "pipeline_name": pipeline.name
    }
    
    return metadata


# Registrar como flow de Prefect
@flow(name="sales_pipeline_flow")
def sales_pipeline_flow(
    sales_file_path: str,
    db_connection_string: str,
    products_query: str
):
    """Flow de Prefect para el pipeline de datos de ventas."""
    # Configurar consulta de productos
    products_query_config = {
        "connection_string": db_connection_string,
        "query": products_query
    }
    
    # Ejecutar pipeline
    metadata = run_sales_pipeline(sales_file_path, products_query_config)
    return metadata


# Ejemplo de uso
if __name__ == "__main__":
    # Configurar rutas y consultas
    sales_file_path = "data/sales_transactions.csv"
    db_connection_string = "sqlite:///data/products.db"
    products_query = "SELECT * FROM products"
    
    # Configurar consulta de productos
    products_query_config = {
        "connection_string": db_connection_string,
        "query": products_query
    }
    
    # Ejecutar pipeline
    metadata = run_sales_pipeline(sales_file_path, products_query_config)
    print(f"Pipeline ejecutado con éxito. Metadatos: {metadata}")
    
    # Alternativamente, ejecutar como flow de Prefect
    # sales_pipeline_flow(sales_file_path, db_connection_string, products_query)