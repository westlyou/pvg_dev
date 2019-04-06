# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

{
    'name': 'OpenEduCat Health Extended',
    'version': '12.0.1.0.0',
    'license': 'LGPL-3',
    'category': 'Education',
    "sequence": 3,
    'summary': 'Manage Health',
    'complexity': "easy",
    'description': """
        This module adds the feature of health in Openeducat
    """,
    'author': 'Muhammad Faisal,Tech Receptives',
    'website': 'https://github.com/mfaisalcfa/odoo-addons',
    'depends': ['openeducat_core'],
    'data': [
        'views/health_view.xml',
        'security/ir.model.access.csv',
        'health_menu.xml',
        'views/report_reg.xml',
        'views/health_register_view.xml',
        'views/health_history_view.xml',
    ],
    'demo': [
        'demo/health_line_demo.xml',
        'demo/health_demo.xml'
    ],
    'images': [
        'static/description/openeducat_health_banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
