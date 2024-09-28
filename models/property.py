from email.policy import default

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class Property(models.Model):
    _name = "property"
    _description = "Property"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    ref=fields.Char(compute="set_ref")

    name = fields.Char(required=True, default='New', size=20)
    description = fields.Text()
    postcode = fields.Char(required=True)
    expected_price = fields.Float(digits=(0, 5))
    # 16 - 9 - 2024
    date_availability = fields.Date(tracking=1)
    expected_selling_date=fields.Date(tracking=1,string='Expected Selling Date')
    is_late=fields.Boolean()
    selling_price = fields.Float(digits=(0, 5))
    diff = fields.Float(compute="_compute_diff", store=1, readonly=0, string="Differance")
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], default='north')

    state = fields.Selection([
            ('draft', 'Draft'),
            ('pending', 'Pending'),
            ('done', 'Done'),
            ('closed','Closed'),
        ], default='draft',tracking=1)

    active = fields.Boolean(string='Active', default=True)
    ribbon_visible = fields.Boolean(string='Show Ribbon', compute='_compute_ribbon_visible')

    @api.depends('active')
    def _compute_ribbon_visible(self):
        for record in self:
            record.ribbon_visible = not record.active  # Show ribbon if active is False

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address', readonly=0, store=1)
    owner_phone = fields.Char(related='owner_id.phone', readonly=0, store=1)
    code =fields.Char(string="Code")
    _sql_constraints = [
        ('unique_name', 'unique("name")', 'This name is exist!')
    ]

    property_line_ids = fields.One2many('property.line', 'property_id')

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    def action_pending(self):
        for rec in self:
            rec.state = 'pending'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_closed(self):
        for rec in self:
            rec.state='closed'
    @api.depends('expected_price', 'selling_price', 'owner_id.phone')
    def _compute_diff(self):
        for rec in self:
            rec.write({
                'diff': rec.expected_price - rec.selling_price
            })
            # print("insid compute fuction")
            # rec.diff = rec.expected_price - rec.selling_price

    @api.onchange('expected_price', 'owner_id')
    def _compute_diff(self):
        return {
            'warning': {'title': "Warning", 'message': "negative value", 'type': 'notification'},
        }


    # noinspection PyTypeChecker
    @api.constrains('bedrooms')
    def _check_bedrooms_grater_zero(self):
        """ Validation Method """
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('Please Add Valid Number Of Bedrooms!')

    @api.model_create_multi
    def create(self, vals):
        res = super(Property, self).create(vals)
        # print("inside create method")     # This logic will do when you click on the save button
        return res

    @api.model
    def _search(self, domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        res = super(Property, self)._search(domain, offset=0, limit=None, order=None, count=False, access_rights_uid=None)
        # print("inside read method")
        # self.play_sound()
        return res

    def write(self, vals):
        res = super(Property, self).write(vals)
        # print("inside write method")
        # self.play_sound2()
        return res

    def unlink(self):
        for rec in self:
            if rec.facades == 0:
                return
        res = super(Property, self).unlink()
        print("inside delete method")
        return res

    # 16 - 9 - 2024
    # def _compute_check_is_late(self):
    #     # property_ids=self.search([])
    #     # for rec in property_ids:
    #     #     if rec.expected_selling_date and rec.expected_selling_date<fields.date.today():
    #     #         rec.is_late=True
    #     print(self)
    def action(self):
        new_owner=self.env['owner'].create({
            'name':'New Owner 1',
            'phone':'01069184910'
        })
    @api.model
    def create(self,vals):
        res=super(Property,self).create(vals)
        if res.ref=='New':
            res.ref=self.env['ir.sequence'].next_by_code('property_seq')
        return res
    @api.depends('name')
    def set_ref(self):
        for rec in self:
            rec.ref='PR'+str(rec.id).zfill(5)
            # print(rec.ref)
    def create_history_record(self,old_state,new_state,reason=""):
        for rec in self:
            rec.env['history'].create({
                'user_id':rec.env.uid,
                'property_id':rec.id,
                'old_state':old_state,
                'new_state':new_state,
                'reason':reason,


            })
    def action_open_state_wizard(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.change_state_wizard_action')
        action['context']={'default_property_id':self.id}
        return action

    def open_related_owner(self):
        action=self.env['ir.actions.actions']._for_xml_id('app_one.owner_action')
        view_id=self.env.ref('app_one.owner_view_form').id
        action['res_id']=self.owner_id.id
        action['views']=[[view_id,'form']]
        return action
        # print(self.owner_id.id)
class PropertyLine(models.Model):
    _name = "property.line"

    property_id = fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()
