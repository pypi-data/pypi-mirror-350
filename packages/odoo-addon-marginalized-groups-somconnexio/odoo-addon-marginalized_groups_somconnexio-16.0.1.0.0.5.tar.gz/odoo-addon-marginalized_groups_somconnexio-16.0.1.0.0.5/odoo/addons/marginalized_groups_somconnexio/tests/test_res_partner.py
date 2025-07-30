from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase


class ResPartnerTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner_id = self.env.ref("somconnexio.res_partner_2_demo")

    def test_is_in_CM_program(self):
        # Assign a category that is not in the CM program
        category = self.env.ref("base.res_partner_category_14")
        self.partner_id.category_id = [(4, category.id)]
        self.assertFalse(self.partner_id.is_in_CM_program)

        # Assign a category that is in the CM program
        category = self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ_50"
        )
        self.partner_id.category_id = [(4, category.id)]
        self.assertTrue(self.partner_id.is_in_CM_program)

    def test_is_CM_organization(self):
        organization_category = self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_organization"
        )
        self.assertFalse(self.partner_id.is_supplier)
        self.assertFalse(self.partner_id.is_CM_organization)

        self.partner_id.is_supplier = True
        self.assertFalse(self.partner_id.is_CM_organization)

        self.partner_id.category_id = [(4, organization_category.id)]
        self.assertTrue(self.partner_id.is_CM_organization)
