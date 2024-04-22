from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    account_freight_in_id = fields.Many2one('account.account', string='Supplier Invoice Freight Account')
    account_freight_out_id = fields.Many2one('account.account', string='Customer Invoice Freight Account')
