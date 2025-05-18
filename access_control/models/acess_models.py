from odoo import models, fields, api

class ProjectAccess(models.Model):
    _name = 'project.access'
    
    user_id = fields.Many2one('res.users', required=True)
    project_id = fields.Many2one('project.project', required=True)
    role = fields.Selection([
        ('admin', 'Administrator Proyek'),
        ('manager', 'Manajer Proyek'),
        ('member', 'Anggota Tim'),
        ('client', 'Klien')
    ], required=True, default = 'member')