from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def _default_sidebar_type(self):
        return self.env.user.company_id.le_default_sidebar_preference or 'small'
    
    @api.model
    def _default_chatter_position(self):
        return self.env.user.company_id.le_default_chatter_preference or 'sided'

    le_sidebar_type = fields.Selection(
        selection=[
            ('invisible', 'Invisible'),
            ('small', 'Icons'),
            ('large', 'Icons + Name')
        ], 
        required=True,
        string="Sidebar Type",
        default=lambda self: self._default_sidebar_type())
    
    le_chatter_position = fields.Selection(
        selection=[
            ('normal', 'Normal'),
            ('sided', 'Sided'),
        ], 
        required=True,
        string="Chatter Position", 
        default=lambda self: self._default_chatter_position())


    def __init__(self, pool, cr):
        init_res = super(ResUsers, self).__init__(pool, cr)
        type(self).SELF_WRITEABLE_FIELDS = list(self.SELF_WRITEABLE_FIELDS)
        type(self).SELF_WRITEABLE_FIELDS.extend(['le_sidebar_type'])
        type(self).SELF_WRITEABLE_FIELDS.extend(['chatter_position'])
        type(self).SELF_READABLE_FIELDS = list(self.SELF_READABLE_FIELDS)
        type(self).SELF_READABLE_FIELDS.extend(['le_sidebar_type'])
        type(self).SELF_READABLE_FIELDS.extend(['chatter_position'])
        return init_res