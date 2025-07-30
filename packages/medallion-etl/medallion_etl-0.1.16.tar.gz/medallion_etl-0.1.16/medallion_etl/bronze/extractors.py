"""Extractores para la capa Bronze de Medallion ETL."""

import json
from pathlib import Path
from typing import Any, Dict, Optional
import polars as pl
import requests
from sqlalchemy import create_engine, text

from medallion_etl.core import Task, TaskResult
from medallion_etl.config import config


class FileExtractor(Task[str, pl.DataFrame]):
    """Extractor base para archivos."""
    
    def __init__(
        self, 
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_raw: bool = True
    ):
        super().__init__(name, description)
        self.output_path = output_path or config.bronze_dir
        self.save_raw = save_raw
    
    def save_raw_data(self, file_path: str, data: Any) -> Path:
        """Guarda los datos crudos en el directorio bronze."""
        output_file = self.output_path / Path(file_path).name
        self.output_path.mkdir(parents=True, exist_ok=True)
        
        if isinstance(data, (str, bytes)):
            mode = "wb" if isinstance(data, bytes) else "w"
            with open(output_file, mode) as f:
                f.write(data)
        else:
            with open(output_file, "w") as f:
                json.dump(data, f)
                
        return output_file


class CSVExtractor(FileExtractor):
    """Extractor para archivos CSV."""
    
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_raw: bool = True,
        **csv_options
    ):
        super().__init__(name, description, output_path, save_raw)
        self.csv_options = csv_options
    
    def run(self, input_data: str, **kwargs) -> TaskResult[pl.DataFrame]:
        """Extrae datos de un archivo CSV."""
        # input_data puede ser una ruta a un archivo o una URL
        is_url = input_data.startswith("http") 
        
        if is_url:
            response = requests.get(input_data)
            response.raise_for_status()
            content = response.text
            
            if self.save_raw:
                file_name = input_data.split("/")[-1]
                if not file_name.endswith(".csv"):
                    file_name = f"download_{file_name}.csv"
                saved_path = self.save_raw_data(file_name, content)
            
            df = pl.read_csv(content, **self.csv_options)
        else:
            # Es una ruta de archivo local
            df = pl.read_csv(input_data, **self.csv_options)
            
            if self.save_raw and Path(input_data) != self.output_path:
                saved_path = self.save_raw_data(input_data, open(input_data, "r").read())  # noqa: F841
        
        metadata = {
            "source": input_data,
            "rows": len(df),
            "columns": df.columns,
        }
        
        return TaskResult(df, metadata)


class ParquetExtractor(FileExtractor):
    """Extractor para archivos Parquet."""
    
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_raw: bool = True,
        **parquet_options
    ):
        super().__init__(name, description, output_path, save_raw)
        self.parquet_options = parquet_options
    
    def run(self, input_data: str, **kwargs) -> TaskResult[pl.DataFrame]:
        """Extrae datos de un archivo Parquet."""
        is_url = input_data.startswith("http")
        
        if is_url:
            response = requests.get(input_data)
            response.raise_for_status()
            content = response.content
            
            if self.save_raw:
                file_name = input_data.split("/")[-1]
                if not file_name.endswith(".parquet"):
                    file_name = f"download_{file_name}.parquet"
                saved_path = self.save_raw_data(file_name, content)
            
            # Guardar temporalmente para leer con polars
            temp_file = Path("temp.parquet")
            with open(temp_file, "wb") as f:
                f.write(content)
            
            df = pl.read_parquet(temp_file, **self.parquet_options)
            temp_file.unlink()  # Eliminar archivo temporal
        else:
            # Es una ruta de archivo local
            df = pl.read_parquet(input_data, **self.parquet_options)
            
            if self.save_raw and Path(input_data) != self.output_path:
                saved_path = self.save_raw_data(input_data, open(input_data, "rb").read())  # noqa: F841
        
        metadata = {
            "source": input_data,
            "rows": len(df),
            "columns": df.columns,
        }
        
        return TaskResult(df, metadata)


