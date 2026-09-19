from frappe import _

def get_data():
    return {
        'fieldname': 'visitor_invitation',  
        'non_standard_fieldnames': {
            'Visitor Pass': 'visitor_invitation'
        },
        'transactions': [
            {
                'label': _('Passes'),
                'items': ['Visitor Pass']
            }
        ]
    }