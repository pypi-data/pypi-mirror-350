"""Transformadores para la capa Gold de Medallion ETL."""

from pathlib import Path
from typing import Dict, List, Optional, Union, Callable
import polars as pl
from sqlalchemy import create_engine

from medallion_etl.core import Task, DataFrameTask, TaskResult
from medallion_etl.config import config


class Aggregator(DataFrameTask):
    """Agregador de datos para la capa Gold."""
    
    def __init__(
        self,
        group_by: List[str],
        aggregations: Dict[str, Union[str, Callable]],
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_aggregated: bool = True,
    ):
        super().__init__(name or "Aggregator", description)
        self.group_by = group_by
        self.aggregations = aggregations
        self.output_path = output_path or config.gold_dir
        self.save_aggregated = save_aggregated
    
    def process_dataframe(self, df: pl.DataFrame, **kwargs) -> pl.DataFrame:
        """Agrega datos en un DataFrame."""
        # Construir expresiones de agregación
        agg_exprs = []
        for col, agg in self.aggregations.items():
            if isinstance(agg, str):
                # Usar método de agregación incorporado
                agg_expr = getattr(pl.col(col), agg)().alias(f"{col}_{agg}")
            else:
                # Usar función personalizada
                agg_expr = pl.col(col).map_elements(agg).alias(f"{col}_custom")
            
            agg_exprs.append(agg_expr)
        
        # Realizar la agregación
        result_df = df.group_by(self.group_by).agg(agg_exprs)
        
        # Guardar datos agregados si es necesario
        if self.save_aggregated:
            self.output_path.mkdir(parents=True, exist_ok=True)
            file_name = f"{self.name}_aggregated.parquet"
            result_df.write_parquet(self.output_path / file_name)
        
        return result_df


class Joiner(Task[Dict[str, pl.DataFrame], pl.DataFrame]):
    """Unificador de datos para la capa Gold."""
    
    def __init__(
        self,
        join_type: str = "inner",  # 'inner', 'left', 'right', 'outer', 'cross'
        on: Optional[Union[str, List[str]]] = None,
        left_on: Optional[Union[str, List[str]]] = None,
        right_on: Optional[Union[str, List[str]]] = None,
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_joined: bool = True,
    ):
        super().__init__(name or "Joiner", description)
        self.join_type = join_type
        self.on = on
        self.left_on = left_on
        self.right_on = right_on
        self.output_path = output_path or config.gold_dir
        self.save_joined = save_joined
    
    def run(self, input_data: Dict[str, pl.DataFrame], **kwargs) -> TaskResult[pl.DataFrame]:
        """Une dos DataFrames."""
        if len(input_data) != 2:
            raise ValueError("Se requieren exactamente dos DataFrames para unir")
        
        # Obtener los DataFrames
        dfs = list(input_data.values())
        left_df, right_df = dfs[0], dfs[1]
        
        # Determinar las columnas de unión
        if self.on is not None:
            left_on = right_on = self.on
        else:
            left_on = self.left_on
            right_on = self.right_on
            
            if left_on is None or right_on is None:
                raise ValueError("Se deben especificar las columnas de unión")
        
        # Realizar la unión
        if self.join_type == "inner":
            result_df = left_df.join(right_df, left_on=left_on, right_on=right_on, how="inner")
        elif self.join_type == "left":
            result_df = left_df.join(right_df, left_on=left_on, right_on=right_on, how="left")
        elif self.join_type == "right":
            result_df = left_df.join(right_df, left_on=left_on, right_on=right_on, how="right")
        elif self.join_type == "outer":
            result_df = left_df.join(right_df, left_on=left_on, right_on=right_on, how="outer")
        elif self.join_type == "cross":
            result_df = left_df.join(right_df, how="cross")
        else:
            raise ValueError(f"Tipo de unión no válido: {self.join_type}")
        
        # Guardar datos unidos si es necesario
        if self.save_joined:
            self.output_path.mkdir(parents=True, exist_ok=True)
            file_name = f"{self.name}_joined.parquet"
            result_df.write_parquet(self.output_path / file_name)
        
        metadata = {
            "left_rows": len(left_df),
            "right_rows": len(right_df),
            "result_rows": len(result_df),
            "join_type": self.join_type,
        }
        
        return TaskResult(result_df, metadata)


class Partitioner(DataFrameTask):
    """Particionador de datos para la capa Gold."""
    
    def __init__(
        self,
        partition_by: List[str],
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        file_format: str = "parquet",  # 'parquet', 'csv', 'json'
    ):
        super().__init__(name or "Partitioner", description)
        self.partition_by = partition_by
        self.output_path = output_path or config.gold_dir
        self.file_format = file_format.lower()
    
    def process_dataframe(self, df: pl.DataFrame, **kwargs) -> pl.DataFrame:
        """Particiona un DataFrame por columnas especificadas."""
        # Asegurar que el directorio de salida exista
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        # Obtener valores únicos para cada columna de particionamiento
        partitions = {}
        for col in self.partition_by:
            if col in df.columns:
                partitions[col] = df[col].unique().to_list()
        
        # Crear particiones y guardar datos
        for col in self.partition_by:
            for value in partitions[col]:
                # Filtrar datos para esta partición
                partition_df = df.filter(pl.col(col) == value)
                
                # Crear directorio para la partición
                partition_dir = self.output_path / f"{col}={value}"
                partition_dir.mkdir(parents=True, exist_ok=True)
                
                # Guardar datos en el formato especificado
                file_name = f"part_{col}_{value}"
                if self.file_format == "parquet":
                    partition_df.write_parquet(partition_dir / f"{file_name}.parquet")
                elif self.file_format == "csv":
                    partition_df.write_csv(partition_dir / f"{file_name}.csv")
                elif self.file_format == "json":
                    partition_df.write_json(partition_dir / f"{file_name}.json")
                else:
                    raise ValueError(f"Formato de archivo no válido: {self.file_format}")
        
        return df  # Devolver el DataFrame original


class SQLLoader(Task[pl.DataFrame, bool]):
    """Cargador de datos a bases de datos SQL para la capa Gold."""
    
    def __init__(
        self,
        table_name: str,
        connection_string: str,
        schema: Optional[str] = None,
        if_exists: str = "append",  # 'fail', 'replace', 'append'
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(name or f"SQLLoader_{table_name}", description)
        self.table_name = table_name
        self.connection_string = connection_string
        self.schema = schema
        self.if_exists = if_exists
    
    def run(self, input_data: pl.DataFrame, **kwargs) -> TaskResult[bool]:
        """Carga un DataFrame en una tabla SQL."""
        # Convertir a pandas para usar con SQLAlchemy
        pandas_df = input_data.to_pandas()
        
        # Crear motor de base de datos
        engine = create_engine(self.connection_string)
        
        # Cargar datos en la tabla
        pandas_df.to_sql(
            name=self.table_name,
            con=engine,
            schema=self.schema,
            if_exists=self.if_exists,
            index=False
        )
        
        metadata = {
            "table_name": self.table_name,
            "schema": self.schema,
            "rows_loaded": len(input_data),
            "if_exists": self.if_exists,
        }
        
        return TaskResult(True, metadata)