# Medallion ETL

Una librería modular para construir data pipelines con arquitectura medallion (Bronze-Silver-Gold).

## Características

- Arquitectura medallion (Bronze-Silver-Gold) para procesamiento de datos
- Interfaz simple para definir nuevos pipelines
- Funciones reutilizables para cada capa del proceso
- Modularidad clara entre extracción, validación y carga
- Compatibilidad con SQLAlchemy para persistencia en bases de datos
- Integración con Prefect para orquestación de flujos
- Validación de datos con Pydantic
- Procesamiento eficiente con Polars

## Requisitos

- Python 3.11+
- polars>=1.30
- pydantic>=2.7
- sqlalchemy>=2.0
- prefect>=2.0

## Instalación

```bash
pip install medallion-etl
```

O desde el código fuente:

```bash
git clone https://github.com/usuario/medallion-etl.git
cd medallion-etl
pip install -e .
```

## Estructura de la librería

```
medallion_etl/
├── bronze/            # Capa de ingesta de datos crudos
├── silver/            # Capa de validación y limpieza
├── gold/              # Capa de transformación y agregación
├── core/              # Componentes centrales de la librería
├── pipelines/         # Definición de flujos completos
├── schemas/           # Modelos Pydantic para validación
├── connectors/        # Conectores para diferentes fuentes/destinos
├── utils/             # Utilidades generales
├── config/            # Configuraciones
└——— templates/         # Plantillas para nuevos pipelines
```

## Uso básico

### Crear un pipeline simple

```python
from medallion_etl.core import MedallionPipeline
from medallion_etl.bronze import CSVExtractor
from medallion_etl.silver import SchemaValidator
from medallion_etl.gold import Aggregator
from medallion_etl.schemas import BaseSchema

# Definir esquema de datos
class UserSchema(BaseSchema):
    id: int
    name: str
    age: int
    email: str

# Crear pipeline
pipeline = MedallionPipeline(name="UserPipeline")

# Agregar tareas
pipeline.add_bronze_task(CSVExtractor(name="UserExtractor"))
pipeline.add_silver_task(SchemaValidator(schema_model=UserSchema))
pipeline.add_gold_task(Aggregator(group_by=["age"], aggregations={"id": "count"}))

# Ejecutar pipeline
result = pipeline.run("data/users.csv")
print(result.metadata)
```

### Usar con Prefect

```python
from medallion_etl.core import MedallionPipeline
from medallion_etl.bronze import CSVExtractor

# Crear pipeline
pipeline = MedallionPipeline(name="SimplePipeline")
pipeline.add_bronze_task(CSVExtractor())

# Convertir a flow de Prefect
flow = pipeline.as_prefect_flow()

# Ejecutar flow
flow("data/sample.csv")
```

## Ejemplos

Consulta la carpeta `examples/` para ver ejemplos completos de pipelines:

- `weather_pipeline.py`: Pipeline para procesar datos meteorológicos
- `sales_etl_pipeline.py`: Pipeline ETL para datos de ventas

## Contribuir

Las contribuciones son bienvenidas! Por favor, siente libre de enviar un Pull Request.

## Licencia

MIT