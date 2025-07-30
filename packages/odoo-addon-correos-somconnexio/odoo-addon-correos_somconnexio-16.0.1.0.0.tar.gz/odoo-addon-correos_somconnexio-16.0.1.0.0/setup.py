import setuptools

setuptools.setup(
    setup_requires=['setuptools-odoo'],
    odoo_addon={
        "external_dependencies_override": {
            "python": {
                "correos_preregistro": "correos-preregistro==0.0.6",
                "correos_seguimiento": "correos-seguimiento==0.3.0",
            },
        },
    },
)
