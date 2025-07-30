import psycopg2

from odoo.tests import common, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install", "impact_data_registry")
class TestImpactDataType(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.type = self.env["impact.data.type"].create(
            {
                "name": "Type",
                "description": "Type description",
                "company_id": self.env.company.id,
            }
        )

    def test_required_fields(self):
        with self.assertRaises(psycopg2.DatabaseError), mute_logger("odoo.sql_db"):
            self.env["impact.data.type"].create({})

    def test_name_uniqueness(self):
        with self.assertRaises(psycopg2.DatabaseError), mute_logger("odoo.sql_db"):
            self.env["impact.data.type"].create(
                {
                    "name": "Type",
                    "company_id": self.env.company.id,
                }
            )
