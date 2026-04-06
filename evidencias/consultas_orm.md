# Consutlas usando el ORM de Odoo 19
**Accede a la BBDD usando modelos de Odoo en Python**

### Modelos que intervienen
- Para ventas:
    - sale.order
    - sale.order.line
    - res.partner
    - product.product

---
#### Ejemplo consulta ORM sencilla de ventas
```python
ventas = self.env['sale.order'].search([
    ('state', 'in', ['sale'. 'done'])
], order='date_order desc')
```
- explicación: 
    - self.env['sale.order'] -> accede al modelo
    - .search([...]) -> busca los registros que cumplan la condición
    - ('state', 'in', ['sale'. 'done']) -> filtra pedidos confirmados o finalizados
    - order='date_order desc' -> ordena por fecha descendente

##### Recorrer resultados ORM
```python
for venta in ventas:
    print(venta.name, venta.partner_id.name, venta.date_order, venta.amount_total)
```
- Con ORM no necesitas hacer JOIN

##### Obtener líneas con cliente, producto, imnporte y fecha
```python
lineas = self.env['sale.order.line'].search([
    ('order_id.state', 'in', ['sale', 'done'])
])
```
##### Recorrer los resultados
```python
for line in lineas:
    cliente = linea.order_id.partner_id.name
    producto = linea.product_id.display_name
    importe = linea.price_subtotal
    fecha = linea.order_id.date_order
    print(cliente, producto, importe, fecha)
```
