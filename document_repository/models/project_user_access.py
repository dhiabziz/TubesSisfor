# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class ProjectUserAccess(models.Model):
    _name = 'project.user.access'
    _description = 'Project User Access Rights'
    _rec_name = 'user_id'

    user_id = fields.Many2one(
        'res.users',
        string='User',
        required=True,
        ondelete='cascade'
    )
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        required=True,
        ondelete='cascade'
    )
    role = fields.Selection([
        ('client', 'Client'),
        ('team', 'Team Member'),
        ('manager', 'Project Manager')
    ], string='Role', required=True, default='team')
    
    read_access = fields.Boolean('Read Documents', default=True)
    write_access = fields.Boolean('Edit Documents')
    create_access = fields.Boolean('Create Documents')
    delete_access = fields.Boolean('Delete Documents')
    
    _sql_constraints = [
        ('unique_user_project', 'UNIQUE(user_id, project_id)', 
         'A user can only have one access entry per project!')
    ]

    @api.onchange('role')
    def _onchange_role(self):
        if self.role == 'client':
            self.read_access = True
            self.write_access = False
            self.create_access = False
            self.delete_access = False
        elif self.role == 'team':
            self.read_access = True
            self.write_access = True
            self.create_access = True
            self.delete_access = False
        elif self.role == 'manager':
            self.read_access = True
            self.write_access = True
            self.create_access = True
            self.delete_access = True

    @api.model
    def create(self, vals):
        record = super(ProjectUserAccess, self).create(vals)
        record._sync_user_groups()
        return record
    
    def write(self, vals):
        result = super(ProjectUserAccess, self).write(vals)
        if 'role' in vals:
            self._sync_user_groups()
        return result
    
    def _sync_user_groups(self):
        for record in self:
            user = record.user_id
            client_group = self.env.ref('document_repository.group_document_client')
            team_group = self.env.ref('document_repository.group_document_team')
            manager_group = self.env.ref('document_repository.group_document_manager')
            
            groups_to_remove = client_group + team_group + manager_group
            user.write({'groups_id': [(3, group.id) for group in groups_to_remove]})
            
            highest_role = self._get_highest_user_role(user)
            
            if highest_role == 'manager':
                user.write({'groups_id': [(4, manager_group.id)]})
            elif highest_role == 'team':
                user.write({'groups_id': [(4, team_group.id)]})
            elif highest_role == 'client':
                user.write({'groups_id': [(4, client_group.id)]})
    
    @api.model
    def _get_highest_user_role(self, user):
        user_accesses = self.search([('user_id', '=', user.id)])
        
        if any(access.role == 'manager' for access in user_accesses):
            return 'manager'
        elif any(access.role == 'team' for access in user_accesses):
            return 'team'
        elif any(access.role == 'client' for access in user_accesses):
            return 'client'
        return None
        
    def name_get(self):
        result = []
        for record in self:
            name = f"{record.user_id.name} - {record.project_id.name} [{dict(self._fields['role'].selection).get(record.role)}]"
            result.append((record.id, name))
        return result