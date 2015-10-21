# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2014  Renato Lima - Akretion                                  #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU Affero General Public License for more details.                         #
#                                                                             #
# You should have received a copy of the GNU Affero General Public License    #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

{
    'name': 'Brazilian Localization Sale Service',
    'description': 'Brazilian Localization Sale Service',
    'category': 'Localisation',
    'license': 'AGPL-3',
    'author': 'Akretion, Odoo Brasil',
    'website': 'http://odoo-brasil.org',
    'version': '8.0',
    'depends': [
        'l10n_br_sale',
        'l10n_br_account_service',
    ],
    'data': [
        'data/l10n_br_sale_service_data.xml',
    ],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': True,
}
