{
    'name': 'app_one',
    'version': '1.0',
    'summary': 'A brief description of my module',
    'description': 'A longer description of what my module does',
    'author': 'Abdo',
    'category': 'Uncategorized',
    'depends': ['base','sale','stock'],  # List of dependencies "inhertinces"
    'data': [
        'views/base_menu.xml',
        'views/property_view.xml',
        'security/ir.model.access.csv',
        
        
    ],
    'installable': True,
    'application': True,
    'license':'LGPL-3'
}