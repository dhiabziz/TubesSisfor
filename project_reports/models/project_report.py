from odoo import models, fields

class ProjectReport(models.Model):
    _name = 'project.report'
    _description = 'Laporan Proyek'

    name = fields.Char(string='Nama Laporan', required=True)
    project_id = fields.Many2one('project.project', string='Proyek', required=True)
    report_file = fields.Binary(string='File Laporan')
    file_name = fields.Char(string='Nama File')
    date_generated = fields.Datetime(string='Tanggal Generate', default=fields.Datetime.now)
