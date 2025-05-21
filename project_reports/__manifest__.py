{
    'name': 'Project Reports',
    'version': '1.0',
    'summary': 'Generate dan download laporan proyek',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_report_views.xml',
        'views/project_project_inherit.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
