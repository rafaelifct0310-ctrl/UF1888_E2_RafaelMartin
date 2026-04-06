{
    # ------------------------------------------------------------
    # NOMBRE DEL MÓDULO (visible en Odoo)
    # ------------------------------------------------------------
    'name': 'Ventas ORM Report',

    # ------------------------------------------------------------
    # VERSIÓN DEL MÓDULO
    # Formato habitual: versión_odoo.major.minor.patch
    # ------------------------------------------------------------
    'version': '19.0.1.0.0',

    # ------------------------------------------------------------
    # DESCRIPCIÓN CORTA (aparece en la lista de apps)
    # ------------------------------------------------------------
    'summary': 'Consultas ORM de ventas, clientes y productos más vendidos',

    # ------------------------------------------------------------
    # DESCRIPCIÓN LARGA (explicación del módulo)
    # Se puede usar para documentar qué hace el módulo
    # ------------------------------------------------------------
    'description': '''
Módulo didáctico para Odoo 19 que muestra cómo explotar información
comercial usando únicamente el ORM de Odoo.
''',

    # ------------------------------------------------------------
    # CATEGORÍA (organización dentro de Odoo Apps)
    # ------------------------------------------------------------
    'category': 'Sales/Reporting',

    # ------------------------------------------------------------
    # AUTOR DEL MÓDULO
    # ------------------------------------------------------------
    'author': 'OpenAI',

    # ------------------------------------------------------------
    # LICENCIA
    # LGPL-3 permite reutilización con ciertas condiciones
    # ------------------------------------------------------------
    'license': 'LGPL-3',

    # ------------------------------------------------------------
    # DEPENDENCIAS
    # Este módulo necesita que el módulo 'sale' esté instalado
    # porque usamos modelos como:
    # - sale.order
    # - sale.order.line
    # ------------------------------------------------------------
    'depends': ['sale'],

    # ------------------------------------------------------------
    # ARCHIVOS QUE SE CARGAN AL INSTALAR EL MÓDULO
    # IMPORTANTE: el orden sí influye
    # ------------------------------------------------------------
    'data': [

        # Permisos de acceso (obligatorio si hay modelos nuevos)
        'security/ir.model.access.csv',

        # Vistas (formularios, listas, menús)
        'views/sale_report_orm_views.xml',

        # Plantillas QWeb (estructura del PDF)
        'report/sale_report_orm_templates.xml',

        # Definición del reporte (acción de impresión)
        'report/sale_report_orm_reports.xml',
    ],

    # ------------------------------------------------------------
    # INDICA SI EL MÓDULO SE PUEDE INSTALAR
    # ------------------------------------------------------------
    'installable': True,

    # ------------------------------------------------------------
    # SI ES UNA APLICACIÓN PRINCIPAL O NO
    # False = módulo funcional (no aparece como app principal)
    # ------------------------------------------------------------
    'application': False,
}
