import logging
import os
import re

from correos_preregistro.client import RawClient
from correos_preregistro.resources import Package, Receiver, Sender
from correos_preregistro.services.shipment import PreRegistrationShipment

from ..helpers.language import lang_to_ISO_639_1

_logger = logging.getLogger(__name__)

# TODO: Move to delivery carrier entity
DELIVERY_ARGS = {
    "ordinary": {
        "weight": 500,
        "postage_type": "FP",
        "product_code": "S0132",
        "delivery_modality": "ST",
        "weight_type": "R",
    },
    # TODO: Change the express data
    "express": {
        "weight": 500,
        "postage_type": "FP",
        "product_code": "S0292",
        "delivery_modality": "ST",
        "weight_type": "R",
    },
}


class CorreosShipment:
    def __init__(self):
        user = os.getenv("CORREOS_USER")
        password = os.getenv("CORREOS_PASSWORD")
        env = os.getenv("CORREOS_ENVIRONMENT", default="pre")
        self.client_code = os.getenv("CORREOS_CODE")
        self.client = RawClient(user, password, env)

    def create(self, crm_lead, delivery_args=None):
        if not delivery_args:
            delivery_args = DELIVERY_ARGS["ordinary"]

        # Call to Correos
        _logger.debug("Creating the shipment to send to Correos")
        try:
            return self._create_correos_shipment(crm_lead, delivery_args)
        except Exception as e:
            _logger.error("Error sending the shipment to Correos")
            raise e

    def _create_correos_shipment(self, crm_lead, delivery_args):
        company = crm_lead.company_id

        receiver = self._create_receiver(crm_lead)

        _logger.debug("Creating the sender")
        sender = Sender(
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
        _logger.debug("Creating the package")
        package = Package(
            weight=delivery_args["weight"],
            postage_type=delivery_args["postage_type"],
            product_code=delivery_args["product_code"],
            delivery_modality=delivery_args["delivery_modality"],
            weight_type=delivery_args["weight_type"],
        )
        _logger.debug("Send the shipment to Correos")
        shipment = PreRegistrationShipment.create(
            client=self.client,
            code=self.client_code,
            receiver=receiver,
            sender=sender,
            package=package,
        )
        _logger.debug("GOOOD! Sent shipment to Correos")
        return shipment

    def _create_receiver(self, crm_lead):
        partner = crm_lead.partner_id
        # TODO: What happens if exists more than one delivery address??
        mobile_isp_info = crm_lead.mobile_lead_line_ids[0].mobile_isp_info

        _logger.debug("Creating the receiver")
        if partner.is_company:
            receiver = Receiver(
                name=partner.name,
                nif=partner.vat,
                address=mobile_isp_info.delivery_street,
                city=mobile_isp_info.delivery_city,
                state=mobile_isp_info.delivery_state_id.name,
                zip=mobile_isp_info.delivery_zip_code,
                phone=partner.phone,
                email=partner.email,
                lang=lang_to_ISO_639_1(partner.lang),
                sms_phone=self._get_valid_mobile(partner),
            )
        else:
            receiver = Receiver(
                name=partner.firstname,
                surname=partner.lastname,
                address=mobile_isp_info.delivery_street,
                city=mobile_isp_info.delivery_city,
                state=mobile_isp_info.delivery_state_id.name,
                zip=mobile_isp_info.delivery_zip_code,
                phone=partner.phone,
                email=partner.email,
                lang=lang_to_ISO_639_1(partner.lang),
                sms_phone=self._get_valid_mobile(partner),
            )

        return receiver

    def _get_valid_mobile(self, partner):
        pattern = re.compile(r"^(6|7)?[0-9]{8}$")
        if partner.phone and pattern.match(partner.phone):
            return partner.phone
        elif partner.mobile and pattern.match(partner.mobile):
            return partner.mobile
