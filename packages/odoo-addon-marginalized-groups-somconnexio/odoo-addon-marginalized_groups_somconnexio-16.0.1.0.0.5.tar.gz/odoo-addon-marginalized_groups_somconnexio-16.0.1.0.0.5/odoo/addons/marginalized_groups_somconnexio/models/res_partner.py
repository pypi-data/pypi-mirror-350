from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    is_in_CM_program = fields.Boolean(
        compute="_compute_is_in_CM_program",
        store=True,
    )
    is_CM_organization = fields.Boolean(
        compute="_compute_is_CM_organization",
        store=True,
    )
    marginalized_group_agent_id = fields.Many2one(
        "res.partner",
        string="Marginalized group agent",
    )

    @api.depends("category_id")
    def _compute_is_in_CM_program(self):
        category = self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ",
            raise_if_not_found=False,
        )
        if not category:
            return
        for partner in self:
            # Check if the partner is in the marginalized group category
            partner.is_in_CM_program = bool(category.child_ids & partner.category_id)
            if not partner.is_in_CM_program:
                partner.marginalized_group_agent_id = False

    @api.depends("category_id")
    def _compute_is_CM_organization(self):
        organization_category = self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_organization",
            raise_if_not_found=False,
        )
        if not organization_category:
            return
        for partner in self:
            # Check if the partner is in the marginalized group organization category
            partner.is_CM_organization = bool(
                partner.is_supplier and (organization_category & partner.category_id)
            )
