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

    def check_access_rights(self, operation, raise_exception=True):
        if self.env.user.has_group('project.group_project_manager'):
            return True
        if operation == 'read' and self.env.user.has_group('document_repository.group_document_viewer'):
            return True
        if operation in ['write', 'create'] and self.env.user.has_group('document_repository.group_document_uploader'):
            return True
        if raise_exception:
            raise AccessError(_("You don't have rights to %s this document.") % operation)
        return False

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
        if not self.env.user.has_group('document_repository.group_document_uploader'):
            raise AccessError(_("Only users with Document Uploader role can upload files."))
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
    @api.onchange('file_data', 'name')
    def _onchange_file_data(self):
        if self.file_data and self.name and not self.original_file_name_upload:
            self.original_file_name_upload = self.name

    def action_download_document(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{self._name}/{self.id}/file_data?download=true&filename={self.name}',
            'target': 'self',
        }