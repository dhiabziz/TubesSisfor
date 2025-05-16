# -*- coding: utf-8 -*-
{
    'name': "Document Repository",
    'summary': """
        Upload, view, and download documents organized by projects,
        with versioning for duplicate filenames.""",
    'description': """
        This module allows users to manage project-specific documents.
        - Attach documents to projects.
        - View and download uploaded documents.
        - If a document with the same name is uploaded to the same project,
          it creates a new version by appending a timestamp to the filename,
          grouping them visually.
    """,
    'author': "Your Name/Company",
    'website': "https://www.yourcompany.com",
    'category': 'Project',
    'version': '17.0.1.0.0',
    'depends': ['project'],  # Depends on the 'project' module
    'data': [
        'security/ir.model.access.csv',
        'views/project_document_views.xml',
    ],
    'installable': True,
    'application': True, # Set to True to make it appear as an App
    'license': 'LGPL-3', # Or your preferred license
}