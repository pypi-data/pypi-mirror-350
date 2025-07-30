# Copyright 2025 Ángel Rivas <angel.rivas@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    invoice_shipping_ref_label = fields.Char(
        string="Invoice Shipping Ref. Label",
        related="company_id.invoice_shipping_ref_label",
        readonly=False,
    )
