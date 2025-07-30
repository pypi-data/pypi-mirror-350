from odoo import models, fields, api, _


class ImpactDataEntry(models.Model):
    _name = "impact.data.entry"
    _description = "Impact Data Log"
    _order = "year desc"
    _check_company_auto = True

    year = fields.Integer(
        string=_("Year"),
        default=lambda self: fields.Date.today().year,
        help=_("Year of the data entry."),
    )
    analytic_account_id = fields.Many2one(
        comodel_name="account.analytic.account",
        string=_("Analytic Account"),
        ondelete="restrict",
        help=_("Analytic account to which the data entry is related."),
    )
    category_id = fields.Many2one(
        comodel_name="impact.data.category",
        string=_("Category / Subcategory"),
        ondelete="restrict",
        help=_("Category to which the data entry is related."),
    )
    parent_category_id = fields.Many2one(
        comodel_name="impact.data.category",
        related="category_id.parent_id",
        string=_("Parent Category"),
        store=True,
        help=_("Parent category of the category/subcategory."),
    )
    type_id = fields.Many2one(
        comodel_name="impact.data.type",
        string=_("Type"),
        ondelete="restrict",
        help=_("Type of the data entry."),
    )
    type_name = fields.Char(
        related="type_id.name",
        string=_("Type Name"),
        store=True,
        help=_("Name of the type of the data entry."),
    )
    value = fields.Float(
        string=_("Value"), required=True, help=_("Value of the data entry.")
    )
    type_uom_id = fields.Many2one(
        related="type_id.type_uom_id",
        string=_("Unit of Measure"),
        store=True,
        help=_("Unit of measure for the data entry."),
    )
    comment = fields.Text(
        string=_("Comment"), help=_("Additional information about the data entry.")
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string=_("Company"),
        default=lambda self: self.env.company,
        help=_("Company to which the data entry belongs."),
    )

    @api.constrains("year")
    def _check_year(self):
        for record in self:
            if record.year and record.year < 1970:
                raise ValueError(_("Year must be greater or equal than 1970."))
