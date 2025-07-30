# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, exceptions, fields, models


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    hide_return_on_invoice = fields.Boolean(
        string="Hide return on invoice report",
        help="Marking this option will hide the return "
        "and the returned pickings from the invoice report",
        default=lambda self: self.env.company.hide_return_pickings_default,
    )

    is_full_return = fields.Boolean(
        string="It is Full Return", compute="_compute_is_full_return"
    )

    @api.depends("product_return_moves", "product_return_moves.quantity")
    def _compute_is_full_return(self):
        self.is_full_return = len(self.picking_id.move_ids) == len(
            self.product_return_moves
        ) and False not in self.product_return_moves.mapped(
            lambda m: m.move_id and m.quantity == m.move_id.quantity_done
        )

    def create_returns(self):
        res = super().create_returns()
        if self.hide_return_on_invoice:
            if self.is_full_return:
                new_picking = self.env["stock.picking"].browse(res["res_id"])
                (self.picking_id | new_picking).write({"hide_on_invoice": True})
            else:
                raise exceptions.ValidationError(
                    _("You can only mark full returns as internal")
                )
        return res
