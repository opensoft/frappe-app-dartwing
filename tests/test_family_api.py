import json
import pytest

pytest.importorskip("frappe")
import frappe  # noqa: E402


@pytest.mark.skip(reason="Requires Frappe site context")
def test_family_slug_generation():
    name = "Test Family"
    doc = frappe.get_doc({"doctype": "Family", "family_name": name})
    doc.insert()
    try:
        assert doc.slug.startswith("test-family")
    finally:
        doc.delete()


@pytest.mark.skip(reason="Requires Frappe site context")
def test_family_member_api():
    family = frappe.get_doc({"doctype": "Family", "family_name": "API Family"})
    family.insert()
    try:
        res = frappe.call("dartwing.api.v1.add_family_member", family=family.name, full_name="John Doe")
        data = res.get("data")
        assert data
        assert data.get("full_name") == "John Doe"
    finally:
        family.delete()
