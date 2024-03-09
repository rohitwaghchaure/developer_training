frappe.ui.form.on("Purchase Receipt Item", {
	custom_add_serial__batch_fields(frm, cdt, cdn) {
		let row = locals[cdt][cdn];

		new erpnext.CustomSerialBatchPackageSelector(frm, row, () => {
			console.log("hii");
		})
	}
})