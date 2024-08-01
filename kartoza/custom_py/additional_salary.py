import frappe
from frappe import _
from frappe.utils import (comma_and, date_diff, formatdate, get_link_to_form,
                          getdate)
from hrms.payroll.doctype.additional_salary.additional_salary import \
    AdditionalSalary


class CustomAdditionalSalary(AdditionalSalary):
	def validate_duplicate_additional_salary(self):
		if not self.overwrite_salary_structure_amount:
			return

		existing_additional_salary = frappe.db.exists(
			"Additional Salary",
			{
				"name": ["!=", self.name],
				"salary_component": self.salary_component,
				"payroll_date": self.payroll_date,
				"overwrite_salary_structure_amount": 1,
				"is_company_contribution": self.is_company_contribution,
				"employee": self.employee,
				"docstatus": 1,
			},
		)

		if existing_additional_salary:
			msg = _(
				"Additional Salary for this salary component with {0} enabled already exists for this date"
			).format(frappe.bold("Overwrite Salary Structure Amount"))
			msg += "<br><br>"
			msg += _("Reference: {0}").format(
				get_link_to_form("Additional Salary", existing_additional_salary)
			)
			frappe.throw(msg, title=_("Duplicate Overwritten Salary"))