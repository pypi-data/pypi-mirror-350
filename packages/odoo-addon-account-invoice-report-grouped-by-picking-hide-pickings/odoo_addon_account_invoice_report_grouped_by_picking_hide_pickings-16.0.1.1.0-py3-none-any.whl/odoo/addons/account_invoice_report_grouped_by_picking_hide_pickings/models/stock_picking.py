# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    hide_on_invoice = fields.Boolean(
        string="Hide on Invoice",
        default=False,
        copy=False,
    )
