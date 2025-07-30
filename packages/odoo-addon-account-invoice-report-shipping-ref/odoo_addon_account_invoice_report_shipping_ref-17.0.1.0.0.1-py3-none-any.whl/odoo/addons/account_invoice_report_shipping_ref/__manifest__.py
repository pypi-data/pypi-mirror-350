# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Account Invoice Report Shipping Ref",
    "version": "17.0.1.0.0",
    "category": "Account",
    "website": "https://github.com/sygel-technology/sy-account-invoice-reporting",
    "summary": "Shows delivery address reference on report invoice",
    "author": "Sygel, Odoo Community Association (OCA)",
    "depends": ["account"],
    "data": [
        "report/report_invoice.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "AGPL-3",
}
