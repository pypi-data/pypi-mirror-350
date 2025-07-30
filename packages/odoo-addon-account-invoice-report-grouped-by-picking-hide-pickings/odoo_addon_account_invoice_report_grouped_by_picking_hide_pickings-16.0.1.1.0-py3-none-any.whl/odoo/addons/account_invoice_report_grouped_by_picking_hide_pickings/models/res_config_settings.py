# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    hide_return_pickings_default = fields.Boolean(
        related="company_id.hide_return_pickings_default",
        readonly=False,
    )
    hide_pickings_update_qty = fields.Boolean(
        related="company_id.hide_pickings_update_qty",
        readonly=False,
    )
