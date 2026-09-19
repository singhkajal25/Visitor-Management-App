// Copyright (c) 2026, Kanak Infosystems LLP and contributors
// For license information, please see license.txt

frappe.ui.form.on('Visitor Invitation', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            
            if (frm.doc.invitation_expires_on && frm.doc.invitation_status !== 'Registered') {
                let expires_on = frappe.datetime.str_to_obj(frm.doc.invitation_expires_on);
                let now = new Date();

                if (now > expires_on && frm.doc.invitation_status !== 'Expired') {
                    frm.set_value('invitation_status', 'Expired');
                    frm.save();
                }
            }

            if (frm.doc.invitation_status) {
                let status = frm.doc.invitation_status;
                let color_map = {
                    'Pending': 'orange',
                    'Sent': 'blue',
                    'Registered': 'green',
                    'Expired': 'red'
                };
                let color = color_map[status] || 'gray';
                frm.page.set_indicator(__(status), color);
            }

            if (['Registered', 'Expired'].includes(frm.doc.invitation_status)) {
                return;
            }

            let button_label = (frm.doc.invitation_status === 'Sent') ? __('Resend Invitation') : __('Send Invitation');

            frm.add_custom_button(button_label, function() {
                frappe.call({
                    method: "send_invitation_email",
                    doc: frm.doc,
                    freeze: true,
                    freeze_message: __("Sending Email..."),
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint(__('Invitation email sent to ' + frm.doc.visitor_email));
                            frm.reload_doc();
                        }
                    }
                });
            }, __('Actions'));
        }
    }
});
