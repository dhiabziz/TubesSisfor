from odoo import models, fields
import base64

class WizardProjectReport(models.TransientModel):
    _name = 'wizard.project.report'
    _description = 'Wizard Generate Laporan Proyek'

    project_id = fields.Many2one('project.project', string='Proyek', required=True)

    def action_generate_report(self):
        project = self.project_id
        report_text = f"Laporan Proyek: {project.name}\nJumlah Task: {len(project.task_ids)}"
        file_data = base64.b64encode(report_text.encode('utf-8'))

        self.env['project.report'].create({
            'name': f"Laporan {project.name}",
            'project_id': project.id,
            'report_file': file_data,
            'file_name': f'laporan_{project.name}.txt'
        })

        return {'type': 'ir.actions.act_window_close'}
