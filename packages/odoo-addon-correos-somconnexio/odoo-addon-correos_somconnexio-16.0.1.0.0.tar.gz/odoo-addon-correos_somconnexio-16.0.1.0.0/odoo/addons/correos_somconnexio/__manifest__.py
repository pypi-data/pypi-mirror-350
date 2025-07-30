{
    "name": "Odoo Som Connexió Correos integration",
    "version": "16.0.1.0.0",
    "depends": [
        "delivery_somconnexio",
    ],
    "external_dependencies": {
        "python": [
            "correos_preregistro",
            "correos_seguimiento",
        ],
    },
    "author": "Coopdevs Treball SCCL, " "Som Connexió SCCL",
    "website": "https://coopdevs.org",
    "category": "Cooperative management",
    "license": "AGPL-3",
    "data": [
        "data/queue_job_config.xml",
    ],
    "demo": [],
}
