from odoo import models, fields, api

class History(models.Model):
    _name='history'

    user_id=fields.Many2one('res.users')
    property_id=fields.Many2one('property')
    reason=fields.Char(string='Reason')
    old_state=fields.Char()
    new_state=fields.Char()