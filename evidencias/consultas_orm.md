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
