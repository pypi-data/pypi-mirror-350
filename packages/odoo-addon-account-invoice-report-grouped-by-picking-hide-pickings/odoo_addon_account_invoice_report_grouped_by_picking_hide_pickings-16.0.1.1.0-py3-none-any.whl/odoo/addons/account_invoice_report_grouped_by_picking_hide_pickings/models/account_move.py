# Copyright 2024 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models
from odoo.tools import float_compare


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.model
    def _update_lines_grouped_by_picking(self, lines, removed):
        """Updates the invoice lines after removing some of them
        to keep the total quantity consistent,
        by creating correction lines
        or modifying old correction lines's quantity
        """
        # Store the removed qty
        to_update = {}
        precision = self.env["decimal.precision"].precision_get(
            "Product Unit of Measure"
        )
        for line in removed:
            key = line["line"]
            if not to_update.get(key):
                to_update[key] = line["quantity"]
            elif float_compare(
                to_update[key] + line["quantity"], 0, precision_digits=precision
            ):
                to_update[key] += line["quantity"]
            else:
                to_update.pop(key)
        # Update the remaining qty
        for inv_line, qty in to_update.items():
            line_without_picking = list(
                filter(lambda g: not g["picking"] and g["line"] == inv_line, lines)
            )[:1]
            if not line_without_picking:
                lines += [
                    {
                        "picking": self.env["stock.picking"],
                        "line": inv_line,
                        "quantity": qty,
                    }
                ]
            elif line_without_picking[0]["quantity"] + qty == 0:
                lines.remove(line_without_picking[0])
            else:
                i = lines.index(line_without_picking[0])
                lines[i]["quantity"] += qty
        return lines

    def lines_grouped_by_picking(self):
        res = super().lines_grouped_by_picking()
        to_remove = list(filter(lambda g: g["picking"].hide_on_invoice, res))
        if to_remove:
            if to_remove == res:
                res = []
            else:
                for line in to_remove:
                    # Remove hidden pickings
                    res.remove(line)
                if self.env.company.hide_pickings_update_qty:
                    res = self._update_lines_grouped_by_picking(res, to_remove)
        return res
