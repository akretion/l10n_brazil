# Copyright 2021 Akretion - Raphael Valyi <raphael.valyi@akretion.com>
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0.en.html).

from odoo import fields

from odoo.addons.spec_driven_model.models import spec_models


class ResPartner(spec_models.SpecModel):
    _name = "res.partner"
    _inherit = ["res.partner", "po.10.usaddress"]

    po10_country = fields.Char(related="country_id.name")
    po10_name = fields.Char(related="name")
    po10_street = fields.Char(related="street")
    po10_city = fields.Char(related="city")
    po10_state = fields.Char(related="state_id.name")
    # FIXME !!
    # po10_zip = fields.Monetary(
    #     currency_field="brl_currency_id",
    #     string="zip", xsd_required=True,
    #     xsd_type="decimal")


class PurchaseOrderLine(spec_models.SpecModel):
    _name = "fake.purchase.order.line"
    _inherit = ["fake.purchase.order.line", "po.10.item"]

    po10_productName = fields.Char(related="name")
    po10_quantity = fields.Integer(related="product_qty")
    po10_USPrice = fields.Monetary(related="price_unit")


class PurchaseOrder(spec_models.StackedModel):
    """
    We use StackedModel to ensure the m2o po10_items field
    from po.10.purchaseorder get its content (the Items class
    with the po10_item o2m field included inside PurchaseOrder).
    This po10_item is then related to the purchase.order order_id o2m field.
    """

    _name = "fake.purchase.order"
    _inherit = ["fake.purchase.order", "po.10.purchaseorder"]
    _spec_module = "odoo.addons.spec_driven_model.tests.spec_po"
    _stacked = "po.10.purchaseorder"
    _stacking_points = {}
    _po10_spec_module_classes = None

    po10_orderDate = fields.Date(compute="_compute_date")
    po10_confirmDate = fields.Date(related="date_approve")
    po10_shipTo = fields.Many2one(related="dest_address_id")
    po10_billTo = fields.Many2one(related="partner_id")
    po10_item = fields.One2many(related="order_line", relation_field="order_id")

    def _compute_date(self):
        """
        Example of data casting to accomodate with the xsd model
        """
        for po in self:
            po.po10_orderDate = po.date_order.date()
