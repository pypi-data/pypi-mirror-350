"""Validadores para la capa Silver de Medallion ETL."""

from pathlib import Path
from typing import Dict, Optional, Type, Callable
import polars as pl
from pydantic import BaseModel, ValidationError

from medallion_etl.core import DataFrameTask
from medallion_etl.config import config


class SchemaValidator(DataFrameTask):
    """Validador de esquema usando modelos Pydantic."""
    
    def __init__(
        self,
        schema_model: Type[BaseModel],
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_validated: bool = True,
        drop_invalid: bool = False,
        error_handling: str = "raise"  # 'raise', 'log', 'ignore'
    ):
        super().__init__(name or f"{schema_model.__name__}Validator", description)
        self.schema_model = schema_model
        self.output_path = output_path or config.silver_dir
        self.save_validated = save_validated
        self.drop_invalid = drop_invalid
        self.error_handling = error_handling
    
    def process_dataframe(self, df: pl.DataFrame, **kwargs) -> pl.DataFrame:
        """Valida un DataFrame contra un esquema Pydantic."""
        valid_rows = []
        invalid_rows = []
        validation_errors = []
        
        # Procesar cada fila
        for row_idx, row in enumerate(df.iter_rows(named=True)):
            try:
                # Validar con Pydantic
                validated_data = self.schema_model(**row).model_dump()
                valid_rows.append(validated_data)
            except ValidationError as e:
                invalid_rows.append(row)
                validation_errors.append({
                    "row_idx": row_idx,
                    "errors": e.errors()
                })
                
                if self.error_handling == "raise":
                    raise ValueError(f"Error de validación en la fila {row_idx}: {e}")
        
        # Crear DataFrame con filas válidas
        if valid_rows:
            result_df = pl.DataFrame(valid_rows)
        else:
            # Crear DataFrame vacío con las mismas columnas
            result_df = pl.DataFrame(schema=self.schema_model.model_json_schema()["properties"].keys())
        
        # Guardar datos validados si es necesario
        if self.save_validated and not result_df.is_empty():
            self.output_path.mkdir(parents=True, exist_ok=True)
            file_name = f"{self.name}_validated.parquet"
            result_df.write_parquet(self.output_path / file_name)
            
            # Guardar errores si hay alguno
            if invalid_rows and not self.drop_invalid:
                error_file = f"{self.name}_errors.json"
                import json
                with open(self.output_path / error_file, "w") as f:
                    json.dump(validation_errors, f, indent=2, default=str)
        
        return result_df


class DataCleaner(DataFrameTask):
    """Limpiador de datos para la capa Silver."""
    
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_cleaned: bool = True,
        drop_na: bool = False,
        drop_duplicates: bool = False,
        cleaning_functions: Optional[Dict[str, Callable]] = None
    ):
        super().__init__(name or "DataCleaner", description)
        self.output_path = output_path or config.silver_dir
        self.save_cleaned = save_cleaned
        self.drop_na = drop_na
        self.drop_duplicates = drop_duplicates
        self.cleaning_functions = cleaning_functions or {}
    
    def process_dataframe(self, df: pl.DataFrame, **kwargs) -> pl.DataFrame:
        """Limpia un DataFrame aplicando transformaciones."""
        result_df = df
        
        # Aplicar funciones de limpieza por columna
        for column, func in self.cleaning_functions.items():
            if column in result_df.columns:
                result_df = result_df.with_columns(
                    pl.col(column).map_elements(func).alias(column)
                )
        
        # Eliminar filas con valores nulos si se especifica
        if self.drop_na:
            result_df = result_df.drop_nulls()
        
        # Eliminar duplicados si se especifica
        if self.drop_duplicates:
            result_df = result_df.unique()
        
        # Guardar datos limpiados si es necesario
        if self.save_cleaned:
            self.output_path.mkdir(parents=True, exist_ok=True)
            file_name = f"{self.name}_cleaned.parquet"
            result_df.write_parquet(self.output_path / file_name)
        
        return result_df


class TypeCaster(DataFrameTask):
    """Conversor de tipos para la capa Silver."""
    
    def __init__(
        self,
        type_mapping: Dict[str, str],
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_casted: bool = True,
    ):
        super().__init__(name or "TypeCaster", description)
        self.type_mapping = type_mapping
        self.output_path = output_path or config.silver_dir
        self.save_casted = save_casted
    
    def process_dataframe(self, df: pl.DataFrame, **kwargs) -> pl.DataFrame:
        """Convierte los tipos de datos en un DataFrame."""
        result_df = df
        
        # Aplicar conversiones de tipo
        for column, dtype in self.type_mapping.items():
            if column in result_df.columns:
                try:
                    result_df = result_df.with_columns(
                        pl.col(column).cast(getattr(pl.datatypes, dtype))
                    )
                except Exception as e:
                    raise ValueError(f"Error al convertir la columna {column} a {dtype}: {e}")
        
        # Guardar datos convertidos si es necesario
        if self.save_casted:
            self.output_path.mkdir(parents=True, exist_ok=True)
            file_name = f"{self.name}_casted.parquet"
            result_df.write_parquet(self.output_path / file_name)
        
        return result_df