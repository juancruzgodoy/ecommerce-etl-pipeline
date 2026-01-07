# E-commerce Data Pipeline (ETL)

Este proyecto simula un proceso **ETL (Extract, Transform, Load)** completo para una empresa de E-commerce. 
El objetivo es ingerir datos crudos de ventas, limpiarlos, transformarlos para obtener métricas de negocio y cargarlos en formatos optimizados para su posterior análisis.

## Tecnologías Utilizadas

* **Python 3.10+**: Lenguaje principal.
* **Pandas**: Procesamiento de datos en memoria.
* **AWS S3**: Almacenamiento en la nube (Data Lake).
* **Docker**: Reproducible en cualquier entorno
* **Boto3 / s3fs**: Conexión y manipulación de objetos en S3.
* **PyArrow**: Motor para escritura eficiente de archivos Parquet.
* **Python-Dotenv**: Gestión de variables de entorno y secretos.

## Arquitectura del Pipeline

El script `etl.py` ejecuta los siguientes pasos secuenciales:

### 1. Extract (Raw Layer)
El script se conecta a un Bucket S3 y lee los archivos CSV crudos directamente desde la carpeta `raw/` utilizando `s3fs`.

### 2. Transform (Transformación y Limpieza)
* **Manejo de Nulos:** Estrategia de rellenado (*fillna*) para no perder registros históricos (ej: promociones vacías).
* **Normalización de Tipos:** Conversión de fechas a objetos `datetime` y optimización de memoria usando tipos `category` para campos repetitivos.
* **Enriquecimiento de Datos (Joins):** Cruce de tablas entre *Items* y *Productos* (`pd.merge`) para agregar nombres y detalles al registro de ventas.

### 3. Business Logic (Lógica de Negocio)
Se programó la lógica para responder preguntas clave de la gerencia:
* **Top Clientes:** Identificación de los 5 usuarios con mayor volumen de compra histórico.
* **Producto Estrella:** Determinación del artículo más vendido por cantidad unitaria.
* **Tendencias:** Análisis de la evolución de ingresos mes a mes (Agrupación temporal).

### 4. Load (Carga)
Los resultados se escriben directamente en la carpeta `processed/` del Bucket S3 en dos formatos:
* **Reportes en CSV:** Para consumo directo del equipo de negocio/Excel.
* **Tablas Limpias en Parquet:** Formato columnar comprimido, optimizado para futuros procesos de Big Data o Machine Learning.

---

## Estructura del Proyecto

```text
├── venv/              # Entorno virtual - Ignorado en git
├── .dockerignore      # Archivos excluidos del contexto de Docker
├── .gitignore         # Configuración de archivos ignorados
├── config.py          # Configuración de infraestructura y rutas S3
├── Dockerfile         # Definición de la imagen Docker para el pipeline
├── etl.py             # Script principal del pipeline
├── README.md          # Documentación del proyecto
└── requirements.txt   # Lista de dependencias del proyecto
```
# Cómo ejecutar este proyecto

Sigue estos pasos para correr el pipeline en tu entorno local:

1.  **Clonar el repositorio:**
    ```bash
    git clone [https://github.com/juancruzgodoy/ecommerce-etl-pipeline](https://github.com/juancruzgodoy/ecommerce-etl-pipeline)
    cd ecommerce-etl-pipeline
    ```

2.  **Crear y activar un entorno virtual:**
    Es recomendable para aislar las librerías del proyecto.
    ```bash
    # Windows
    python -m venv venv
    .\venv\Scripts\activate

    # Mac/Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instalar dependencias:**
    Ahora utilizamos `requirements.txt` para instalar todo lo necesario (Pandas, S3fs, PyArrow, Dotenv, etc.).
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configurar Variables de Entorno (.env):**
    Crea un archivo llamado `.env` en la raíz del proyecto y agrega tus credenciales de AWS (este archivo es ignorado por git por seguridad).

    ```env
    AWS_ACCESS_KEY_ID=tu_access_key_aqui
    AWS_SECRET_ACCESS_KEY=tu_secret_key_aqui
    AWS_BUCKET_NAME=nombre-de-tu-bucket
    ```

5.  **Ejecutar el pipeline:**
    ```bash
    python etl.py
    ```
    *Verás los logs en la terminal indicando la conexión a AWS. Los archivos procesados y reportes aparecerán automáticamente en la carpeta `processed/` de tu bucket S3.*

## Cómo correr con Docker

Si no querés instalar Python ni configurar entornos, podés correr este proyecto usando Docker.

1. **Construir la imagen:**
   ```bash
   docker build -t etl-image .
   ```

2. **Ejecutar el ETL:** Este comando corre el script y guarda los resultados en tu carpeta output local.

    ```bash
    docker run -v ${PWD}/output:/app/output etl-image
    ```
