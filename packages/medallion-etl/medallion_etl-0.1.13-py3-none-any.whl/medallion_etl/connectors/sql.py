"""Conectores SQL para Medallion ETL."""

from typing import Any, Dict, List, Optional
from sqlalchemy import create_engine, text, Table, MetaData
from sqlalchemy.engine import Engine
import polars as pl

from medallion_etl.connectors.base import Connector


class SQLConnector(Connector):
    """Conector para bases de datos SQL."""
    
    def __init__(
        self,
        connection_string: str,
        name: Optional[str] = None,
        description: Optional[str] = None,
    ):
        super().__init__(name or "SQLConnector", description)
        self.connection_string = connection_string
        self._engine = None
    
    def connect(self) -> Engine:
        """Establece una conexión con la base de datos."""
        if self._engine is None:
            self._engine = create_engine(self.connection_string)
        return self._engine
    
    def close(self) -> None:
        """Cierra la conexión con la base de datos."""
        if self._engine is not None:
            self._engine.dispose()
            self._engine = None
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Ejecuta una consulta SQL y devuelve los resultados."""
        engine = self.connect()
        with engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            columns = result.keys()
            rows = result.fetchall()
            return [{col: row[i] for i, col in enumerate(columns)} for row in rows]
    
    def query_to_dataframe(self, query: str, params: Optional[Dict[str, Any]] = None) -> pl.DataFrame:
        """Ejecuta una consulta SQL y devuelve un DataFrame de Polars."""
        engine = self.connect()
        with engine.connect() as connection:
            result = connection.execute(text(query), params or {})
            columns = result.keys()
            rows = result.fetchall()
            
            # Convertir a DataFrame de Polars
            data = {col: [row[i] for row in rows] for i, col in enumerate(columns)}
            return pl.DataFrame(data)
    
    def load_dataframe(self, df: pl.DataFrame, table_name: str, schema: Optional[str] = None, if_exists: str = "append") -> int:
        """Carga un DataFrame en una tabla SQL."""
        engine = self.connect()
        pandas_df = df.to_pandas()
        pandas_df.to_sql(name=table_name, con=engine, schema=schema, if_exists=if_exists, index=False)
        return len(df)
    
    def get_table_schema(self, table_name: str, schema: Optional[str] = None) -> Dict[str, Any]:
        """Obtiene el esquema de una tabla."""
        engine = self.connect()
        metadata = MetaData()
        table = Table(table_name, metadata, schema=schema, autoload_with=engine)
        
        columns = {}
        for column in table.columns:
            columns[column.name] = {
                "type": str(column.type),
                "nullable": column.nullable,
                "primary_key": column.primary_key,
            }
        
        return {
            "table_name": table_name,
            "schema": schema,
            "columns": columns,
        }