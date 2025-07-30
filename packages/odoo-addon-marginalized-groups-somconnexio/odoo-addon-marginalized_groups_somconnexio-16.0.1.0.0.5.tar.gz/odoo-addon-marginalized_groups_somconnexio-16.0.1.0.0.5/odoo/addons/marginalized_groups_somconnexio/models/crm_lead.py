import base64
from odoo import models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    def _get_crm_lead_creation_email_template(self):
        if not self.partner_id.is_in_CM_program:
            return super()._get_crm_lead_creation_email_template()

        mg_partner_categ_id = self.partner_id.category_id.filtered(
            lambda c: c.parent_id
            == self.env.ref("marginalized_groups_somconnexio.marginalized_group_categ")
        )

        # Generate the PDF report
        report_id = None
        if mg_partner_categ_id == self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ_50"
        ):
            report_id = self.env.ref(
                "marginalized_groups_somconnexio.report_CM_50_conditions"
            )
        elif mg_partner_categ_id == self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ_mixed"
        ):
            report_id = self.env.ref(
                "marginalized_groups_somconnexio.report_CM_mixed_conditions"
            )
        elif mg_partner_categ_id == self.env.ref(
            "marginalized_groups_somconnexio.marginalized_group_categ_100"
        ):
            report_id = self.env.ref(
                "marginalized_groups_somconnexio.report_CM_100_conditions"
            )

        pdf_report = report_id._render_qweb_pdf(report_id, self.id)

        # Create an attachment with it
        attachment_vals = {
            "name": "particular_conditions.pdf",
            "type": "binary",
            "datas": base64.b64encode(pdf_report[0]),
            "mimetype": "application/pdf",
            "res_model": "crm.lead",
            "res_id": self.id,
        }
        attachment = self.env["ir.attachment"].create(attachment_vals)

        template = self.env.ref(
            "marginalized_groups_somconnexio.crm_lead_creation_CM_email_template"
        )

        # Attach pdf to mail.template
        template.write({"attachment_ids": [(6, 0, [attachment.id])]})

        return template
