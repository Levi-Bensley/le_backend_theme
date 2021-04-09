import re
import uuid
import base64
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models

XML_ID = "le_backend_theme.assets_theme_colors"
SCSS_URL = "/le_backend_theme/static/src/scss/colors.scss"
VARIABLES = [
    'wr-primary',
    'wr-secondary',
    'wr-gradient',
]

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'    
    
    le_theme_default_sidebar_preference = fields.Selection(
        related="company_id.le_default_sidebar_preference",
        readonly=False)

    le_theme_color_primary = fields.Char(
        string="Theme Primary Color")
    
    le_theme_color_secondary = fields.Char(
        string="Theme Secondary Color")
    
    le_theme_color_accent = fields.Char(
        string="Theme Accent Color")

    le_theme_default_chatter_preference = fields.Selection(
        related="company_id.le_default_chatter_preference",
        readonly=False)


    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].with_user(self.env.ref('base.user_admin'))
        variables = VARIABLES
        colors = self.env['scss.editor'].get_values(
            SCSS_URL, XML_ID, variables
        )
        colors_changed = []
        colors_changed.append(self.le_theme_color_primary != colors['wr-primary'])
        colors_changed.append(self.le_theme_color_secondary != colors['wr-gradient'])
        colors_changed.append(self.le_theme_color_accent != colors['wr-secondary'])
        if(any(colors_changed)):
            variables = [
                {'name': 'wr-primary', 'value': self.le_theme_color_primary or "#0B2E59"},
                {'name': 'wr-gradient', 'value': self.le_theme_color_secondary or "#3F71AB"},
                {'name': 'wr-secondary', 'value': self.le_theme_color_accent or "#FEBA00"},
            ]
            if self.le_theme_color_primary:
                variables.append({'name': 'wr-primary-dark', 'value': "scale-color(" + self.le_theme_color_primary + ", $lightness: 20%)"},)
            else:
                variables.append({'name': 'wr-primary-dark', 'value': 'scale-color(#0B2E59, $lightness: 20%)'})
            if self.le_theme_color_secondary:
                variables.append({'name': 'wr-gradient-muted', 'value': "scale-color(" + self.le_theme_color_secondary + ", $lightness: 20%)"},)
                variables.append({'name': 'wr-gradient-dark', 'value': "scale-color(" + self.le_theme_color_secondary + ", $lightness: -20%)"},)
            else:
                variables.append({'name': 'wr-gradient-muted', 'value': 'scale-color(#3F71AB, $lightness: 20%)'})
                variables.append({'name': 'wr-gradient-dark', 'value': 'scale-color(#3F71AB, $lightness: -20%)'})
            if self.le_theme_color_accent:
                variables.append({'name': 'wr-secondary-dark', 'value': "scale-color(" + self.le_theme_color_accent + ", $lightness: -20%)"},)
            else:
                variables.append({'name': 'wr-secondary-dark', 'value': 'scale-color(#FEBA00, $lightness: -20%)'})

            _logger.info("\n\n%s\n\n" % variables)
            self.env['scss.editor'].replace_values(
                SCSS_URL, XML_ID, variables
            )
        return res

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].with_user(self.env.ref('base.user_admin'))
        variables = VARIABLES
        colors = self.env['scss.editor'].get_values(
            SCSS_URL, XML_ID, variables
        )
        res.update({
            'le_theme_color_primary': colors['wr-primary'],
            'le_theme_color_secondary': colors['wr-gradient'],
            'le_theme_color_accent': colors['wr-secondary'],
        })
        return res
