import frappe
from frappe.utils import flt

def execute():

	today = frappe.utils.today()
	start_date, end_date = frappe.db.get_value(
		"Payroll Period",
		{
			"start_date": ("<=", today),
			"end_date": (">=", today),
		},
		["start_date", "end_date"],
	)
	salary_slips = frappe.get_all(
		"Salary Slip",
		filters={
			"start_date": [">=", start_date],
			"end_date": ["<=", end_date],
			"docstatus": 1,
		},
		fields=["name"],
	)

	for salary_slip in salary_slips:
		salary_slip_doc = frappe.get_doc("Salary Slip", salary_slip.name)
		annual_bonus = salary_slip_doc.get_bonus_amount()
		provision_for_tax_on_annual_bonus = 0

		if annual_bonus:
			provision_for_tax_on_annual_bonus = flt(
				annual_bonus / 12, salary_slip_doc.precision("custom_provision_for_tax_on_annual_bonus")
			)

		frappe.db.set_value(
			"Salary Slip",
			salary_slip.name,
			"custom_provision_for_tax_on_annual_bonus",
			provision_for_tax_on_annual_bonus,
		)
