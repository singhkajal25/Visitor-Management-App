from frappe import _

def get_data():
    return {
        'fieldname': 'visitor_pass',
        'transactions': [
            {
                'label': _('Reference'),
                'items': ['Visitor Invitation']
            }
        ]
    }