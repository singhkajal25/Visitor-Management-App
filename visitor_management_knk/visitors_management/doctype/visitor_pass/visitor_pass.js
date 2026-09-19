// Copyright (c) 2026, Kanak Infosystems LLP and contributors
// For license information, please see license.txt


frappe.ui.form.on("Visitor Pass", {
    refresh(frm) {
        let current_state = frm.doc.workflow_state || frm.doc.status;

        if (!frm.is_new() && current_state === "Approved") {
            frm.add_custom_button(__('Send Pass to Visitor'), function() {
                if (!frm.doc.email_id) {
                    frappe.msgprint(__('Please set an Email ID before sending the pass.'));
                    return;
                }

                frappe.call({
                    method: "visitor_management_knk.visitors_management.doctype.visitor_pass.visitor_pass.send_pass_email",
                    args: {
                        docname: frm.doc.name
                    },
                    freeze: true,
                    freeze_message: __('Sending Visitor Pass PDF...'),
                    callback: function(r) {
                        if (!r.exc) {
                            frappe.msgprint(__('Pass sent successfully to {0}', [frm.doc.email_id]));
                            
                            frm.reload_doc();
                        }
                    }
                });
            }, __('Actions'));
        }
    }
});