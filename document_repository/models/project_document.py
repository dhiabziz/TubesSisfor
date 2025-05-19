# -*- coding: utf-8 -*-
import os
from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import UserError, AccessError

class ProjectDocument(models.Model):
    _name = 'project.document'
    _description = 'Project Document'
    _order = 'project_id, document_group_name, create_date desc' 
    _rec_name = 'name' 

    name = fields.Char(
        string="Filename",
        required=True,
        help="The actual stored filename, possibly versioned."
    )
    file_data = fields.Binary(
        string="File",
        required=True,
        attachment=True, 
        help="The document file."
    )
    original_file_name_upload = fields.Char('Original Filename', help="The filename as originally uploaded by the user")
    project_id = fields.Many2one(
        'project.project',
        string="Project",
        required=True,
        ondelete='cascade',
        index=True
    )
    description = fields.Text(string="Description")
    upload_date = fields.Datetime(
        string="Upload Date",
        default=fields.Datetime.now,
        readonly=True
    )
    document_group_name = fields.Char('Document Group', compute='_compute_document_group', store=True)
    create_uid = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user, readonly=True)

    @api.depends('original_file_name_upload')
    def _compute_document_group(self):
        for record in self:
            if record.original_file_name_upload:
                base_name, _ = os.path.splitext(record.original_file_name_upload)
                record.document_group_name = base_name
            else:
                record.document_group_name = False

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            project_id = vals.get('project_id')
            if project_id:
                self._check_project_access(project_id, 'create')
        
        records_to_create = []
        for vals in vals_list:
            original_filename = vals.get('name')
            vals['original_file_name_upload'] = original_filename
            
            if original_filename:
                base_name, ext = os.path.splitext(original_filename)
                vals['document_group_name'] = base_name

                project_id = vals.get('project_id')
                if project_id:
                    existing_docs = self.search([
                        ('project_id', '=', project_id),
                        ('document_group_name', '=', base_name)
                    ])
                    
                    if existing_docs:
                        timestamp = datetime.now().strftime("%Y%m%d%H%M")
                        vals['name'] = f"{base_name}_{timestamp}{ext}"
            
            records_to_create.append(vals)
        
        return super().create(records_to_create)

    def write(self, vals):
        for record in self:
            record._check_project_access(record.project_id.id, 'write')
        return super().write(vals)
    
    def unlink(self):
        for record in self:
            record._check_project_access(record.project_id.id, 'delete')
        return super().unlink()

    def _check_project_access(self, project_id, access_type):
        if self.env.user.has_group('document_repository.group_document_manager'):
            return True
        
        user_access = self.env['project.user.access'].search([
            ('user_id', '=', self.env.user.id),
            ('project_id', '=', project_id)
        ], limit=1)
        
        if not user_access:
            project = self.env['project.project'].browse(project_id)
            if project.user_id and project.user_id.id == self.env.user.id:
                return True
            raise AccessError(_(
                "You don't have access to project documents for this project. "
                "Please contact your administrator."
            ))
        
        if access_type == 'read' and not user_access.read_access:
            raise AccessError(_("You don't have read access to this project's documents."))
        elif access_type == 'write' and not user_access.write_access:
            raise AccessError(_("You don't have write access to this project's documents."))
        elif access_type == 'create' and not user_access.create_access:
            raise AccessError(_("You don't have permission to create documents for this project."))
        elif access_type == 'delete' and not user_access.delete_access:
            raise AccessError(_("You don't have permission to delete documents from this project."))
        
        return True

    @api.onchange('file_data', 'name')
    def _onchange_file_data(self):
        if self.file_data and self.name and not self.original_file_name_upload:
            self.original_file_name_upload = self.name

    def action_download_document(self):
        self.ensure_one()
        self._check_project_access(self.project_id.id, 'read')
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/file_data?download=true&filename={self.name}',
            'target': 'self',
        }