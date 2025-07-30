from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ImpactDataCategory(models.Model):
    _name = "impact.data.category"
    _description = "Impact Data Category"
    _rec_name = "complete_name"
    _order = "complete_name asc"
    _check_company_auto = True

    name = fields.Char(string="Name", required=True)
    complete_name = fields.Char(
        string=_("Complete Name"),
        compute="_compute_complete_name",
        recursive=True,
        index=True,
        store=True,
        help=_("Complete category/subcategory name."),
    )
    description = fields.Text(string="Description")
    parent_id = fields.Many2one(
        comodel_name="impact.data.category",
        string=_("Parent Category"),
        ondelete="restrict",
        index=True,
        help=_("Parent category of the category/subcategory."),
    )
    child_ids = fields.One2many(
        comodel_name="impact.data.category",
        inverse_name="parent_id",
        string=_("Subcategories"),
        readonly=True,
        help=_("Related subcategories."),
    )
    unallowed_parent_ids = fields.Many2many(
        comodel_name="impact.data.category",
        compute="_compute_unallowed_parent_ids",
        recursive=True,
        help=_("Categories that cannot be parent of this category."),
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string=_("Company"),
        default=lambda self: self.env.company,
        help=_("Company to which the category belongs."),
    )

    @api.depends("child_ids", "child_ids.unallowed_parent_ids")
    def _compute_unallowed_parent_ids(self):
        for record in self:
            record.unallowed_parent_ids = (
                record.child_ids.mapped("unallowed_parent_ids")
                | record.child_ids
                | record
            )

    @api.depends("name", "parent_id.complete_name")
    def _compute_complete_name(self):
        for record in self:
            if record.parent_id:
                record.complete_name = (
                    f"{record.parent_id.complete_name} / {record.name}"
                )
            else:
                record.complete_name = record.name

    @api.constrains("parent_id")
    def _check_parent_not_circular(self):
        if not self._check_recursion():
            raise ValidationError(_("You cannot create recursive categories."))

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id)",
            "Category/subcategory name must be unique by company.",
        ),
        (
            "parent_id_not_itself",
            "check(parent_id != id)",
            "Category/subcategory cannot be parent of itself.",
        )
    ]
