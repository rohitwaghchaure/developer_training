frappe.ui.form.on("Stock Entry Detail", {
	custom_add_serial__batch(frm, cdt, cdn) {
		let item = locals[cdt][cdn];
		new erpnext.CustomSerialBatchPackageSelector(
			frm, item, (r) => {
				if (r) {
					let qty = Math.abs(r.total_qty);
					if (doc.is_return) {
						qty = qty * -1;
					}

					let update_values = {
						"serial_and_batch_bundle": r.name,
						"use_serial_batch_fields": 0,
						"qty": qty / flt(item.conversion_factor || 1, precision("conversion_factor", item))
					}

					if (r.warehouse) {
						update_values["warehouse"] = r.warehouse;
					}

					frappe.model.set_value(item.doctype, item.name, update_values);
				}
			}
		);
	}
})