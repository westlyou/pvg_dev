# -*- coding: utf-8 -*-

from odoo import fields, models, api, _


class ResLang(models.Model):
    _inherit = 'res.lang'

    flag = fields.Binary(string='Language Flag')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
