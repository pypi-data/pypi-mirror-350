"""Definiciones base para tareas en Medallion ETL."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Generic, Optional, TypeVar, Callable
import polars as pl
from prefect import task

from medallion_etl.config import config

# Tipo genérico para los datos de entrada/salida
T = TypeVar('T')
U = TypeVar('U')


class TaskResult(Generic[T]):
    """Resultado de una tarea con metadatos."""
    
    def __init__(self, data: T, metadata: Optional[Dict[str, Any]] = None):
        self.data = data
        self.metadata = metadata or {}
    
    def with_metadata(self, **kwargs) -> 'TaskResult[T]':
        """Añade metadatos adicionales al resultado."""
        self.metadata.update(kwargs)
        return self


class Task(Generic[T, U], ABC):
    """Clase base para todas las tareas en Medallion ETL."""
    
    def __init__(self, name: Optional[str] = None, description: Optional[str] = None):
        self.name = name or self.__class__.__name__
        self.description = description
        self._prefect_task: Optional[Any] = None
    
    @abstractmethod
    def run(self, input_data: T, **kwargs) -> TaskResult[U]:
        """Ejecuta la tarea con los datos de entrada proporcionados."""
        pass
    
    def __call__(self, input_data: T, **kwargs) -> TaskResult[U]:
        """Permite llamar a la tarea como una función."""
        return self.run(input_data, **kwargs)
    
    def as_prefect_task(self, **task_kwargs) -> Callable:
        """Convierte esta tarea en una tarea de Prefect."""
        if self._prefect_task is None:
            task_kwargs.setdefault("name", self.name)
            task_kwargs.setdefault("description", self.description)
            task_kwargs.setdefault("retries", config.max_retries)
            task_kwargs.setdefault("retry_delay_seconds", config.retry_delay_seconds)
            
            @task(**task_kwargs)
            def _task_wrapper(input_data: T, **kwargs) -> U:
                result = self.run(input_data, **kwargs)
                return result.data
            
            self._prefect_task = _task_wrapper
        
        return self._prefect_task


class DataFrameTask(Task[pl.DataFrame, pl.DataFrame]):
    """Tarea base para operaciones con DataFrames de Polars."""
    
    @abstractmethod
    def process_dataframe(self, df: pl.DataFrame, **kwargs) -> pl.DataFrame:
        """Procesa un DataFrame de Polars."""
        pass
    
    def run(self, input_data: pl.DataFrame, **kwargs) -> TaskResult[pl.DataFrame]:
        """Ejecuta la tarea con un DataFrame de entrada."""
        result_df = self.process_dataframe(input_data, **kwargs)
        metadata = {
            "input_rows": len(input_data),
            "output_rows": len(result_df),
            "columns": result_df.columns,
        }
        return TaskResult(result_df, metadata)