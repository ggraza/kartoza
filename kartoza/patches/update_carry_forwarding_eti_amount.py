import frappe
from kartoza.custom_py.salary_slip import get_eti_deduction

def execute():

	eti_logs = frappe.db.get_list("Employee ETI Log", {"docstatus":1}, ["name", "date", "against_salary_slip", "eti_amount"], order_by="date asc, against_salary_slip")

	for eti_log in eti_logs:
		salary_slip_doc = frappe.get_doc("Salary Slip", eti_log.against_salary_slip)
		eti_amount = get_eti_deduction(salary_slip_doc)

		carry_forwarding_eti_amount = (eti_amount.current_eti_amount + eti_amount.carry_forwarded_eti_amount) - salary_slip_doc.tax_value
		carry_forwarding_eti_amount = carry_forwarding_eti_amount if carry_forwarding_eti_amount > 0 else 0

		frappe.db.set_value(
			"Employee ETI Log",
			eti_log.name,
			"carry_forwarding_eti_amount",
			carry_forwarding_eti_amount,
			update_modified=False
		)
		frappe.db.commit()
