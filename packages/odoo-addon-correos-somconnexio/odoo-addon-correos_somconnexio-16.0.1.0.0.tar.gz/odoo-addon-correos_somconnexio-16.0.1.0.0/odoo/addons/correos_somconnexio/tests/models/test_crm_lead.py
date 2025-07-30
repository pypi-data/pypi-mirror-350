from socket import error as SocketError
from requests.exceptions import ConnectionError as RequestConnectionError
from requests.exceptions import Timeout as TimeOut

from mock import patch, Mock

from correos_preregistro.errors import (
    InvalidApiResponse,
    MissingData,
    UnknownApiResponse,
)
from correos_seguimiento.services.shipment import (
    InvalidApiResponse as InvalidApiResponseSeguimiento,
)
from correos_seguimiento.services.shipment import (
    InvalidCredentials,
    InvalidEndpoint,
    UndefinedCredentials,
)
from correos_seguimiento.errors import (
    UnknownApiResponse as UnknownApiResponseSeguimiento,
)
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

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.CorreosShipment",
        return_value=Mock(spec=["create"]),
    )
    def test_create_shipment_ok(self, mock_correos_shipment):
        shipment_code = "test_code"
        label_file = "XXXXXXXX"

        mock_shipment = Mock(spec=["shipment_code", "label_file"])
        mock_shipment.shipment_code = shipment_code
        mock_shipment.label_file = label_file

        mock_correos_shipment.return_value.create.return_value = mock_shipment

        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        crm_lead.create_shipment()

        self.assertEqual(
            crm_lead.stage_id, self.env.ref("delivery_somconnexio.stage_lead6")
        )
        self.assertEqual(crm_lead.correos_tracking_code, "test_code")
        mock_correos_shipment.return_value.create.assert_called_once_with(
            crm_lead, None
        )
        attachment = self.env["ir.attachment"].search(
            [
                ("res_id", "=", crm_lead.id),
                ("res_model", "=", "crm.lead"),
            ]
        )
        self.assertTrue(attachment)

        self.assertEqual(attachment.name, "shipment_{}".format(shipment_code))
        self.assertEqual(attachment.datas.decode(), label_file)

    @patch("odoo.addons.mail.models.mail_thread.MailThread.message_post")
    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.CorreosShipment",
        side_effect=MissingData("Nombre"),
    )
    def test_create_shipment_KO_MissingData(
        self,
        mock_correos_shipment,
        mock_message_post,
    ):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        crm_lead.create_shipment()

        self.assertEqual(
            crm_lead.stage_id, self.env.ref("delivery_somconnexio.stage_lead7")
        )
        mock_message_post.assert_called_with(
            body="Error sending the delivery to Correos with the next field: Nombre"
        )

    @patch("odoo.addons.mail.models.mail_thread.MailThread.message_post")
    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.CorreosShipment",
        side_effect=UnknownApiResponse("Exception Message"),
    )
    def test_create_shipment_KO_UnknownApiResponse(
        self,
        mock_correos_shipment,
        mock_message_post,
    ):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        crm_lead.create_shipment()

        self.assertEqual(
            crm_lead.stage_id, self.env.ref("delivery_somconnexio.stage_lead7")
        )
        mock_message_post.assert_called_with(
            body="Error sending the delivery to Correos. Contact with Sistemas team."
            " Error: Exception Message"
        )

    @patch("odoo.addons.mail.models.mail_thread.MailThread.message_post")
    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.CorreosShipment",
        side_effect=InvalidApiResponse("Exception Message"),
    )
    def test_create_shipment_KO_InvalidApiResponse(
        self,
        mock_correos_shipment,
        mock_message_post,
    ):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        crm_lead.create_shipment()

        self.assertEqual(
            crm_lead.stage_id, self.env.ref("delivery_somconnexio.stage_lead7")
        )
        mock_message_post.assert_called_with(
            body="Error sending the delivery to Correos. Contact with Sistemas team."
            " Error: Exception Message"
        )

    @patch("odoo.addons.mail.models.mail_thread.MailThread.message_post")
    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.CorreosShipment",
        side_effect=Exception(),
    )
    def test_create_shipment_KO_Exception(
        self,
        mock_correos_shipment,
        mock_message_post,
    ):
        crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        crm_lead.action_set_remesa()

        with self.assertRaises(Exception):
            crm_lead.create_shipment()

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_not_delivered(
        self,
        mock_tracking_shipment,
    ):
        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = False
        mock_delivery.is_returned.return_value = False

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        self.assertEqual(crm_lead.sims_to_deliver, "one")
        crm_lead.track_delivery()
        mock_tracking_shipment.assert_called_with("XXX", "YYY", "ZZZ")
        mock_delivery.is_delivered.assert_called_once()
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_not_delivered_relabeled(self, mock_tracking_shipment):
        correos_tracking_code = "AAA"
        new_tracking_code = "BBB"

        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = False
        mock_delivery.is_returned.return_value = False
        mock_delivery.is_relabeled.return_value = True
        mock_delivery.get_relabeled_shipment_code.return_value = new_tracking_code

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": correos_tracking_code,
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        crm_lead.track_delivery()

        mock_tracking_shipment.assert_called_with("XXX", "YYY", correos_tracking_code)
        mock_delivery.is_delivered.assert_called()
        mock_delivery.is_relabeled.assert_called()
        mock_delivery.get_relabeled_shipment_code.assert_called()
        self.assertEqual(crm_lead.correos_tracking_code, new_tracking_code)
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_not_delivered_relabeled_index_error(
        self, mock_tracking_shipment
    ):
        correos_tracking_code = "AAA"

        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = False
        mock_delivery.is_relabeled.return_value = True
        mock_delivery.is_returned.return_value = False
        mock_delivery.get_relabeled_shipment_code.side_effect = IndexError(
            "IndexError while retrieving relabeled shipment code"
        )

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": correos_tracking_code,
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        with self.assertRaises(IndexError):
            crm_lead.track_delivery()

        mock_tracking_shipment.assert_called_with("XXX", "YYY", correos_tracking_code)
        mock_delivery.is_delivered.assert_called()
        mock_delivery.is_relabeled.assert_called()
        mock_delivery.get_relabeled_shipment_code.assert_called()
        self.assertEqual(crm_lead.correos_tracking_code, correos_tracking_code)
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_delivered(
        self,
        mock_tracking_shipment,
    ):
        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = True
        mock_delivery.is_relabeled.return_value = False
        mock_delivery.is_returned.return_value = False

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        self.assertEqual(crm_lead.sims_to_deliver, "one")

        crm_lead.track_delivery()

        mock_tracking_shipment.assert_called_with("XXX", "YYY", "ZZZ")
        mock_delivery.is_delivered.assert_called()
        self.assertFalse(crm_lead.sim_delivery_in_course)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_returned(self, mock_tracking_shipment):
        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_returned.return_value = True

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        self.assertEqual(crm_lead.sims_to_deliver, "one")

        crm_lead.track_delivery()

        mock_tracking_shipment.assert_called_with("XXX", "YYY", "ZZZ")
        mock_delivery.is_returned.assert_called()
        self.assertFalse(crm_lead.sim_delivery_in_course)
        self.assertFalse(crm_lead.correos_tracking_code)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_delivered_lead_line_has_sim(self, mock_tracking_shipment):
        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_delivered.return_value = True
        mock_delivery.is_returned.return_value = False
        mobile_isp_info_with_sim = self.mobile_isp_info.copy()
        mobile_isp_info_with_sim.write({"has_sim": True})
        self.mobile_lead_line_vals.update(
            {"mobile_isp_info": mobile_isp_info_with_sim.id}
        )
        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
                "lead_line_ids": [
                    (0, 0, self.mobile_lead_line_vals),
                ],
            }
        )

        # Set has sim to True to first mobile lead line
        crm_lead.mobile_lead_line_ids[1].mobile_isp_info.has_sim = True

        mobile_lead_line_with_sim = crm_lead.lead_line_ids.filtered(
            "mobile_isp_info_has_sim"
        )
        self.assertTrue(mobile_lead_line_with_sim.mobile_isp_info_has_sim)
        self.assertEqual(crm_lead.sims_to_deliver, "one")

        crm_lead.track_delivery()

        mock_tracking_shipment.assert_called_with("XXX", "YYY", "ZZZ")
        mock_delivery.is_delivered.assert_called()
        self.assertFalse(crm_lead.sim_delivery_in_course)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_undefined_credentials(
        self,
        mock_tracking_shipment,
    ):
        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_returned.side_effect = UndefinedCredentials()

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        self.assertEqual(crm_lead.sims_to_deliver, "one")
        self.assertRaisesRegex(
            UndefinedCredentials,
            "Credentials for Correos API are not defined",
            crm_lead.track_delivery,
        )
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_invalid_credentials(
        self,
        mock_tracking_shipment,
    ):
        mock_tracking_shipment_instance = mock_tracking_shipment.return_value
        mock_delivery = mock_tracking_shipment_instance.build.return_value
        mock_delivery.is_returned.side_effect = InvalidCredentials()

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        self.assertEqual(crm_lead.sims_to_deliver, "one")
        self.assertRaisesRegex(
            InvalidCredentials,
            "Credentials for Correos API are not valid",
            crm_lead.track_delivery,
        )
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch("time.sleep")
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_error_retry_3(
        self,
        delay,
        mock_tracking_shipment,
    ):
        mock_delivery = Mock(spec=["is_delivered", "is_returned"])
        mock_delivery.is_delivered.return_value = True
        mock_delivery.is_returned.return_value = False

        def is_delivered_side_effect(*args, **kwargs):
            if mock_tracking_shipment.call_count == 1:
                raise SocketError()
            elif mock_tracking_shipment.call_count < 3:
                raise TimeOut()
            elif mock_tracking_shipment.call_count == 3:
                raise RequestConnectionError()
            return mock_delivery

        mock_tracking_shipment.return_value.build.side_effect = is_delivered_side_effect

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        self.assertEqual(crm_lead.sims_to_deliver, "one")

        crm_lead.track_delivery()

        self.assertEqual(mock_tracking_shipment.call_count, 4)
        mock_delivery.is_delivered.assert_called_once()
        self.assertTrue(mock_delivery.is_delivered())
        self.assertFalse(crm_lead.sim_delivery_in_course)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch("time.sleep")
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_error_retry_4(
        self,
        delay,
        mock_tracking_shipment,
    ):  # noqa
        mock_delivery = Mock(spec=["is_delivered", "is_returned"])
        mock_delivery.is_delivered.return_value = False
        mock_delivery.is_returned.return_value = False

        def is_delivered_side_effect(*args, **kwargs):
            if mock_tracking_shipment.call_count < 21:
                raise InvalidEndpoint()
            elif mock_tracking_shipment.call_count == 21:
                raise RequestConnectionError()
            return mock_delivery

        mock_tracking_shipment.return_value.build.side_effect = is_delivered_side_effect

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        self.assertEqual(crm_lead.sims_to_deliver, "one")
        self.assertRaisesRegex(
            RequestConnectionError,
            "Connection with Correos API failed",
            crm_lead.track_delivery,
        )

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_unknown_api_response(
        self,
        mock_tracking_shipment,
    ):
        mock_tracking_shipment.return_value.build.side_effect = (
            UnknownApiResponseSeguimiento()
        )

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        self.assertEqual(crm_lead.sims_to_deliver, "one")
        self.assertRaisesRegex(
            UnknownApiResponseSeguimiento,
            "The JSON shows a data format that can't be parsed",
            crm_lead.track_delivery,
        )
        self.assertTrue(crm_lead.sim_delivery_in_course)

    @patch(
        "odoo.addons.correos_somconnexio.models.crm_lead.TrackingShipment",
        autospec=True,
    )
    @patch.dict("os.environ", {"CORREOS_USER": "XXX", "CORREOS_PASSWORD": "YYY"})
    def test_track_delivery_invalid_api_response(
        self,
        mock_tracking_shipment,
    ):
        mock_tracking_shipment.return_value.build.side_effect = (
            InvalidApiResponseSeguimiento()
        )

        crm_lead = crm_lead_create(self.env, self.partner_id, "pack", portability=True)
        crm_lead.write(
            {
                "sim_delivery_in_course": True,
                "correos_tracking_code": "ZZZ",
                "stage_id": self.env.ref("crm.stage_lead3").id,
            }
        )

        self.assertEqual(crm_lead.sims_to_deliver, "one")
        self.assertRaisesRegex(
            InvalidApiResponseSeguimiento,
            "Returned data is not JSON valid",
            crm_lead.track_delivery,
        )
        self.assertTrue(crm_lead.sim_delivery_in_course)
