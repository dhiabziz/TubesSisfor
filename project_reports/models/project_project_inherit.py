from odoo import models

class ProjectProject(models.Model):
    _inherit = 'project.project'

    def action_open_report_wizard(self):
        return {
            'name': 'Generate Laporan Proyek',
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.project.report',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_project_id': self.id}
        }
