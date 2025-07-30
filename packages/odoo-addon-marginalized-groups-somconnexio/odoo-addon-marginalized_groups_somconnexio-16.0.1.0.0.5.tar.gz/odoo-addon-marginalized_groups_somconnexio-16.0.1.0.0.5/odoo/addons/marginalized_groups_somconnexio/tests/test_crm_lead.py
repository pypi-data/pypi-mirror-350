import base64
from mock import patch
from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase
from odoo.addons.somconnexio.tests.helper_service import crm_lead_create


class CRMLeadTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner_id = self.env.ref("somconnexio.res_partner_2_demo")
        self.crm_lead = crm_lead_create(
            self.env, self.partner_id, "pack", portability=True
        )
        self.template = self.env.ref(
            "marginalized_groups_somconnexio.crm_lead_creation_CM_email_template"
        )

    @patch("odoo.addons.mail.models.mail_template.MailTemplate.send_mail")
    def test_crm_lead_action_send_email(self, mock_send_mail):
        self.crm_lead.action_send_email()

        mock_send_mail.assert_called_with(self.crm_lead.id)
        self.assertFalse(self.partner_id.is_in_CM_program)
        self.assertFalse(self.template.attachment_ids)

    @patch("odoo.addons.mail.models.mail_template.MailTemplate.send_mail")
    def test_crm_lead_action_send_email_CM_50(self, mock_send_mail):
        partner_category = self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ_50"
        )
        self.partner_id.category_id = [(4, partner_category.id)]

        self.crm_lead.action_send_email()
        attachment = self.template.attachment_ids
        content = self._extract_pdf_content(attachment)

        mock_send_mail.assert_called_once()
        self.assertTrue(self.partner_id.is_in_CM_program)
        self.assertTrue(attachment)
        self.assertEqual(attachment.name, "particular_conditions.pdf")
        self.assertIn("Preu: import equivalent al 50% del PVP", content)
        self.assertNotIn(
            "import equivalent a 0€ del servei de fibra 300MB sense fix", content
        )

    @patch("odoo.addons.mail.models.mail_template.MailTemplate.send_mail")
    def test_crm_lead_action_send_email_CM_100(self, mock_send_mail):
        partner_category = self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ_100"
        )

        self.partner_id.category_id = [(4, partner_category.id)]
        self.crm_lead.action_send_email()
        attachment = self.template.attachment_ids
        content = self._extract_pdf_content(attachment)

        mock_send_mail.assert_called_once()
        self.assertTrue(self.partner_id.is_in_CM_program)
        self.assertTrue(attachment)
        self.assertEqual(attachment.name, "particular_conditions.pdf")
        self.assertIn("Preu: import equivalent a 0€.", content)

    @patch("odoo.addons.mail.models.mail_template.MailTemplate.send_mail")
    def test_crm_lead_action_send_email_CM_mixed(self, mock_send_mail):
        partner_category = self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ_mixed"
        )
        self.partner_id.category_id = [(4, partner_category.id)]

        self.crm_lead.action_send_email()
        attachment = self.template.attachment_ids
        content = self._extract_pdf_content(attachment)

        mock_send_mail.assert_called_once()
        self.assertTrue(self.partner_id.is_in_CM_program)
        self.assertTrue(attachment)
        self.assertEqual(attachment.name, "particular_conditions.pdf")
        self.assertIn("import equivalent al 50% del PVP", content)
        self.assertIn(
            "import equivalent a 0€ del servei de fibra 300MB sense fix", content
        )

    @patch("odoo.addons.mail.models.mail_template.MailTemplate.send_mail")
    def test_crm_lead_action_send_email_CM_multiple_categ(self, mock_send_mail):
        cm_category = self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ_mixed"
        )
        other_category = self.env.ref("base.res_partner_category_3")
        self.partner_id.category_id = cm_category + other_category

        self.crm_lead.action_send_email()
        attachment = self.template.attachment_ids
        content = self._extract_pdf_content(attachment)

        mock_send_mail.assert_called_once()
        self.assertTrue(self.partner_id.is_in_CM_program)
        self.assertTrue(attachment)
        self.assertEqual(attachment.name, "particular_conditions.pdf")
        self.assertIn("import equivalent al 50% del PVP", content)
        self.assertIn(
            "import equivalent a 0€ del servei de fibra 300MB sense fix", content
        )

    @patch("odoo.addons.mail.models.mail_template.MailTemplate.send_mail")
    def test_crm_lead_action_send_email_spanish(self, mock_send_mail):
        partner_category = self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ_mixed"
        )
        self.partner_id.write(
            {
                "lang": "es_ES",
                "category_id": [(4, partner_category.id)],
            }
        )

        self.crm_lead.action_send_email()

        mock_send_mail.assert_called_once()

        attachment = self.template.attachment_ids
        self.assertTrue(attachment)
        self.assertEqual(attachment.name, "particular_conditions.pdf")

    def _extract_pdf_content(self, attachment):
        pdf_content = base64.b64decode(attachment.datas)
        return pdf_content.decode("utf-8")
