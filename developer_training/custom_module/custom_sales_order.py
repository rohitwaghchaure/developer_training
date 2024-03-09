import frappe
from frappe import _
from frappe.utils import today, flt
from erpnext.selling.doctype.sales_order.sales_order import SalesOrder

class CustomSalesOrder(SalesOrder):
	def validate_po(self):
		print("hii")

def on_submit_events(doc, method=None):
	return
	itemwise_projected_qty = get_projected_qty_of_items(doc)

	po_items = frappe._dict({})
	for row in doc.items:
		key = (row.item_code, row.warehouse)
		if itemwise_projected_qty.get(key) and itemwise_projected_qty.get(key) < 0:
			po_items.setdefault(key, frappe._dict({
				"projected_qty": flt(abs(itemwise_projected_qty.get(key)))
			}))

	if po_items:
		set_default_supplier(po_items)
		create_purchase_order(po_items)

def get_projected_qty_of_items(doc) -> dict:
	items, warehouses = [], []

	for row in doc.items:
		items.append(row.item_code)
		warehouses.append(row.warehouse)

	item_details = {}
	data = frappe.get_all("Bin",
		fields = ["item_code", "warehouse", "projected_qty"],
		filters = {"item_code": ("in", items), "warehouse": ("in", warehouses)})

	for row in data:
		item_details.setdefault((row.item_code, row.warehouse), row.projected_qty)

	return item_details

def set_default_supplier(po_items):
	items = []
	for key in po_items:
		items.append(key[0])

	supplier_dict = {}
	data = frappe.get_all("Item Default",
		fields = ["parent", "default_supplier"],
		filters = {"parent": ("in", items)})

	for row in data:
		supplier_dict.setdefault(row.parent, row.default_supplier)

	for key in po_items:
		if key[0] in supplier_dict:
			po_items[key].supplier = supplier_dict.get(key[0]) or "Default Supplier"
		else:
			po_items[key].supplier = "Default Supplier"

def create_purchase_order(po_items):
	for (item_code, warehouse), value in po_items.items():
		po_doc = frappe.get_doc({
			"doctype": "Purchase Order",
			"supplier": value.supplier,
			"schedule_date": today(),
			"items": [{
				"item_code": item_code,
				"warehouse": warehouse,
				"qty": value.projected_qty,
				"schedule_date": today()
			}]
		})

		po_doc.save()

		frappe.msgprint(_(f"Purchase order {po_doc.name} created"))