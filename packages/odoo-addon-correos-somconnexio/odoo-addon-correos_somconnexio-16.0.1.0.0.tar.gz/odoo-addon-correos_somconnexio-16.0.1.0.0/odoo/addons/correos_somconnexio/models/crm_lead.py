import os
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
    TrackingShipment,
    UndefinedCredentials,
)
from correos_seguimiento.errors import (
    UnknownApiResponse as UnknownApiResponseSeguimiento,
)
from socket import error as SocketError
from requests.exceptions import ConnectionError as RequestConnectionError
from requests.exceptions import Timeout as TimeOut

from odoo import _, models

from ..helpers.job_retry_utils import retry_on_error
from ..correos_services.shipment import DELIVERY_ARGS, CorreosShipment


class CrmLead(models.Model):
    _inherit = "crm.lead"

    @retry_on_error(
        retries=20,
        delay=300,
        errors=[InvalidEndpoint, RequestConnectionError, SocketError, TimeOut],
    )
    def track_delivery(self):
        try:
            delivery = TrackingShipment(
                os.environ["CORREOS_USER"],
                os.environ["CORREOS_PASSWORD"],
                self.correos_tracking_code,
            ).build()

            if delivery.is_returned():
                self.message_post(
                    _(
                        "Return Process\nThe tracking code {tracking_code} is no loger valid"  # noqa
                    ).format(tracking_code=self.correos_tracking_code)
                )
                self.correos_tracking_code = False
                self.sim_delivery_in_course = False

            elif delivery.is_delivered():
                self.sim_delivery_in_course = False
            else:
                if delivery.is_relabeled():
                    old_tracking_code = self.correos_tracking_code
                    self.correos_tracking_code = delivery.get_relabeled_shipment_code()

                    self.message_post(
                        _(
                            "The shipment code was relabeled from: {old} to {new}"
                        ).format(old=old_tracking_code, new=self.correos_tracking_code)
                    )

        except IndexError:
            raise IndexError(_("IndexError while retrieving relabeled shipment code"))
        except KeyError:
            raise KeyError(_("KeyError while retrieving relabeled shipment code"))
        except UndefinedCredentials:
            raise UndefinedCredentials(_("Credentials for Correos API are not defined"))
        except InvalidCredentials:
            raise InvalidCredentials(_("Credentials for Correos API are not valid"))
        except InvalidEndpoint:
            raise InvalidEndpoint(_("Endpoint is wrong or is down"))
        except RequestConnectionError:
            raise RequestConnectionError(_("Connection with Correos API failed"))
        except SocketError:
            raise SocketError(_("Connection with Correos API failed"))
        except UnknownApiResponseSeguimiento:
            raise UnknownApiResponseSeguimiento(
                _("The JSON shows a data format that can't be parsed")
            )
        except InvalidApiResponseSeguimiento:
            raise InvalidApiResponseSeguimiento(_("Returned data is not JSON valid"))

    def create_shipment(self, delivery_args=None):
        delivery_OK_stage_id = self.env.ref("delivery_somconnexio.stage_lead6").id
        delivery_KO_stage_id = self.env.ref("delivery_somconnexio.stage_lead7").id
        self.validate_leads_to_generate_SIM_delivery()
        try:
            self._create_shipment(delivery_args)
            self.write({"stage_id": delivery_OK_stage_id})
        except (MissingData, UnknownApiResponse, InvalidApiResponse) as e:
            self.write({"stage_id": delivery_KO_stage_id})
            if isinstance(e, MissingData):
                message = _(
                    "Error sending the delivery to Correos with the next field: {}"  # noqa
                ).format(e.field)
            else:
                message = _(
                    "Error sending the delivery to Correos. Contact with Sistemas team. Error: {}"  # noqa
                ).format(e.message)
            self.message_post(message)

    def _create_shipment(self, delivery_args):
        """Create a Correos shipment and save the PDF label and the
        shipment_code in the CRMLead."""
        shipment = CorreosShipment().create(self, delivery_args)
        self.write(
            {
                "correos_tracking_code": shipment.shipment_code,
                "sim_delivery_in_course": True,
            }
        )
        name = "shipment_{}".format(shipment.shipment_code)
        self.env["ir.attachment"].create(
            {
                "name": name,
                "type": "binary",
                "datas": shipment.label_file,
                "store_fname": name + ".pdf",
                "res_model": "crm.lead",
                "res_id": self.id,
                "mimetype": "application/x-pdf",
            }
        )

    def action_generate_express_delivery(self):
        for crm_lead in self:
            crm_lead.with_delay().create_shipment(DELIVERY_ARGS["express"])
