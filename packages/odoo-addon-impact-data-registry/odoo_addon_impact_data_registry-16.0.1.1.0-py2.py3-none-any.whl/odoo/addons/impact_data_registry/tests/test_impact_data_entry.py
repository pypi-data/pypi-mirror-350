import psycopg2

from odoo.tests import common, tagged
from odoo.tools import mute_logger


@tagged("post_install", "-at_install", "impact_data_registry")
class TestImpactDataEntry(common.TransactionCase):
    def setUp(self):
        super().setUp()

        self.category = self.env["impact.data.category"].create(
            {"name": "Category", "description": "Category description"}
        )
        self.type = self.env["impact.data.type"].create(
            {"name": "Type", "description": "Type description"}
        )
        self.plan_id = self.env["account.analytic.plan"].create(
            {"name": "Plan", "company_id": self.env.company.id}
        )
        self.account_analytic = self.env["account.analytic.account"].create(
            {
                "name": "Account Analytic",
                "company_id": self.env.company.id,
                "plan_id": self.plan_id.id,
            }
        )

    def test_required_fields(self):
        with self.assertRaises(psycopg2.DatabaseError), mute_logger("odoo.sql_db"):
            self.env["impact.data.entry"].create(
                {
                    "year": 1970,
                    "category_id": self.category.id,
                    "type_id": self.type.id,
                    "analytic_account_id": self.account_analytic.id,
                }
            )

    def test_year_constraint(self):
        with self.assertRaises(ValueError):
            self.env["impact.data.entry"].create(
                {
                    "year": 1969,
                    "category_id": self.category.id,
                    "type_id": self.type.id,
                    "analytic_account_id": self.account_analytic.id,
                    "value": 1,
                }
            )
