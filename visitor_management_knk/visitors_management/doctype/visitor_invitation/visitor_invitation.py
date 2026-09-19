# # Copyright (c) 2026, Kanak Infosystems LLP and contributors
# # For license information, please see license.txt

# import json
# import secrets
# import frappe
# from frappe.model.document import Document
# from frappe.utils import getdate, add_days, get_datetime, now_datetime, format_datetime

# class VisitorInvitation(Document):
    
#     def before_save(self):
#         if self.visit_date:
#             day_before = add_days(getdate(self.visit_date), -1)
#             self.invitation_expires_on = f"{day_before} 12:00:00"

#     @frappe.whitelist()
#     def send_invitation_email(self):
#         if not self.visitor_email:
#             frappe.throw("Please enter a valid Visitor Email first.")

#         if not self.get("access_token"):
#             token = secrets.token_urlsafe(16)
#             self.access_token = token
#             self.db_set("access_token", token, update_modified=False)

#         web_form_link = f"{frappe.utils.get_url()}/visitor-registration?token={self.access_token}"

#         formatted_expiry = ""
#         if self.invitation_expires_on:
#             formatted_expiry = format_datetime(self.invitation_expires_on, "dd-MM-yyyy hh:mm a")

#         subject = f"Visitor Pre-Registration Request from {frappe.defaults.get_user_default('Company') or 'Our Office'}"
        
#         message = f"""
#             <p>Dear Visitor,</p>
#             <p>You have been invited for a visit on <b>{self.visit_date or ''}</b>.</p>
#             <p>Please click the link below to fill in your details and generate your gate pass:</p>
#             <p><a href="{web_form_link}" style="padding: 10px 18px; background-color: #171717; color: #ffffff; text-decoration: none; border-radius: 5px; display: inline-block;">Fill Visitor Form</a></p>
#             <br>
#             <p style="color: #e53e3e; font-size: 13px;"><b>Note:</b> This invitation link will expire on <b>{formatted_expiry}</b>.</p>
#             <br>
#             <p>Regards,<br>Front Desk Team</p>
#         """

#         frappe.sendmail(
#             recipients=[self.visitor_email],
#             subject=subject,
#             message=message,
#             now=True
#         )

#         self.invitation_status = "Sent"
#         self.db_set("invitation_status", "Sent", update_modified=False)


# @frappe.whitelist(allow_guest=True)
# def get_invitation_details(token):
#     if not token:
#         return None

#     invitation = frappe.db.get_value(
#         "Visitor Invitation",
#         {"access_token": token},
#         ["name", "host_employee", "visitor_type", "visitor_email", "visit_date", "invitation_expires_on", "invitation_status"],
#         as_dict=True
#     )

#     if not invitation:
#         frappe.throw("Invalid Invitation Link.")

#     if invitation.get("invitation_status") == "Registered":
#         frappe.throw("This invitation form has already been submitted.")

#     if invitation.get("invitation_expires_on"):
#         expires_on = get_datetime(invitation.invitation_expires_on)
#         if now_datetime() > expires_on or invitation.get("invitation_status") == "Expired":
#             frappe.db.set_value("Visitor Invitation", invitation.name, "invitation_status", "Expired")
#             frappe.throw("This invitation form link has expired.")

#     return invitation


# @frappe.whitelist(allow_guest=True)
# def submit_visitor_pass(
#     token, full_name, mobile, email, visitor_type, id_type, id_number, photo, id_scan, 
#     person_to_visit=None, department=None, visit_date=None, expected_checkin=None, 
#     expected_checkout=None, purpose=None, vehicle_number=None, visitor_items=None
# ):
#     invitation = frappe.db.get_value(
#         "Visitor Invitation", 
#         {"access_token": token}, 
#         ["name", "host_employee", "visit_date", "invitation_expires_on", "invitation_status"], 
#         as_dict=True
#     )

#     if not invitation:
#         frappe.throw("Invalid or Expired Invitation Link.")

#     if invitation.get("invitation_status") == "Registered":
#         frappe.throw("This invitation has already been submitted.")

#     if invitation.get("invitation_expires_on"):
#         expires_on = get_datetime(invitation.invitation_expires_on)
#         if now_datetime() > expires_on or invitation.get("invitation_status") == "Expired":
#             frappe.db.set_value("Visitor Invitation", invitation.name, "invitation_status", "Expired")
#             frappe.throw("This invitation form link has expired.")

#     id_type_map = {
#         "Aadhaar": "Aadhar",
#         "Driving License": "Driving Licence",
#         "Voter ID": "Voter ID"
#     }
#     mapped_id_type = id_type_map.get(id_type, id_type)

#     visitor_type_map = {
#         "Guest": "Customer",
#         "Vendor": "Supplier"
#     }
#     mapped_visitor_type = visitor_type_map.get(visitor_type, visitor_type)

