import os

from mock import patch

from odoo.addons.somconnexio.tests.helper_service import crm_lead_create
from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase

from ...correos_services.shipment import DELIVERY_ARGS, CorreosShipment
from ...helpers.language import lang_to_ISO_639_1


@patch.dict(
    os.environ,
    {
        "CORREOS_USER": "user",
        "CORREOS_PASSWORD": "password",
        "CORREOS_ENVIRONMENT": "pre",
        "CORREOS_CODE": "XXX1",
    },
)
class CorreosShipmentTestCase(SCTestCase):
    @patch(
        "odoo.addons.correos_somconnexio.correos_services.shipment.PreRegistrationShipment",  # noqa
        spec=["create"],
    )
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.RawClient")
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.Package")
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.Receiver")
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.Sender")
    def test_shipment_create(
        self,
        MockSender,
        MockReceiver,
        MockPackage,
        MockRawClient,
        MockPreRegistrationShipment,
    ):
        crm_lead = crm_lead_create(
            self.env,
            self.browse_ref("somconnexio.res_partner_2_demo"),
            "mobile",
            portability=True,
        )

        expected_shipment = object
        MockPreRegistrationShipment.create.return_value = expected_shipment

        shipment = CorreosShipment().create(crm_lead, DELIVERY_ARGS["ordinary"])

        partner = crm_lead.partner_id
        mobile_isp_info = crm_lead.mobile_lead_line_ids[0].mobile_isp_info
        company = crm_lead.company_id

        self.assertEqual(shipment, expected_shipment)
        MockRawClient.assert_called_once_with(
            "user",
            "password",
            "pre",
        )
        MockReceiver.assert_called_once_with(
            name=partner.firstname,
            surname=partner.lastname,
            address=mobile_isp_info.delivery_street,
            city=mobile_isp_info.delivery_city,
            state=mobile_isp_info.delivery_state_id.name,
            zip=mobile_isp_info.delivery_zip_code,
            phone=partner.phone,
            email=partner.email,
            lang=lang_to_ISO_639_1(partner.lang),
            sms_phone=partner.phone,
        )
        MockSender.assert_called_once_with(
            name=company.name,
            nif=company.vat,
            address=company.street,
            city=company.city,
            state=company.state_id.name,
            zip=company.zip,
            phone=company.phone,
            email=company.email,
            lang="CA",
        )
        MockPackage.assert_called_once_with(
            weight=DELIVERY_ARGS["ordinary"]["weight"],
            postage_type=DELIVERY_ARGS["ordinary"]["postage_type"],
            product_code=DELIVERY_ARGS["ordinary"]["product_code"],
            delivery_modality=DELIVERY_ARGS["ordinary"]["delivery_modality"],
            weight_type=DELIVERY_ARGS["ordinary"]["weight_type"],
        )
        MockPreRegistrationShipment.create.assert_called_once_with(
            client=MockRawClient.return_value,
            code="XXX1",
            receiver=MockReceiver.return_value,
            sender=MockSender.return_value,
            package=MockPackage.return_value,
        )

    @patch(
        "odoo.addons.correos_somconnexio.correos_services.shipment.PreRegistrationShipment",  # noqa
        spec=["create"],
    )
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.RawClient")
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.Package")
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.Receiver")
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.Sender")
    def test_create_company(
        self,
        MockSender,
        MockReceiver,
        MockPackage,
        MockRawClient,
        MockPreRegistrationShipment,
    ):
        crm_lead = crm_lead_create(
            self.env,
            self.browse_ref("somconnexio.res_partner_company_demo"),
            "mobile",
            portability=True,
        )

        expected_shipment = object
        MockPreRegistrationShipment.create.return_value = expected_shipment

        shipment = CorreosShipment().create(crm_lead, DELIVERY_ARGS["ordinary"])

        partner = crm_lead.partner_id
        mobile_isp_info = crm_lead.mobile_lead_line_ids[0].mobile_isp_info
        company = crm_lead.company_id

        self.assertEqual(shipment, expected_shipment)
        MockRawClient.assert_called_once_with(
            "user",
            "password",
            "pre",
        )
        MockReceiver.assert_called_once_with(
            name=partner.name,
            nif=partner.vat,
            address=mobile_isp_info.delivery_street,
            city=mobile_isp_info.delivery_city,
            state=mobile_isp_info.delivery_state_id.name,
            zip=mobile_isp_info.delivery_zip_code,
            phone=partner.phone,
            email=partner.email,
            lang=lang_to_ISO_639_1(partner.lang),
            sms_phone=None,
        )
        MockSender.assert_called_once_with(
            name=company.name,
            nif=company.vat,
            address=company.street,
            city=company.city,
            state=company.state_id.name,
            zip=company.zip,
            phone=company.phone,
            email=company.email,
            lang="CA",
        )
        MockPackage.assert_called_once_with(
            weight=DELIVERY_ARGS["ordinary"]["weight"],
            postage_type=DELIVERY_ARGS["ordinary"]["postage_type"],
            product_code=DELIVERY_ARGS["ordinary"]["product_code"],
            delivery_modality=DELIVERY_ARGS["ordinary"]["delivery_modality"],
            weight_type=DELIVERY_ARGS["ordinary"]["weight_type"],
        )
        MockPreRegistrationShipment.create.assert_called_once_with(
            client=MockRawClient.return_value,
            code="XXX1",
            receiver=MockReceiver.return_value,
            sender=MockSender.return_value,
            package=MockPackage.return_value,
        )

    @patch(
        "odoo.addons.correos_somconnexio.correos_services.shipment.PreRegistrationShipment",  # noqa
        spec=["create"],
    )
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.RawClient")
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.Package")
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.Receiver")
    @patch("odoo.addons.correos_somconnexio.correos_services.shipment.Sender")
    def test_create_without_sms_data(
        self,
        MockSender,
        MockReceiver,
        MockPackage,
        MockRawClient,
        MockPreRegistrationShipment,
    ):
        partner = self.browse_ref("somconnexio.res_partner_2_demo")
        partner.mobile = None
        partner.phone = "934567876"

        crm_lead = crm_lead_create(
            self.env,
            partner,
            "mobile",
            portability=True,
        )

        CorreosShipment().create(crm_lead, DELIVERY_ARGS["ordinary"])

        partner = crm_lead.partner_id
        mobile_isp_info = crm_lead.mobile_lead_line_ids[0].mobile_isp_info

        MockReceiver.assert_called_once_with(
            name=partner.firstname,
            surname=partner.lastname,
            address=mobile_isp_info.delivery_street,
            city=mobile_isp_info.delivery_city,
            state=mobile_isp_info.delivery_state_id.name,
            zip=mobile_isp_info.delivery_zip_code,
            phone=partner.phone,
            email=partner.email,
            lang=lang_to_ISO_639_1(partner.lang),
            sms_phone=None,
        )
