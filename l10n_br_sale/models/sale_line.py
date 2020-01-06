# @ 2019 Akretion - www.akretion.com.br -
#   Magno Costa <magno.costa@akretion.com.br>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    _name = 'sale.order.line'
    _inherit = ['sale.order.line', 'l10n_br_fiscal.document.line.mixin']

    @api.model
    def _default_operation(self):
        return self.env.user.company_id.sale_fiscal_operation_id.id

    @api.model
    def _operation_domain(self):
        domain = [('state', '=', 'approved')]
        domain.append(('fiscal_type', 'in', ('sale', 'other')))
        domain.append(('operation_type', 'in', ('out', 'all')))
        return domain

    operation_id = fields.Many2one(
        default=_default_operation,
        domain=lambda self: self._operation_domain()
    )

    def _calc_line_base_price(self):
        return self.price_unit * (1 - (self.discount or 0.0) / 100.0)

    def _calc_line_quantity(self):
        return self.product_uom_qty

    def _calc_price_gross(self, qty):
        return self.price_unit * qty

    @api.depends('product_uom_qty', 'discount', 'price_unit', 'tax_id')
    def _compute_amount(self):
        """
        Compute the amounts of the SO line.
        """
        for line in self:
            price = line._calc_line_base_price()
            qty = line._calc_line_quantity()
            taxes = line.tax_id.compute_all(
                price, line.order_id.currency_id, line.product_uom_qty,
                product=line.product_id,
                partner=line.order_id.partner_shipping_id)

            line.update({
                'price_tax': sum(t.get('amount', 0.0)
                    for t in taxes.get('taxes', [])
                    if not t.get('tax_include', False)),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                'price_gross': line._calc_price_gross(qty),
                'discount_value': line.order_id.pricelist_id.currency_id.round(
                    line._calc_price_gross(qty) - (price * qty))
            })

            print({
                'price_tax': sum(t.get('amount', 0.0)
                    for t in taxes.get('taxes', [])
                    if not t.get('tax_include', False)),
                'price_total': taxes['total_included'],
                'price_subtotal': taxes['total_excluded'],
                'price_gross': line._calc_price_gross(qty),
                'discount_value': line.order_id.pricelist_id.currency_id.round(
                    line._calc_price_gross(qty) - (price * qty))
            })

    partner_id = fields.Many2one(
        comodel_name="res.partner",
        related="order_id.partner_id",
        string="Partner")

    discount_value = fields.Float(
        compute='_compute_amount',
        string='Vlr. Desc. (-)',
        digits=dp.get_precision('Sale Price'))

    price_gross = fields.Float(
        compute='_compute_amount', string='Vlr. Bruto',
        digits=dp.get_precision('Sale Price'))

    price_subtotal = fields.Float(
        compute='_compute_amount', string='Subtotal',
        digits=dp.get_precision('Sale Price'))

    @api.onchange('operation_line_id')
    def _onchange_operation_line_id(self):
        if self.operation_line_id:
            fiscal_taxes = self.operation_line_id.get_fiscal_taxes(
                self.company_id, self.partner_id, self.product_id)
            self.tax_id |= fiscal_taxes.get_account_tax(self.operation_type)

    @api.multi
    def _prepare_invoice_line(self, qty):
        self.ensure_one()
        result = super(SaleOrderLine, self)._prepare_invoice_line(qty)
        result['operation_id'] = \
            self.operation_id.id or self.order_id.operation_id.id \
            or False
        result['operation_line_id'] = self.operation_line_id.id or False
        return result
