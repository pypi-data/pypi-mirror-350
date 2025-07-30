# Copyright 2025-SomItCoop SCCL(<https://gitlab.com/somitcoop>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Impact Data",
    "version": "16.0.1.1.0",
    "author": "Som It Cooperatiu SCCL",
    "website": "https://gitlab.com/somitcoop/projects/odoo-finanzas-eticas-addons.git",
    "category": "Custom",
    "summary": """
        Log structured data about the impact of the organization.
    """,
    "description": """
        Organize and provide a structured way to register and manage relevant data
        regarding the impact of the organization's activities.
    """,
    "depends": ["base", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/impact_data_category_views.xml",
        "views/impact_data_type_views.xml",
        "views/impact_data_type_uom_views.xml",
        "views/impact_data_entry_views.xml",
        "views/impact_data_menuitems.xml",
    ],
    "installable": True,
    "application": False,
    "license": "AGPL-3",
    "post_init_hook": "post_init_hook",
    "auto_install": False,
}
