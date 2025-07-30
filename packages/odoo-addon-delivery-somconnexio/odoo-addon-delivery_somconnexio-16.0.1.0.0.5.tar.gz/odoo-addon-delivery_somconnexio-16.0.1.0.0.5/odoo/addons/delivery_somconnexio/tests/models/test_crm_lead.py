from odoo.addons.somconnexio.tests.helper_service import crm_lead_create, random_icc
from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase


class CRMLeadTest(SCTestCase):
    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)

        self.partner_id = self.env.ref("somconnexio.res_partner_2_demo")
        self.partner_iban = self.partner_id.bank_ids[0].sanitized_acc_number

        self.crm_lead = crm_lead_create(self.env, self.partner_id, "mobile")
        self.crm_lead_mobile = self.crm_lead.lead_line_ids[
            0
        ].mobile_isp_info.phone_number
        self.product_pack_mobile = self.env.ref(
            "somconnexio.TrucadesIllimitades20GBPack"
        )
        self.product_mobile = self.env.ref("somconnexio.TrucadesIllimitades20GB")
        self.product_pack_fiber = self.env.ref("somconnexio.Fibra100Mb")
        self.mobile_isp_info = self.env["mobile.isp.info"].create(
            {"type": "new", "icc": random_icc(self.env), "phone_number": "616382488"}
        )
        self.mobile_lead_line_vals = {
            "name": "TEST",
            "product_id": self.product_mobile.id,
            "mobile_isp_info": self.mobile_isp_info.id,
            "iban": self.partner_iban,
        }

        self.CRMLeadLine = self.env["crm.lead.line"]

    def test_crm_lead_action_set_delivery_generated(self):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        self.assertFalse(crm_lead.sim_delivery_in_course)

        crm_lead.action_set_delivery_generated()

        self.assertTrue(crm_lead.sim_delivery_in_course)
        self.assertEqual(
            crm_lead.stage_id, self.env.ref("delivery_somconnexio.stage_lead8")
        )

    def test_create_shipment_not_implemented(self):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )

        self.assertRaises(
            NotImplementedError,
            crm_lead.create_shipment,
        )

    def test_track_delivery_not_implemented(self):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )

        self.assertRaises(
            NotImplementedError,
            crm_lead.track_delivery,
        )
