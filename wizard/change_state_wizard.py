from odoo import fields,models

class ChangeState(models.TransientModel):
    _name='change.state'


    property_id=fields.Many2one('property')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('closed', 'Closed'),
    ], default='draft', tracking=1,string='State')
    reason=fields.Char(string='Reason')


    def confirm_action(self):
        self.property_id.state = self.state
        self.property_id.create_history_record('closed', self.state, self.reason)
