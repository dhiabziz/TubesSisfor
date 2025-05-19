# -*- coding: utf-8 -*-
{
    'name': "Document Repository",
    'summary': """
        Upload, view, and download documents organized by projects,
        with versioning for duplicate filenames and access control.""",
    'description': """
        This module allows users to manage project-specific documents.
        - Attach documents to projects.
        - View and download uploaded documents.
        - If a document with the same name is uploaded to the same project,
          it creates a new version by appending a timestamp to the filename,
          grouping them visually.
        - Control access to documents with roles (client, team member, manager).
        - Set specific permissions for users on each project.
    """,
    'author': "Your Name/Company",
    'website': "https://www.yourcompany.com",
    'category': 'Project',
    'version': '17.0.1.0.0',
    'depends': ['base', 'project'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/security_rules.xml',
        'views/project_document_views.xml',
        'views/project_user_access_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}