# Copyright (C) 2009  Renato Lima - Akretion
# Copyright (C) 2012  Raphaël Valyi - Akretion
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp


class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'l10n_br_fiscal.document.mixin']

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

    @api.depends('order_line.price_unit', 'order_line.tax_id',
                 'order_line.discount', 'order_line.product_uom_qty')
    def _amount_all(self):
        """
        Compute the total amounts of the SO.
        """
        for order in self:
            amount_untaxed = amount_tax = amount_discount = amount_gross = 0.0
            for line in order.order_line:
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
                amount_discount += line.discount_value
                amount_gross += line.price_gross
            order.update({
                'amount_untaxed': amount_untaxed,
                'amount_tax': amount_tax,
                'amount_total': amount_untaxed + amount_tax,
                'amount_gross': amount_gross
            })

    copy_note = fields.Boolean(
        string='Copiar Observação no documentos fiscal')

    amount_discount = fields.Float(
        compute='_amount_all',
        string='Desconto (-)',
        digits=dp.get_precision('Account'),
        store=True,
        help="The discount amount.")

    amount_gross = fields.Float(
        compute='_amount_all',
        string='Vlr. Bruto',
        digits=dp.get_precision('Account'),
        store=True, help="The discount amount.")

    discount_rate = fields.Float(
        string='Desconto',
        readonly=True,
        states={'draft': [('readonly', False)]})

    cnpj_cpf = fields.Char(
        string=u'CNPJ/CPF',
        related='partner_id.cnpj_cpf')

    legal_name = fields.Char(
        string=u'Razão Social',
        related='partner_id.legal_name')

    ie = fields.Char(
        string=u'Inscrição Estadual',
        related='partner_id.inscr_est')

    @api.onchange('discount_rate')
    def onchange_discount_rate(self):
        for sale_order in self:
            for sale_line in sale_order.order_line:
                sale_line.discount = sale_order.discount_rate

    @api.model
    def _fiscal_comment(self, order):
        fp_comment = []
        fp_ids = []
        """
        for line in order.order_line:
            if line.fiscal_position_id and \
                    line.fiscal_position_id.inv_copy_note and \
                    line.fiscal_position_id.note:
                if line.fiscal_position_id.id not in fp_ids:
                    fp_comment.append(line.fiscal_position_id.note)
                    fp_ids.append(line.fiscal_position_id.id)
        """
        return fp_comment

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        result = super(SaleOrder, self)._prepare_invoice()
        context = self.env.context

        if (context.get('fiscal_type') == 'service' and
                self.order_line and self.order_line[0].operation_id):
            operation_id = self.order_line[0].operation_id.id
        else:
            operation_id = self.operation_id

        if operation_id:
            result['journal_id'] = operation_id.journal_id.id

        result['partner_shipping_id'] = self.partner_shipping_id.id

        comment = []
        if self.note and self.copy_note:
            comment.append(self.note)

        fiscal_comment = self._fiscal_comment(self)
        result['comment'] = " - ".join(comment)
        result['fiscal_comment'] = " - ".join(fiscal_comment)
        result['operation_id'] = operation_id.id

        return result