class APIExtractor(Task[Dict[str, Any], pl.DataFrame]):
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_raw: bool = True,
        method: str = "GET",
        headers: Optional[Dict[str, str]] = None,
        data_key: Optional[str] = None,
        use_mock: bool = False,              
        mock_file: Optional[str] = None      
    ):
        super().__init__(name, description)
        self.output_path = output_path or config.bronze_dir
        self.save_raw = save_raw
        self.method = method.upper()
        self.headers = headers or {}
        self.data_key = data_key
        self.use_mock = use_mock
        self.mock_file = mock_file

    def run(self, input_data: Dict[str, Any], **kwargs) -> TaskResult[pl.DataFrame]:
        if self.use_mock and self.mock_file:
            # Usar JSON mockeado
            with open(self.mock_file, "r") as f:
                json_data = json.load(f)
            print(f"🧪 Usando mock data de {self.mock_file}")
            status_code = 200
        else:
            # Lógica normal de llamada a la API
            url = input_data.get("url")
            if not url:
                raise ValueError("Se requiere una URL en el diccionario de entrada")
            params = input_data.get("params", {})
            body = input_data.get("body", {})
            headers = {**self.headers, **input_data.get("headers", {})}
            response = requests.request(
                method=self.method,
                url=url,
                params=params,
                json=body if self.method in ["POST", "PUT", "PATCH"] else None,
                headers=headers
            )
            response.raise_for_status()
            json_data = response.json()
            status_code = response.status_code
            # Guardar datos crudos si es necesario
            if self.save_raw:
                file_name = f"{self.name or 'api'}_{url.split('/')[-1]}.json"
                self.output_path.mkdir(parents=True, exist_ok=True)
                with open(self.output_path / file_name, "w") as f:
                    json.dump(json_data, f, indent=2)
        # Extraer datos relevantes si se especifica una clave
        if self.data_key:
            data_to_convert = json_data.get(self.data_key, [])
        else:
            data_to_convert = json_data
        # Convertir a DataFrame
        if isinstance(data_to_convert, list):
            df = pl.DataFrame(data_to_convert)
        elif isinstance(data_to_convert, dict):
            df = pl.DataFrame([data_to_convert])
        else:
            raise ValueError(f"No se pueden convertir los datos a DataFrame: {type(data_to_convert)}")
        metadata = {
            "source": self.mock_file if self.use_mock else input_data.get("url"),
            "status_code": status_code,
            "rows": len(df),
            "columns": df.columns,
        }
        return TaskResult(df, metadata)


class SQLExtractor(Task[Dict[str, Any], pl.DataFrame]):
    """Extractor para bases de datos SQL."""
    
    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        output_path: Optional[Path] = None,
        save_raw: bool = True,
        connection_string: Optional[str] = None,
    ):
        super().__init__(name, description)
        self.output_path = output_path or config.bronze_dir
        self.save_raw = save_raw
        self.connection_string = connection_string
    
    def run(self, input_data: Dict[str, Any], **kwargs) -> TaskResult[pl.DataFrame]:
        """Extrae datos de una base de datos SQL."""
        # Obtener la consulta SQL
        query = input_data.get("query")
        if not query:
            raise ValueError("Se requiere una consulta SQL en el diccionario de entrada")
        
        # Obtener la cadena de conexión
        connection_string = input_data.get("connection_string") or self.connection_string
        if not connection_string:
            # Intentar obtener de la configuración
            db_name = input_data.get("db_name")
            if db_name and db_name in config.database_urls:
                connection_string = config.database_urls[db_name]
            else:
                raise ValueError("Se requiere una cadena de conexión")
        
        # Conectar a la base de datos
        engine = create_engine(connection_string)
        
        # Ejecutar la consulta
        with engine.connect() as connection:
            result = connection.execute(text(query))
            rows = result.fetchall()
            columns = result.keys()
        
        # Convertir a DataFrame de Polars
        df = pl.DataFrame({col: [row[i] for row in rows] for i, col in enumerate(columns)})
        
        # Guardar datos crudos si es necesario
        if self.save_raw:
            file_name = f"{self.name or 'sql'}_{input_data.get('db_name', 'query')}.csv"
            self.output_path.mkdir(parents=True, exist_ok=True)
            df.write_csv(self.output_path / file_name)
        
        metadata = {
            "source": connection_string,
            "query": query,
            "rows": len(df),
            "columns": df.columns,
        }
        
        return TaskResult(df, metadata)