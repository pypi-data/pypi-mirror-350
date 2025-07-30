from odoo import api, fields, models


class CRMLeadPrintSIMDeliveryLabelWizard(models.TransientModel):
    _name = "crm.lead.print.sim.delivery.label.wizard"
    crm_lead_ids = fields.Many2many("crm.lead")

    def button_print_delivery(self):
        attachment_ids = self._get_attachments(self.crm_lead_ids.ids).ids
        if not attachment_ids:
            return
        url = "/web/binary/download_attachments?attachment_ids=%s" % ",".join(
            [str(id) for id in attachment_ids]
        )
        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }

    def _get_attachments(self, crm_lead_ids):
        return self.env["ir.attachment"].search(
            [
                ("res_model", "=", "crm.lead"),
                ("res_id", "in", crm_lead_ids),
                ("name", "like", "shipment_%"),
            ]
        )

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        crm_lead_ids = self.env.context["active_ids"]
        defaults["crm_lead_ids"] = crm_lead_ids
        return defaults
