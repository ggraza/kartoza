frappe.ui.form.on("Employee", {
	"onload":function(frm){
		frm.set_query('payroll_payable_account', function(doc) {
			return {
				filters: {
					"is_company_account": 1,
					"account": ["!=", null]
				}
			};
		});

		if(frm.doc.company && frm.doc.payroll_payable_account){
			frm.toggle_display("eligible_for_paye", frm.doc.__onload && frm.doc.__onload.is_forex_employee);
		}
	}
})