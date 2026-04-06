# Importamos defaultdict para poder agrupar datos fácilmente (similar a un GROUP BY en SQL)
from collections import defaultdict

# Importaciones base de Odoo
from odoo import api, fields, models
# Para lanzar errores controlados al usuario
from odoo.exceptions import UserError


# ============================================================
# MODELO 1: ASISTENTE (WIZARD)
# ============================================================
class SaleReportOrmWizard(models.TransientModel):
    # Nombre técnico del modelo
    _name = 'sale.report.orm.wizard'
    # Descripción visible
    _description = 'Asistente de informe ORM de ventas'
    # Nombre amigable
    _rec_name = 'name'  # ← indicamos que use este campo como nombre

    # Campo calculado, sin store → no necesita columna en BD
    name = fields.Char(
        string='Nombre',
        compute='_compute_name'
    )
    
    @api.depends()
    def _compute_name(self):
        for rec in self:
            rec.name = 'Informe ORM de Ventas'

    # ------------------------------------------------------------
    # CAMPOS DE FILTRO (lo que el usuario rellena en pantalla)
    # ------------------------------------------------------------

    # Fecha inicial para filtrar ventas
    date_from = fields.Date(string='Fecha desde')

    # Fecha final para filtrar ventas
    date_to = fields.Date(string='Fecha hasta')

    # Cliente (relación Many2one con res.partner)
    partner_id = fields.Many2one('res.partner', string='Cliente')

    # Checkbox para cambiar el comportamiento del informe
    only_top_products = fields.Boolean(
        string='Mostrar resumen de productos más vendidos',
        help='Si se activa, el informe agrupa por producto en lugar de mostrar cada línea de venta.'
    )

    # Relación con las líneas del informe (One2many)
    # Este campo almacenará los resultados generados
    line_ids = fields.One2many(
        'sale.report.orm.line',   # modelo destino
        'wizard_id',              # campo inverso
        string='Líneas del informe'
    )

    # Campos calculados (no se guardan directamente en base de datos)
    total_amount = fields.Float(string='Importe total', compute='_compute_totals')
    total_qty = fields.Float(string='Cantidad total', compute='_compute_totals')
    line_count = fields.Integer(string='Número de líneas', compute='_compute_totals')

    # ------------------------------------------------------------
    # MÉTODO COMPUTE: calcula totales automáticamente
    # ------------------------------------------------------------
    @api.depends('line_ids.amount', 'line_ids.qty')
    def _compute_totals(self):
        # Recorremos cada wizard (aunque normalmente será uno)
        for wizard in self:
            # Sumamos todos los importes
            wizard.total_amount = sum(wizard.line_ids.mapped('amount'))

            # Sumamos todas las cantidades
            wizard.total_qty = sum(wizard.line_ids.mapped('qty'))

            # Contamos número de líneas
            wizard.line_count = len(wizard.line_ids)

    # ------------------------------------------------------------
    # CONSTRUCCIÓN DEL DOMINIO (equivalente al WHERE en SQL)
    # ------------------------------------------------------------
    def _build_domain(self):
        self.ensure_one()  # aseguramos que trabajamos con un solo registro

        # Filtro base: solo ventas confirmadas o finalizadas
        domain = [('order_id.state', 'in', ['sale', 'done'])]

        # Si el usuario ha indicado fecha desde
        if self.date_from:
            domain.append(('order_id.date_order', '>=', self.date_from))

        # Si hay fecha hasta → ajustamos a final del día
        if self.date_to:
            domain.append((
                'order_id.date_order',
                '<=',
                fields.Datetime.to_datetime(self.date_to).replace(hour=23, minute=59, second=59)
            ))

        # Si hay cliente seleccionado
        if self.partner_id:
            domain.append(('order_id.partner_id', '=', self.partner_id.id))

        return domain

    # ------------------------------------------------------------
    # ACCIÓN PRINCIPAL: genera el informe
    # ------------------------------------------------------------
    def action_generate(self):
        self.ensure_one()

        # Limpiamos resultados anteriores
        self.line_ids.unlink()

        # Construimos filtros
        domain = self._build_domain()

        # CONSULTA ORM (equivalente a SELECT)
        # ANTES (incorrecto en Odoo 19):
        # sale_lines = self.env['sale.order.line'].search(
        #     domain,
        #     order='order_id.date_order desc, id desc'
        # )
        # AHORA (correcto en Odoo 19):
        sale_lines = self.env['sale.order.line'].search(
            domain,
            order='order_id desc, id desc'
        )

        # Si no hay datos → error para el usuario
        if not sale_lines:
            raise UserError('No se encontraron líneas de venta con los filtros indicados.')

        # ------------------------------------------------------------
        # MODO 1: AGRUPADO (productos más vendidos)
        # ------------------------------------------------------------
        if self.only_top_products:

            # Diccionario para agrupar datos
            grouped = defaultdict(lambda: {
                'qty': 0.0,
                'amount': 0.0,
                'partner_id': False,
                'date_order': False,
            })

            # Recorremos cada línea de venta
            for line in sale_lines:
                key = line.product_id.id  # agrupamos por producto

                # Sumamos cantidades
                grouped[key]['qty'] += line.product_uom_qty

                # Sumamos importes
                grouped[key]['amount'] += line.price_subtotal

                # Guardamos una fecha (la primera encontrada)
                if not grouped[key]['date_order']:
                    grouped[key]['date_order'] = line.order_id.date_order

            # Convertimos el diccionario en registros Odoo
            values = []
            for product_id, data in grouped.items():
                values.append({
                    'wizard_id': self.id,
                    'product_id': product_id,
                    'qty': data['qty'],
                    'amount': data['amount'],
                    'date_order': data['date_order'],
                    'is_grouped': True,
                })

            # Creamos las líneas en base de datos
            self.env['sale.report.orm.line'].create(values)

        # ------------------------------------------------------------
        # MODO 2: DETALLE (línea por línea)
        # ------------------------------------------------------------
        else:
            values = []

            for line in sale_lines:
                values.append({
                    'wizard_id': self.id,

                    # Navegación ORM (equivalente a JOIN)
                    'partner_id': line.order_id.partner_id.id,
                    'product_id': line.product_id.id,

                    # Datos de la línea
                    'qty': line.product_uom_qty,
                    'amount': line.price_subtotal,
                    'date_order': line.order_id.date_order,

                    # Información adicional
                    'order_name': line.order_id.name,

                    'is_grouped': False,
                })

            # Creamos registros
            self.env['sale.report.orm.line'].create(values)

        # ------------------------------------------------------------
        # DEVOLVEMOS LA VISTA DEL WIZARD
        # ------------------------------------------------------------
        return {
            'type': 'ir.actions.act_window',
            'name': 'Informe ORM de ventas',
            'res_model': 'sale.report.orm.wizard',
            'view_mode': 'form',
            'res_id': self.id,
            'target': 'current',
        }

    # ------------------------------------------------------------
    # ACCIÓN PARA GENERAR PDF
    # ------------------------------------------------------------
    def action_print_pdf(self):
        self.ensure_one()

        # Si no hay datos, generamos primero
        if not self.line_ids:
            self.action_generate()

        # Llamamos al reporte QWeb
        return self.env.ref('ventas_orm_report.action_report_sale_report_orm').report_action(self)

    # ------------------------------------------------------------
    # ACCIÓN PARA ABRIR EL WIZARD
    # ------------------------------------------------------------
    def action_open_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Informe ORM de ventas',
            'res_model': 'sale.report.orm.wizard',
            'view_mode': 'form',
            'target': 'current',
        }


# ============================================================
# MODELO 2: LÍNEAS DEL INFORME
# ============================================================
class SaleReportOrmLine(models.TransientModel):
    _name = 'sale.report.orm.line'
    _description = 'Línea de informe ORM de ventas'

    # Orden por defecto (más recientes primero)
    _order = 'date_order desc, id desc'

    # Relación con el wizard
    wizard_id = fields.Many2one(
        'sale.report.orm.wizard',
        required=True,
        ondelete='cascade'
    )

    # Cliente
    partner_id = fields.Many2one('res.partner', string='Cliente')

    # Producto
    product_id = fields.Many2one('product.product', string='Producto', required=True)

    # Cantidad vendida
    qty = fields.Float(string='Cantidad')

    # Importe de la línea
    amount = fields.Float(string='Importe')

    # Fecha del pedido
    date_order = fields.Datetime(string='Fecha')

    # Referencia del pedido
    order_name = fields.Char(string='Pedido')

    # Indica si la línea está agrupada
    is_grouped = fields.Boolean(string='Agrupado por producto')