from odoo import models, fields

class SidebarItem(models.Model):
    _name = 'sidebar.item'
    _description = 'Sidebar Navigation Item'

    name = fields.Char(string='Label', required=True)
    action = fields.Char(string='Action', required=True)