from odoo import models, fields, api, _


class ImpactDataType(models.Model):
    _name = "impact.data.type"
    _description = "Impact Data Type"
    _rec_name = "display_name"
    _order = "display_name asc"

    name = fields.Char(string=_("Name"), required=True, help=_("Name of the type."))
    display_name = fields.Char(
        string=_("Display Name"),
        compute="_compute_display_name",
        store=True,
        help=_("Display name of the type."),
    )
    description = fields.Text(
        string=_("Description"), help=_("Description of the type.")
    )
    type_uom_id = fields.Many2one(
        comodel_name="impact.data.type.uom",
        string=_("Unit of Measure"),
        ondelete="restrict",
        help=_("Unit of measure for the type."),
    )
    company_id = fields.Many2one(
        comodel_name="res.company",
        string=_("Company"),
        default=lambda self: self.env.company,
        help=_("Company to which the type belongs."),
    )

    @api.depends("name", "type_uom_id")
    def _compute_display_name(self):
        for record in self:
            if record.type_uom_id:
                record.display_name = f"{record.type_uom_id.name} / {record.name}"
            else:
                record.display_name = record.name

    _sql_constraints = [
        (
            "name_company_uniq",
            "unique(name, company_id)",
            "Type name must be unique by company.",
        )
    ]


class ImpactDataTypeUoM(models.Model):
    _name = "impact.data.type.uom"
    _description = "Impact Data Type UoM"
    _rec_name = "name"
    _order = "name asc"

    name = fields.Char(string=_("Name"), required=True, help=_("Name of the type."))
