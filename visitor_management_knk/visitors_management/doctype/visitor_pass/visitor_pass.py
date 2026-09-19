# Copyright (c) 2026, Kanak Infosystems LLP and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import format_datetime, get_url


class VisitorPass(Document):

    def before_insert(self):
        if not self.workflow_state:
            self.workflow_state = "Draft"

    def on_update(self):
        ensure_workflow_exists()

        if self.workflow_state == "Pending Approval" and not self.flags.approval_email_sent:
            self.send_approval_email()
            self.flags.approval_email_sent = True

    def send_approval_email(self):
        if not self.person_to_visit:
            return

        employee_email = frappe.db.get_value("Employee", self.person_to_visit, "personal_email")

        if not employee_email:
            frappe.msgprint(f"Employee {self.person_to_visit} does not have a valid 'personal_email'.")
            return

        approval_page_url = f"{get_url()}/visitor-pass?pass_id={self.name}"
        formatted_date = format_datetime(self.visit_date, "dd-MM-yyyy") if self.visit_date else "N/A"

        subject = f"Approval Required: Visitor Pass - {self.visitor_full_name}"
        
        message = f"""
            <p>Dear <b>{self.person_to_visit}</b>,</p>
            <p>A new visitor pass requires your approval.</p>
            
            <table style="border-collapse: collapse; width: 100%; max-width: 500px; margin: 15px 0;">
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd;"><b>Visitor Name:</b></td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{self.visitor_full_name}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd;"><b>Mobile:</b></td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{self.mobile_number or 'N/A'}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd;"><b>Email:</b></td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{self.email_id or 'N/A'}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd;"><b>Department:</b></td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{self.department or 'N/A'}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd;"><b>Visit Date:</b></td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{formatted_date}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd;"><b>Expected Check-In:</b></td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{self.expected_checkin or 'N/A'}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd;"><b>Expected Check-Out:</b></td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{self.expected_checkout or 'N/A'}</td></tr>
                <tr><td style="padding: 6px; border-bottom: 1px solid #ddd;"><b>Purpose:</b></td><td style="padding: 6px; border-bottom: 1px solid #ddd;">{self.purpose_of_visit or 'N/A'}</td></tr>
            </table>

            <p>Click below to approve or reject this request:</p>
            <p>
                <a href="{approval_page_url}" style="padding: 10px 18px; background-color: #171717; color: #ffffff; text-decoration: none; border-radius: 5px; display: inline-block;">
                    Review Request
                </a>
            </p>
        """

        frappe.sendmail(
            recipients=[employee_email],
            subject=subject,
            message=message,
            now=True
        )


def setup_visitor_pass_workflow():
    ensure_workflow_exists()


def create_workflow_state_if_missing(state_name, style=None):
    if not frappe.db.exists("Workflow State", state_name):
        doc = frappe.get_doc({
            "doctype": "Workflow State",
            "workflow_state_name": state_name,
            "style": style or "Primary"
        })
        doc.insert(ignore_permissions=True)


def create_workflow_action_if_missing(action_name):
    if not frappe.db.exists("Workflow Action Master", action_name):
        doc = frappe.get_doc({
            "doctype": "Workflow Action Master",
            "workflow_action_name": action_name
        })
        doc.insert(ignore_permissions=True)


