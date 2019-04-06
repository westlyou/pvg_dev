# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': 'Project Gantt View',
    'version': '1.0',
    'category': 'Project Management Gantt View',
    'summary': 'Enabling Project Module to show Gantt View for project and task.',
    'description': """
                Enabling Project Module to show Gantt View for project and task.""",
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'price': 25.00,
    'currency': 'EUR',
    'depends': ['base', 'project'],
    'images': ['static/description/main_screenshot.png'],
    "data": [
        'views/templates.xml',
        'views/project_views.xml',
    ],
    'qweb': ['static/src/xml/*.xml'],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: