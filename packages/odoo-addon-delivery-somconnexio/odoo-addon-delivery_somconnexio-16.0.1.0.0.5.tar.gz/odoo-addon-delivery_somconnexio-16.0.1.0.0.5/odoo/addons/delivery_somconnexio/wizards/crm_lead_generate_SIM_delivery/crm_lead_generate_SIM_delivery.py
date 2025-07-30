from odoo import api, fields, models


class CRMLeadGenerateSIMDeliveryWizard(models.TransientModel):
    _name = "crm.lead.generate.sim.delivery.wizard"
    crm_lead_ids = fields.Many2many("crm.lead")

    def button_generate_delivery(self):
        for lead in self.crm_lead_ids:
            lead.action_set_delivery_generated()
        return True

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        crm_lead_ids = self.env.context["active_ids"]
        defaults["crm_lead_ids"] = crm_lead_ids
        return defaults