#     items_str = ""
#     if isinstance(visitor_items, list):
#         items_str = ", ".join([str(i) for i in visitor_items if i])
#     elif isinstance(visitor_items, str):
#         try:
#             parsed = json.loads(visitor_items)
#             if isinstance(parsed, list):
#                 items_str = ", ".join([str(i) for i in parsed if i])
#             else:
#                 items_str = visitor_items
#         except Exception:
#             items_str = visitor_items
#     elif visitor_items:
#         items_str = str(visitor_items)

#     doc = frappe.get_doc({
#         "doctype": "Visitor Pass",
#         "visitor_invitation": invitation.name,
#         "visitor_full_name": full_name,
#         "mobile_number": mobile,
#         "email_id": email,
#         "visitor_type": mapped_visitor_type,
#         "id_proof_type": mapped_id_type,
#         "id_proof_number": id_number,
#         "visitor_photo": photo,
#         "id_proof_scan": id_scan,
#         "person_to_visit": person_to_visit or invitation.host_employee,
#         "department": department,
#         "visit_date": visit_date or invitation.visit_date,
#         "expected_checkin": expected_checkin,
#         "expected_checkout": expected_checkout,
#         "purpose_of_visit": purpose,
#         "vehicle_number": vehicle_number,
#         "items": items_str,
#         "workflow_state": "Draft",
#         "docstatus": 0
#     })

#     doc.flags.ignore_workflow = True
#     doc.insert(ignore_permissions=True)

#     frappe.db.set_value("Visitor Invitation", invitation.name, {
#         "invitation_status": "Registered",
#         "visitor_pass": doc.name
#     })

#     return {"status": "success", "visitor_pass": doc.name}

# Copyright (c) 2026, Kanak Infosystems LLP and contributors
# For license information, please see license.txt

import json
import secrets
import base64
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import getdate, add_days, get_datetime, now_datetime, format_datetime
from frappe.utils.file_manager import save_file


class VisitorInvitation(Document):
    
    def validate(self):
        if self.visitor_email:
            existing = frappe.db.exists(
                "Visitor Invitation",
                {
                    "visitor_email": self.visitor_email,
                    "invitation_status": ["in", ["Pending", "Sent", "Registered"]],
                    "name": ["!=", self.name]
                }
            )
            if existing:
                status = frappe.db.get_value("Visitor Invitation", existing, "invitation_status")
                frappe.throw(
                    _("An invitation ({0}) already exists for email {1} with status '{2}'.")
                    .format(existing, self.visitor_email, status)
                )

    def before_save(self):
        if self.visit_date:
            day_before = add_days(getdate(self.visit_date), -1)
            self.invitation_expires_on = f"{day_before} 12:00:00"

    def get_indicator(self):
        status_colors = {
            "Pending": "orange",
            "Sent": "blue",
            "Registered": "green",
            "Expired": "red"
        }
        status = self.invitation_status or "Pending"
        color = status_colors.get(status, "gray")
        return [_(status), color, f"invitation_status,=,{status}"]

    @frappe.whitelist()
    def send_invitation_email(self):
        if not self.visitor_email:
            frappe.throw("Please enter a valid Visitor Email first.")

        if not self.get("access_token"):
            token = secrets.token_urlsafe(16)
            self.access_token = token
            self.db_set("access_token", token, update_modified=False)

        web_form_link = f"{frappe.utils.get_url()}/visitor-registration?token={self.access_token}"

        formatted_expiry = ""
        if self.invitation_expires_on:
            formatted_expiry = format_datetime(self.invitation_expires_on, "dd-MM-yyyy hh:mm a")

        subject = f"Visitor Pre-Registration Request from {frappe.defaults.get_user_default('Company') or 'Our Office'}"
        
        message = f"""
            <p>Dear Visitor,</p>
            <p>You have been invited for a visit on <b>{self.visit_date or ''}</b>.</p>
            <p>Please click the link below to fill in your details and generate your gate pass:</p>
            <p><a href="{web_form_link}" style="padding: 10px 18px; background-color: #171717; color: #ffffff; text-decoration: none; border-radius: 5px; display: inline-block;">Fill Visitor Form</a></p>
            <br>
            <p style="color: #e53e3e; font-size: 13px;"><b>Note:</b> This invitation link will expire on <b>{formatted_expiry}</b>.</p>
            <br>
            <p>Regards,<br>Front Desk Team</p>
        """

        frappe.sendmail(
            recipients=[self.visitor_email],
            subject=subject,
            message=message,
            now=True
        )

        self.invitation_status = "Sent"
        self.db_set("invitation_status", "Sent", update_modified=False)


def upload_file_from_base64(base64_str, filename_prefix, dt_name):
    if not base64_str or not isinstance(base64_str, str) or not base64_str.startswith("data:"):
        return base64_str

    try:
        header, data = base64_str.split(",", 1)
        file_ext = "png"
        if "jpeg" in header or "jpg" in header:
            file_ext = "jpg"
        elif "pdf" in header:
            file_ext = "pdf"

        file_content = base64.b64decode(data)
        file_name = f"{filename_prefix}_{dt_name}.{file_ext}"

        saved_file = save_file(
            fname=file_name,
            content=file_content,
            dt="Visitor Pass",
            dn=dt_name,
            is_private=0
        )
        return saved_file.file_url
    except Exception as e:
        frappe.log_error(f"File upload error for {filename_prefix}: {str(e)}")
        return None


