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

from odoo import models, fields, api


class OpScholarship(models.Model):
    _name = 'op.scholarship'
    _inherit = 'mail.thread'
    _description = 'Scholarship'

    name = fields.Char('Name', size=64, required=True)
    student_id = fields.Many2one('op.student', 'Student', required=True)
    type_id = fields.Many2one('op.scholarship.type', 'Type', required=True)
    type_amount = fields.Integer(related='type_id.amount',string="Scholarship Amount", store=True, track_visibility='onchange')
    state = fields.Selection(
        [('draft', 'Draft'), ('confirm', 'Confirm'),
         ('reject', 'Reject')], 'State', default='draft', readonly=True,
        select=True, track_visibility='onchange')
    course_id = fields.Many2one(
        'op.course', 'Course', required=True,
        states={'confirm': [('readonly', True)]})
    batch_id = fields.Many2one(
        'op.batch', 'Batch', required=True,
        states={'confirm': [('readonly', True)]})
    roll_number = fields.Char(
        'Roll Number', required=True,
        states={'confirm': [('readonly', True)]})

    @api.onchange('type_id')
    def _onchange_vehicle(self):
        self.type_amount = self.type_id.amount

    @api.one
    def act_confirm(self):
        self.state = 'confirm'

    @api.one
    def act_reject(self):
        self.state = 'reject'