def ensure_workflow_exists():
    create_workflow_state_if_missing("Pass Sent to Visitor", "Success")

    if frappe.db.exists("Workflow", "Visitor Pass Approval Workflow"):
        workflow = frappe.get_doc("Workflow", "Visitor Pass Approval Workflow")
        existing_states = [d.state for d in workflow.states]
        
        if "Pass Sent to Visitor" not in existing_states:
            workflow.append("states", {
                "state": "Pass Sent to Visitor",
                "doc_status": "1",
                "allow_edit": "System Manager",
                "style": "Success"
            })
            workflow.save(ignore_permissions=True)
            frappe.db.commit()
        return

    states_to_create = [
        ("Draft", "Inverse"),
        ("Pending Approval", "Warning"),
        ("Approved", "Success"),
        ("Rejected", "Danger"),
        ("Pass Sent to Visitor", "Success")
    ]
    for state_name, style in states_to_create:
        create_workflow_state_if_missing(state_name, style)

    actions_to_create = ["Send for Approval", "Approve", "Reject"]
    for action_name in actions_to_create:
        create_workflow_action_if_missing(action_name)

    workflow = frappe.get_doc({
        "doctype": "Workflow",
        "workflow_name": "Visitor Pass Approval Workflow",
        "document_type": "Visitor Pass",
        "is_active": 1,
        "override_status": 0,
        "workflow_state_field": "workflow_state",
        "states": [
            {"state": "Draft", "doc_status": "0", "allow_edit": "System Manager", "style": "Inverse"},
            {"state": "Pending Approval", "doc_status": "0", "allow_edit": "System Manager", "style": "Warning"},
            {"state": "Approved", "doc_status": "1", "allow_edit": "System Manager", "style": "Success"},
            {"state": "Rejected", "doc_status": "0", "allow_edit": "System Manager", "style": "Danger"},
            {"state": "Pass Sent to Visitor", "doc_status": "1", "allow_edit": "System Manager", "style": "Success"}
        ],
        "transitions": [
            {"state": "Draft", "action": "Send for Approval", "next_state": "Pending Approval", "allowed": "System Manager"},
            {"state": "Pending Approval", "action": "Approve", "next_state": "Approved", "allowed": "System Manager"},
            {"state": "Pending Approval", "action": "Reject", "next_state": "Rejected", "allowed": "System Manager"}
        ]
    })
    
    workflow.insert(ignore_permissions=True)
    frappe.db.commit()


@frappe.whitelist(allow_guest=True)
def get_visitor_pass_details(pass_id):
    if not pass_id:
        frappe.throw("Invalid or missing Pass ID.")

    pass_data = frappe.db.sql(
        """
        SELECT 
            name,
            visitor_full_name,
            email_id,
            mobile_number,
            person_to_visit,
            department,
            purpose_of_visit,
            visit_date,
            expected_checkin,
            expected_checkout,
            workflow_state
        FROM `tabVisitor Pass`
        WHERE name = %s
        """,
        (pass_id,),
        as_dict=True
    )

    if not pass_data:
        frappe.throw("Visitor Pass not found.")

    return pass_data[0]


@frappe.whitelist(allow_guest=True)
def update_visitor_pass_status(pass_id, action):
    if action not in ["Approve", "Reject"]:
        frappe.throw("Invalid action requested.")

    if not frappe.db.exists("Visitor Pass", pass_id):
        frappe.throw("Visitor Pass not found.")

    new_state = "Approved" if action == "Approve" else "Rejected"
    new_docstatus = 1 if action == "Approve" else 0

    frappe.db.set_value(
        "Visitor Pass",
        pass_id,
        {
            "workflow_state": new_state,
            "docstatus": new_docstatus
        },
        update_modified=True
    )

    frappe.db.commit()

    return {"status": "success", "workflow_state": new_state}


@frappe.whitelist()
def send_pass_email(docname):
    doc = frappe.get_doc("Visitor Pass", docname)
    
    if not doc.email_id:
        frappe.throw("Email ID is required to send the pass.")
        
    pdf_content = frappe.get_print(
        doctype="Visitor Pass",
        name=doc.name,
        print_format="Visitor Pass",  
        as_pdf=True
    )
    
    frappe.sendmail(
        recipients=[doc.email_id],
        subject=f"Visitor Pass - {doc.name}",
        message=f"""
            <p>Dear <b>{doc.visitor_full_name or 'Visitor'}</b>,</p>
            <p>Your Visitor Pass has been approved. Please find the attached pass details.</p>
        """,
        now=True,
        attachments=[{
            "fname": f"Visitor_Pass_{doc.name}.pdf",
            "fcontent": pdf_content
        }]
    )

    doc.db_set("workflow_state", "Pass Sent to Visitor", update_modified=True)
    frappe.db.commit()

    return {
        "status": "success", 
        "message": f"Pass sent successfully to {doc.email_id}",
        "workflow_state": "Pass Sent to Visitor"
    }

    