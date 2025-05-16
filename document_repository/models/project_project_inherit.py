# -*- coding: utf-8 -*-
from odoo import models, fields, api

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

    def _compute_document_count(self):
        for project in self:
            project.document_count = self.env['project.document'].search_count(
                [('project_id', '=', project.id)]
            )

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