# -*- coding: utf-8 -*-

from odoo import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    le_default_sidebar_preference = fields.Selection(
        selection=[
            ('invisible', 'Invisible'),
            ('small', 'Icons'),
            ('full', 'Icons + Name')
        ], 
        string="Sidebar Type",
        default='small')
    
    le_default_chatter_preference = fields.Selection(
        selection=[
            ('normal', 'Normal'),
            ('sided', 'Sided'),
        ], 
        string="Chatter Position", 
        default='sided')