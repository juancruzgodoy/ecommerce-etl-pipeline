import os
from dotenv import load_dotenv

# Cargo las variables del .env
load_dotenv()

# Configuración de AWS S3
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")

RAW_PREFIX = f"s3://{AWS_BUCKET_NAME}/raw"
PROCESSED_PREFIX = f"s3://{AWS_BUCKET_NAME}/processed"

# Rutas de los archivos en S3
PATH_ORDERS = f'{RAW_PREFIX}/ecommerce_orders.csv'
PATH_ITEMS = f'{RAW_PREFIX}/ecommerce_order_items.csv'
PATH_PRODUCTS = f'{RAW_PREFIX}/ecommerce_products.csv'

# Rutas de salida procesadas csv
PATH_PROCESSED_ORDERS_CSV = f'{PROCESSED_PREFIX}/ecommerce_orders.csv'
PATH_PROCESSED_ITEMS_CSV = f'{PROCESSED_PREFIX}/ecommerce_order_items.csv'
PATH_PROCESSED_PRODUCTS_CSV = f'{PROCESSED_PREFIX}/ecommerce_products.csv'

# Reportes procesados csv
PATH_REPORT_CLIENTES_CSV = f'{PROCESSED_PREFIX}/reporte_clientes_top5.csv'
PATH_REPORT_PRODUCTO_CSV = f'{PROCESSED_PREFIX}/reporte_producto_mas_vendido.csv'
PATH_REPORT_VENTAS_MENSUAL_CSV = f'{PROCESSED_PREFIX}/reporte_ventas_mensual.csv'

# Rutas de salida procesadas parquet
PATH_PROCESSED_ORDERS_PARQUET = f'{PROCESSED_PREFIX}/ecommerce_orders.parquet'
PATH_PROCESSED_ITEMS_PARQUET = f'{PROCESSED_PREFIX}/ecommerce_order_items.parquet'
PATH_PROCESSED_PRODUCTS_PARQUET = f'{PROCESSED_PREFIX}/ecommerce_products.parquet'

# Reportes procesados parquet
PATH_REPORT_CLIENTES_PARQUET = f'{PROCESSED_PREFIX}/reporte_clientes_top5.parquet'
PATH_REPORT_PRODUCTO_PARQUET = f'{PROCESSED_PREFIX}/reporte_producto_mas_vendido.parquet'
PATH_REPORT_VENTAS_MENSUAL_PARQUET = f'{PROCESSED_PREFIX}/reporte_ventas_mensual.parquet'