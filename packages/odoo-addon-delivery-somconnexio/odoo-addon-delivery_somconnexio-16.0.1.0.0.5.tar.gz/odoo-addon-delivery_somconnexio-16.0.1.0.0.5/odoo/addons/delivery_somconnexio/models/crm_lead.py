import logging

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _inherit = "crm.lead"
    sims_to_deliver = fields.Selection(
        [("none", "None"), ("one", "One"), ("multiple", "multiple")],
        compute="_compute_sims_to_deliver",
        store=True,
    )
    sim_delivery_in_course = fields.Boolean()
    correos_tracking_code = fields.Char(string="Correos Tracking Code")

    @api.depends(
        "lead_line_ids", "lead_line_ids.mobile_isp_info_has_sim", "lead_line_ids.active"
    )
    def _compute_sims_to_deliver(self):
        for crm in self:
            mobile_lines_without_sims = crm.lead_line_ids.filtered(
                lambda line: (
                    line.is_mobile and not line.mobile_isp_info_has_sim and line.active
                )
            )
            if not mobile_lines_without_sims:
                crm.sims_to_deliver = "none"
            elif len(mobile_lines_without_sims) == 1:
                crm.sims_to_deliver = "one"
            else:
                crm.sims_to_deliver = "multiple"

    def validate_won(self):
        try:
            super().validate_won()
        except ValidationError as error:
            if self.stage_id != self.env.ref("delivery_somconnexio.stage_lead6"):
                raise error

    def validate_remesa(self):
        try:
            super().validate_remesa()
        except ValidationError as error:
            if self.stage_id != self.env.ref("delivery_somconnexio.stage_lead6"):
                raise error

    def action_set_delivery_generated(self):
        for crm_lead in self:
            crm_lead.sim_delivery_in_course = True
            crm_lead.write(
                {"stage_id": self.env.ref("delivery_somconnexio.stage_lead8").id}
            )

    def validate_leads_to_generate_SIM_delivery(self):
        self.ensure_one()
        if self.stage_id not in [
            self.env.ref("crm.stage_lead3"),
            self.env.ref("delivery_somconnexio.stage_lead8"),
        ]:
            raise ValidationError(
                _("The crm lead with id {} must be in remesa stage.").format(self.id)
            )

        if self.sims_to_deliver == "none":
            raise ValidationError(
                _("The crm lead with id {} does not need SIM delivery.").format(self.id)
            )

    def create_shipment(self, delivery_args=None):
        raise NotImplementedError()

    def track_delivery(self):
        raise NotImplementedError()

    @api.model
    def cron_track_delivery(self):
        domain = [
            ("stage_id", "=", self.env.ref("crm.stage_lead4").id),
            ("sims_to_deliver", "!=", "none"),
            ("sim_delivery_in_course", "=", True),
        ]
        crm_leads = self.search(domain)
        for lead in crm_leads:
            lead.with_delay(max_retries=3).track_delivery()

    def action_generate_express_delivery(self):
        for crm_lead in self:
            crm_lead.with_delay().create_shipment()
