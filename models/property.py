from odoo import models, fields, api

class Property(models.Model):
    _name='property'


    name=fields.Char(string="Name")

    gender=fields.Selection(
        [
            ('male','Male'),
            ('femal','Femal'),

        ]
    )
    