import psycopg2

from odoo.tools import mute_logger
from odoo.tests import common, tagged

from lxml import etree


@tagged("post_install", "-at_install", "impact_data_registry")
class TestImpactDataCategory(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.category_parent = self.env["impact.data.category"].create(
            {"name": "Category", "description": "Category description"}
        )
        self.category_child = self.env["impact.data.category"].create(
            {
                "name": "Subcategory",
                "description": "Subcategory description",
                "parent_id": self.category_parent.id,
            }
        )
        self.category_grandchild = self.env["impact.data.category"].create(
            {
                "name": "Sub-subcategory",
                "description": "Sub-subcategory description",
                "parent_id": self.category_child.id,
            }
        )

    def test_recursion_prevention_orm(self):
        with self.assertRaises(psycopg2.DatabaseError), mute_logger("odoo.sql_db"):
            self.category_parent.write({"parent_id": self.category_child.id})
        with self.assertRaises(psycopg2.DatabaseError), mute_logger("odoo.sql_db"):
            self.category_parent.write({"parent_id": self.category_parent.id})

    def test_recursion_prevention_sql(self):
        with self.assertRaises(psycopg2.DatabaseError), mute_logger("odoo.sql_db"):
            self.env.cr.execute(
                """
                UPDATE impact_data_category
                SET parent_id = %s
                WHERE id = %s
                """
                % (self.category_child.id, self.category_parent.id)
            )
        with self.assertRaises(psycopg2.DatabaseError), mute_logger("odoo.sql_db"):
            self.env.cr.execute(
                """
                UPDATE impact_data_category
                SET parent_id = %s
                WHERE id = %s
                """
                % (self.category_parent.id, self.category_parent.id)
            )

    def test_recursion_prevention_ui(self):
        form_view = self.env["impact.data.category"].get_view(view_type="form")
        arch = form_view["arch"]
        tree = etree.fromstring(arch)
        node = tree.xpath("//field[@name='parent_id']")[0]
        domain = node.attrib.get("domain")

        self.category_parent._compute_unallowed_parent_ids()
        unallowed_parent_ids = self.category_parent.unallowed_parent_ids.ids

        self.assertEqual(domain, "[('id', 'not in', unallowed_parent_ids)]")
        self.assertIn(self.category_parent.id, unallowed_parent_ids)
        self.assertIn(self.category_child.id, unallowed_parent_ids)
        self.assertIn(self.category_grandchild.id, unallowed_parent_ids)

    def test_complete_name_recompute(self):
        self.category_parent.write({"name": "Category Renamed"})
        self.assertEqual(self.category_parent.complete_name, "Category Renamed")
        self.assertEqual(
            self.category_child.complete_name, "Category Renamed / Subcategory"
        )
        self.assertEqual(
            self.category_grandchild.complete_name,
            "Category Renamed / Subcategory / Sub-subcategory",
        )
        self.category_child.write({"name": "Subcategory Renamed"})
        self.assertEqual(self.category_parent.complete_name, "Category Renamed")
        self.assertEqual(
            self.category_child.complete_name, "Category Renamed / Subcategory Renamed"
        )
        self.assertEqual(
            self.category_grandchild.complete_name,
            "Category Renamed / Subcategory Renamed / Sub-subcategory",
        )

    def test_required_fields(self):
        with self.assertRaises(psycopg2.DatabaseError), mute_logger("odoo.sql_db"):
            self.env["impact.data.category"].create(
                {"description": "Category description"}
            )

    def test_sql_constraints(self):
        with self.assertRaises(psycopg2.DatabaseError), mute_logger("odoo.sql_db"):
            self.env["impact.data.category"].create(
                {"name": "Category", "company_id": self.env.ref("base.main_company").id}
            )
