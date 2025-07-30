from odoo.addons.component.core import Component


class CrmLeadListener(Component):
    _name = "crm.lead.listener"
    _inherit = "base.event.listener"
    _apply_on = ["crm.lead"]

    def on_record_write(self, record, fields=None):
        if (
            "stage_id" in fields
            and record.stage_id.id
            == self.env.ref("delivery_somconnexio.stage_lead8").id
        ):  # Stage Generating delivery
            record.with_delay().create_shipment()
