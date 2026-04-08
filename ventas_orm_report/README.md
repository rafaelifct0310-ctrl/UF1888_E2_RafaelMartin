# Ventas ORM Report para Odoo 19

Módulo para mostrar consultas de ventas usando **ORM** en Odoo 19.

## Qué hace

- Añade un menú: **Consultas ORM > Informe de ventas**
- Permite filtrar por:
  - fecha desde
  - fecha hasta
  - cliente
- Tiene dos modos:
  - detalle de líneas de venta
  - resumen de productos más vendidos
- Muestra resultados en pantalla
- Permite imprimir PDF
- Desde la lista, el usuario puede usar la exportación estándar de Odoo a CSV/Excel

## Instalación

1. Copiar la carpeta `ventas_orm_report` al directorio de addons personalizados (/opt/odoo/odoo/custom_addons).
2. Reiniciar Odoo.
3. Actualizar lista de aplicaciones.
4. Instalar el módulo **Ventas ORM Report**.

## Ruta funcional

**Consultas ORM > Informe de ventas**

## Recordatorio

El módulo trabaja con el modelo `sale.order.line` usando el ORM de Odoo:

- `search()` para recuperar datos
- navegación relacional, por ejemplo:
  - `line.order_id.partner_id.name`
  - `line.product_id.display_name`
- agrupación manual en Python para productos más vendidos