@frappe.whitelist(allow_guest=True)
def get_active_employees():
    frappe.set_user("Administrator")
    return frappe.get_all(
        "Employee",
        fields=["name", "first_name", "employee_name", "department"],
        filters={"status": "Active"},
        limit_page_length=500
    )


@frappe.whitelist(allow_guest=True)
def get_invitation_details(token):
    if not token:
        return None

    frappe.set_user("Administrator")

    invitation = frappe.db.get_value(
        "Visitor Invitation",
        {"access_token": token},
        ["name", "host_employee", "visitor_type", "visitor_email", "visit_date", "invitation_expires_on", "invitation_status"],
        as_dict=True
    )

    if not invitation:
        frappe.throw("Invalid Invitation Link.")

    if invitation.get("invitation_status") == "Registered":
        frappe.throw("This invitation form has already been submitted.")

    if invitation.get("invitation_expires_on"):
        expires_on = get_datetime(invitation.invitation_expires_on)
        if now_datetime() > expires_on or invitation.get("invitation_status") == "Expired":
            frappe.db.set_value("Visitor Invitation", invitation.name, "invitation_status", "Expired", update_modified=False)
            frappe.db.commit()
            frappe.throw("This invitation form link has expired.")

    return invitation


@frappe.whitelist(allow_guest=True)
def submit_visitor_pass(
    token, full_name, mobile, email, visitor_type, id_type, id_number, photo, id_scan, 
    person_to_visit=None, department=None, visit_date=None, expected_checkin=None, 
    expected_checkout=None, purpose=None, vehicle_number=None, visitor_items=None
):
    frappe.set_user("Administrator")

    invitation = frappe.db.get_value(
        "Visitor Invitation", 
        {"access_token": token}, 
        ["name", "host_employee", "visit_date", "invitation_expires_on", "invitation_status"], 
        as_dict=True
    )

    if not invitation:
        frappe.throw("Invalid or Expired Invitation Link.")

    if invitation.get("invitation_status") == "Registered":
        frappe.throw("This invitation has already been submitted.")

    if invitation.get("invitation_expires_on"):
        expires_on = get_datetime(invitation.invitation_expires_on)
        if now_datetime() > expires_on or invitation.get("invitation_status") == "Expired":
            frappe.db.set_value("Visitor Invitation", invitation.name, "invitation_status", "Expired", update_modified=False)
            frappe.db.commit()
            frappe.throw("This invitation form link has expired.")

    id_type_map = {
        "Aadhaar": "Aadhar",
        "Driving License": "Driving Licence",
        "Voter ID": "Voter ID"
    }
    mapped_id_type = id_type_map.get(id_type, id_type)

    visitor_type_map = {
        "Guest": "Customer",
        "Vendor": "Supplier"
    }
    mapped_visitor_type = visitor_type_map.get(visitor_type, visitor_type)

    items_str = ""
    if isinstance(visitor_items, list):
        items_str = ", ".join([str(i) for i in visitor_items if i])
    elif isinstance(visitor_items, str):
        try:
            parsed = json.loads(visitor_items)
            if isinstance(parsed, list):
                items_str = ", ".join([str(i) for i in parsed if i])
            else:
                items_str = visitor_items
        except Exception:
            items_str = visitor_items
    elif visitor_items:
        items_str = str(visitor_items)

    doc = frappe.get_doc({
        "doctype": "Visitor Pass",
        "visitor_invitation": invitation.name,
        "visitor_full_name": full_name,
        "mobile_number": mobile,
        "email_id": email,
        "visitor_type": mapped_visitor_type,
        "id_proof_type": mapped_id_type,
        "id_proof_number": id_number,
        "person_to_visit": person_to_visit or invitation.host_employee,
        "department": department,
        "visit_date": visit_date or invitation.visit_date,
        "expected_checkin": expected_checkin,
        "expected_checkout": expected_checkout,
        "purpose_of_visit": purpose,
        "vehicle_number": vehicle_number,
        "items": items_str,
        "workflow_state": "Draft",
        "docstatus": 0
    })

    doc.flags.ignore_permissions = True
    doc.flags.ignore_workflow = True
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_permissions=True)

    photo_url = upload_file_from_base64(photo, "visitor_photo", doc.name)
    id_scan_url = upload_file_from_base64(id_scan, "id_proof_scan", doc.name)

    if photo_url:
        doc.db_set("visitor_photo", photo_url, update_modified=False)
    if id_scan_url:
        doc.db_set("id_proof_scan", id_scan_url, update_modified=False)

    frappe.db.set_value("Visitor Invitation", invitation.name, {
        "invitation_status": "Registered",
        "visitor_pass": doc.name
    }, update_modified=False)

    frappe.db.commit()

    return {"status": "success", "visitor_pass": doc.name}