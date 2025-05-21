{
    'name': 'Custom Sidebar Module',
    'version': '1.0',
    'summary': 'Custom sidebar with navigation buttons',
    'description': 'Module that adds a sidebar with buttons for navigating to project, document, and account dashboards.',
    'category': 'Tools',
    'author': 'Your Name',
    'website': 'https://yourcompany.com',
    'depends': ['base', 'web'],
    'data': [
        'views/sidebar_menu.xml',
        'views/sidebar_view.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}