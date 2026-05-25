# Copyright 2026 NuoBiT Solutions SL - Eric Antones <eantones@nuobit.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models

FUNERAL_DETAIL_FIELDS = (
    "funeral_deceased_name",
    "funeral_home",
    "funeral_delivery_city",
    "funeral_delivery_state",
    "funeral_delivery_notes",
    "funeral_condolence_ribbon",
    "funeral_add_card",
    "funeral_condolence_card",
)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    funeral_deceased_name = fields.Char(string="Deceased Name")
    funeral_home = fields.Char()
    funeral_delivery_city = fields.Char(string="Delivery City")
    funeral_delivery_state = fields.Char(string="Delivery Province")
    funeral_delivery_notes = fields.Text(string="Delivery Notes")
    funeral_condolence_ribbon = fields.Text(string="Condolence Ribbon")
    funeral_add_card = fields.Char(string="Add Condolence Card")
    funeral_condolence_card = fields.Text(string="Condolence Card")
    funeral_details_available = fields.Boolean(
        compute="_compute_funeral_details_available"
    )

    @api.depends(*FUNERAL_DETAIL_FIELDS)
    def _compute_funeral_details_available(self):
        for line in self:
            line.funeral_details_available = any(
                line[field] for field in FUNERAL_DETAIL_FIELDS
            )

    def action_view_funeral_details(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Funeral Details"),
            "res_model": "sale.order.line",
            "res_id": self.id,
            "view_mode": "form",
            "view_id": self.env.ref(
                "sale_order_line_funeral_details.view_sale_order_line_funeral_details_form"
            ).id,
            "target": "new",
        }
