# E-commerce Data Pipeline (ETL)

Este proyecto simula un proceso **ETL (Extract, Transform, Load)** completo para una empresa de E-commerce. 
El objetivo es ingerir datos crudos de ventas, limpiarlos, transformarlos para obtener métricas de negocio y cargarlos en formatos optimizados para su posterior análisis.

## Tecnologías Utilizadas
* **Python 3.x**: Lenguaje principal.
* **Pandas**: Manipulación y análisis de datos.
* **PyArrow/Parquet**: Almacenamiento columnar eficiente.

## Arquitectura del Pipeline

El script `etl.py` ejecuta los siguientes pasos secuenciales:

### 1. Extract (Extracción)
* Ingesta de datos desde archivos CSV crudos (`orders`, `order_items`, `products`).
* Verificación inicial de estructuras y tipos de datos.

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
Generación de dos tipos de salidas en la carpeta `output/`:
* **Reportes en CSV:** Para consumo directo del equipo de negocio/Excel.
* **Tablas Limpias en Parquet:** Formato columnar comprimido, optimizado para futuros procesos de Big Data o Machine Learning.

---

## Estructura del Proyecto

```text
├── data/                  # Archivos CSV de entrada (Source)
├── output/                # Archivos generados por el script (Target) - Ignorado en git
├── venv/                  # Entorno virtual - Ignorado en git
├── etl.py                 # Script principal del pipeline
├── .gitignore             # Configuración de archivos ignorados
└── README.md              # Documentación del proyecto
```
## Cómo ejecutar este proyecto

Sigue estos pasos para correr el pipeline en tu entorno local:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/TU_USUARIO/ecommerce-etl-pipeline.git](https://github.com/TU_USUARIO/ecommerce-etl-pipeline.git)
   cd ecommerce-etl-pipeline
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate

   # Mac/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install pandas pyarrow
   ```

4. **Ejecutar el pipeline:**
   ```bash
   python etl.py
   ```
   *Verás los logs en la terminal y los archivos generados aparecerán automáticamente en la carpeta `output/`.*
