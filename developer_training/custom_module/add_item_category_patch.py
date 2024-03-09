import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_field

def execute():
    create_custom_field("Item", {
        "fieldname": "item_category",
        "label": "Item Category",
        "fieldtype": "Data",
        "insert_after": "stock_uom",
    })

    create_custom_field("Item", {
        "fieldname": "sub_item_category",
        "label": "Sub Item Category",
        "fieldtype": "Data",
        "insert_after": "item_category",
    })