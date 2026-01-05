import pandas as pd
import s3fs
import config as c

# 1. Cargar
print("Cargando datos...")
df_orders = pd.read_csv(c.PATH_ORDERS)
df_items = pd.read_csv(c.PATH_ITEMS)
df_products = pd.read_csv(c.PATH_PRODUCTS)

#2. Explorar
print("\n--- ORDERS ---")
print(df_orders.info()) # Ver nulos y tipos de datos
print(df_orders.head()) # Ver las primeras filas

print("\n--- ITEMS (Detalle de productos por orden) ---")
print(df_items.info())
print(df_items.head())

#3. Limpiar

# Verificar nulos
print("\n--- NULOS ---")
print("\nOrders:")
print(df_orders.isnull().sum())
print("\nItems:")
print(df_items.isnull().sum())
print("\nProducts:")
print(df_products.isnull().sum())

# Como solo orders tiene nulos y no son errores los relleno
df_orders["promotion_id"] = df_orders["promotion_id"].fillna(value =  "Sin codigo")
df_orders["notes"] = df_orders["notes"].fillna(value =  "Sin notas")
print("\n--- NULOS DESPUÉS DE RELLENAR ---")
print(df_orders.isnull().sum())

# Verificar duplicados
duplicados_orders = df_orders.duplicated().sum()
duplicados_items = df_items.duplicated().sum()
duplicados_products = df_products.duplicated().sum()

print("\n--- DUPLICADOS ---")
print(f"Orders: {duplicados_orders}")
print(f"Items: {duplicados_items}")
print(f"Products: {duplicados_products}")

# Corregir tipos de datos
# Order
df_orders["order_date"] = df_orders["order_date"].astype("datetime64[ns]") # Convertir a fecha
# Categorizar variables
df_orders["status"] = df_orders["status"].astype("category")
df_orders["payment_method"] = df_orders["payment_method"].astype("category")
df_orders["shipping_method"] = df_orders["shipping_method"].astype("category")
print(df_orders.info())

# Preguntas de negocio

# 1. TOP 5 clientes que mas han gastado
reporte_clientes = df_orders.groupby("customer_id")["total_amount"].sum()
print("\n--- TOP 5 CLIENTES QUE MÁS HAN GASTADO ---")
print(reporte_clientes.sort_values(ascending=False).head(5))

# 2. Producto más vendido (En cantidad)

reporte_ventas = pd.merge(df_items, df_products, on="product_id", how="left").groupby("product_name")["quantity"].sum()
print("\n--- PRODUCTO MÁS VENDIDO (EN CANTIDAD) ---")
print(reporte_ventas.sort_values(ascending=False).head(1))

# 3. Evolucion de las ventas mes a mes

df_orders_aux = df_orders.copy() # Hago una copia para no modificar el original
df_orders_aux["order_date"] = df_orders["order_date"].dt.to_period("M")
reporte_mensual = df_orders_aux.groupby("order_date")["total_amount"].sum()
print("\n--- EVOLUCIÓN DE LAS VENTAS MES A MES ---")
print(reporte_mensual)

# Guardo todo en CSVs
df_orders.to_csv(c.PATH_PROCESSED_ORDERS_CSV, index=False)
df_items.to_csv(c.PATH_PROCESSED_ITEMS_CSV, index=False)
df_products.to_csv(c.PATH_PROCESSED_PRODUCTS_CSV, index=False)
reporte_clientes.to_csv(c.PATH_REPORT_CLIENTES_CSV)
reporte_ventas.to_csv(c.PATH_REPORT_PRODUCTO_CSV)
reporte_mensual.to_csv(c.PATH_REPORT_VENTAS_MENSUAL_CSV)

# Guardo todo en parquet

# Asegurar que promotion_id es string para evitar problemas
df_orders['promotion_id'] = df_orders['promotion_id'].astype(str)
df_orders.to_parquet(c.PATH_PROCESSED_ORDERS_PARQUET, index=False)

df_items.to_parquet(c.PATH_PROCESSED_ITEMS_PARQUET, index=False)
df_products.to_parquet(c.PATH_PROCESSED_PRODUCTS_PARQUET, index=False)

# A los reportes los tengo que convertir a DataFrame para guardarlos bien
# Reporte 1: Top Clientes
reporte_clientes.to_frame(name="total_gastado").to_parquet(c.PATH_REPORT_CLIENTES_PARQUET)

# Reporte 2: Producto más vendido
reporte_ventas.to_frame(name="cantidad").to_parquet(c.PATH_REPORT_PRODUCTO_PARQUET)

# Reporte 3: Ventas Mensuales
df_mensual = reporte_mensual.to_frame(name="total_ventas")
# Convierto el indice a string para evitar problemas al guardar
df_mensual.index = df_mensual.index.astype(str)
df_mensual.to_parquet(c.PATH_REPORT_VENTAS_MENSUAL_PARQUET)