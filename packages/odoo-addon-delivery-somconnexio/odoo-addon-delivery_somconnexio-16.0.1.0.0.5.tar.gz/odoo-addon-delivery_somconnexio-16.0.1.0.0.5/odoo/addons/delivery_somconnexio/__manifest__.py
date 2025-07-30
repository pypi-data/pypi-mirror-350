{
    "name": "Odoo Som Connexió Delivery processes customizations",
    "version": "16.0.1.0.0",
    "depends": [
        "component",
        "somconnexio",
    ],
    "author": "Coopdevs Treball SCCL, " "Som Connexió SCCL",
    "website": "https://coopdevs.org",
    "category": "Cooperative management",
    "license": "AGPL-3",
    "data": [
        "data/crm_stage_data.xml",
        "views/crm_lead.xml",
        "crons/crm_track_correos_delivery_cron.xml",
        "wizards/crm_lead_generate_SIM_delivery/crm_lead_generate_SIM_delivery.xml",
        "wizards/crm_lead_print_SIM_delivery_label/crm_lead_print_SIM_delivery_label.xml",  # noqa
        "security/ir.model.access.csv",
    ],
    "demo": [],
    "external_dependencies": {},
}
