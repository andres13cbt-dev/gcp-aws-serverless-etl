SELECT 
    CAST(id AS STRING) AS id_producto,
    title AS nombre_producto,
    category AS categoria,
    'Venta Directa Colombia' AS modelo_negocio,
    price AS precio_venta,
    CURRENT_TIMESTAMP() AS fecha_extraccion
FROM 
    `{PROJECT_ID}.{DATASET}.{TABLE_RAW}`
WHERE 
    price > 50  -- Simula la regla de negocio