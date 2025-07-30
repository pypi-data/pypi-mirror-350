"""Definiciones para pipelines en Medallion ETL."""

from typing import List, Optional, Callable, TypeVar, Generic, Any
from prefect import flow

from medallion_etl.core.task import Task, TaskResult

# Tipos genéricos para entrada/salida
T = TypeVar('T')
U = TypeVar('U')


class Pipeline(Generic[T, U]):
    """Pipeline que encadena múltiples tareas para procesar datos."""
    
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description
        self.tasks: List[Task] = []
        self._prefect_flow: Optional[Any] = None
    
    def add_task(self, task: Task) -> 'Pipeline':
        """Añade una tarea al pipeline."""
        self.tasks.append(task)
        return self
    
    def run(self, input_data: T, **kwargs) -> TaskResult[U]:
        """Ejecuta el pipeline completo con los datos de entrada."""
        current_data = input_data
        current_metadata = {}
        
        for i, task in enumerate(self.tasks):
            task_name = task.name
            try:
                result = task(current_data, **kwargs)
                current_data = result.data
                
                # Acumular metadatos
                task_metadata = {f"{task_name}.{k}": v for k, v in result.metadata.items()}
                current_metadata.update(task_metadata)
                
            except Exception as e:
                # Registrar el error y propagar la excepción
                error_msg = f"Error en tarea {task_name} (paso {i+1}/{len(self.tasks)}): {str(e)}"
                raise RuntimeError(error_msg) from e
        
        return TaskResult(current_data, current_metadata)
    
    def as_prefect_flow(self, **flow_kwargs) -> Callable:
        """Convierte este pipeline en un flow de Prefect."""
        if self._prefect_flow is None:
            flow_kwargs.setdefault("name", self.name)
            flow_kwargs.setdefault("description", self.description)
            
            @flow(**flow_kwargs)
            def _flow_wrapper(input_data: T, **kwargs) -> U:
                result = self.run(input_data, **kwargs)
                return result.data
            
            self._prefect_flow = _flow_wrapper
        
        return self._prefect_flow


class MedallionPipeline(Pipeline):
    """Pipeline especializado para la arquitectura medallion (Bronze-Silver-Gold)."""
    
    def __init__(self, name: str, description: Optional[str] = None):
        super().__init__(name, description)
        self.bronze_tasks: List[Task] = []
        self.silver_tasks: List[Task] = []
        self.gold_tasks: List[Task] = []
    
    def add_bronze_task(self, task: Task) -> 'MedallionPipeline':
        """Añade una tarea a la capa Bronze."""
        self.bronze_tasks.append(task)
        self.tasks.append(task)
        return self
    
    def add_silver_task(self, task: Task) -> 'MedallionPipeline':
        """Añade una tarea a la capa Silver."""
        self.silver_tasks.append(task)
        self.tasks.append(task)
        return self
    
    def add_gold_task(self, task: Task) -> 'MedallionPipeline':
        """Añade una tarea a la capa Gold."""
        self.gold_tasks.append(task)
        self.tasks.append(task)
        return self