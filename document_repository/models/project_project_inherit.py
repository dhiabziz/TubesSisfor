# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class ProjectProjectInherit(models.Model):
    _inherit = 'project.project'

    document_ids = fields.One2many(
        'project.document',
        'project_id',
        string='Documents'
    )
    document_count = fields.Integer(
        compute='_compute_document_count',
        string='Document Count'
    )
    user_access_ids = fields.One2many(
        'project.user.access',
        'project_id',
        string='User Access Rights'
    )
    member_ids = fields.Many2many(
        'res.users', 
        string='Project Members',
        compute='_compute_member_ids', 
        store=True
    )

    def _compute_document_count(self):
        for project in self:
            project.document_count = self.env['project.document'].search_count(
                [('project_id', '=', project.id)]
            )
    
    @api.depends('user_access_ids', 'user_access_ids.user_id')
    def _compute_member_ids(self):
        for project in self:
            member_ids = project.user_access_ids.mapped('user_id').ids
            # Always include the project manager if there is one
            if project.user_id and project.user_id.id not in member_ids:
                member_ids.append(project.user_id.id)
            project.member_ids = member_ids

    def action_view_project_documents(self):
        self.ensure_one()
        return {
            'name': ('Documents'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.document',
            'view_mode': 'tree,form',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
                'search_default_project_id': self.id,
                'search_default_group_by_document_group': 1, 
            }
        }
    
    def action_manage_user_access(self):
        self.ensure_one()
        return {
            'name': _('Manage User Access'),
            'type': 'ir.actions.act_window',
            'res_model': 'project.user.access',
            'view_mode': 'tree,form',
            'domain': [('project_id', '=', self.id)],
            'context': {
                'default_project_id': self.id,
            },
        }