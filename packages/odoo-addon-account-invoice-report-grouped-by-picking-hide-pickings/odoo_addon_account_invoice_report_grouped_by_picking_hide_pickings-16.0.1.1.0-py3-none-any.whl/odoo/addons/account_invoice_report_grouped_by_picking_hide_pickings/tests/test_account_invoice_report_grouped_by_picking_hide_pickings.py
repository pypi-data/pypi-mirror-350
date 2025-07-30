# Copyright 2025 Alberto Martínez <alberto.martinez@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
# pylint: disable=E501
from odoo.addons.account_invoice_report_grouped_by_picking.tests import (
    test_account_invoice_group_picking,
)

TestAccountInvoiceGroupPicking = (
    test_account_invoice_group_picking.TestAccountInvoiceGroupPicking
)


class SomethingCase(TestAccountInvoiceGroupPicking):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def test_hide_return(self):
        self.sale.order_line[1].unlink()
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"qty_done": 2})
        picking._action_done()
        wiz_return = self.get_return_picking_wizard(picking)
        res = wiz_return.create_returns()
        picking_return = self.env["stock.picking"].browse(res["res_id"])
        picking_return.move_line_ids.write({"qty_done": 2})
        picking_return._action_done()
        picking.copy()
        final_picking = picking.copy()
        final_picking.action_confirm()
        final_picking.move_line_ids.write({"qty_done": 2})
        final_picking._action_done()

        invoice = self.sale._create_invoices()
        (picking + picking_return).write({"hide_on_invoice": True})
        report_lines = invoice.lines_grouped_by_picking()

        self.assertEqual(len(report_lines), 1)
        self.assertEqual(report_lines[0]["quantity"], 2)

    def test_hide_single_picking(self):
        self.sale.order_line[1].unlink()
        self.sale.action_confirm()
        picking = self.sale.picking_ids[:1]
        picking.action_confirm()
        picking.move_line_ids.write({"qty_done": 2})
        picking.write({"hide_on_invoice": True})
        picking._action_done()
        invoice = self.sale._create_invoices()
        invoice.invoice_line_ids.write({"quantity": 5})
        report_lines = invoice.lines_grouped_by_picking()
        self.assertEqual(len(report_lines), 1)
        self.assertEqual(report_lines[0]["quantity"], 5)
