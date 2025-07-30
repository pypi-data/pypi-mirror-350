from otrs_somconnexio.services.set_SIM_recieved_mobile_ticket import (
    SetSIMRecievedMobileTicket,
)
from otrs_somconnexio.services.set_SIM_returned_mobile_ticket import (
    SetSIMReturnedMobileTicket,
)
from otrs_somconnexio.exceptions import TicketNotReadyToBeUpdatedWithSIMReceivedData

from ..services.mobile_activation_date_service import (
    MobileActivationDateService,
)
from odoo.addons.component.core import Component

# 5 mins in seconds to delay the jobs
ETA = 300


class CrmLeadListener(Component):
    _inherit = "crm.lead.listener"

    def on_record_write(self, record, fields=None):
        if record.stage_id.id == self.env.ref("crm.stage_lead4").id:  # Stage Won
            for line in record.lead_line_ids:
                line.with_delay().create_ticket()
            if record.has_mobile_lead_lines and record.has_broadband_lead_lines:
                record.with_delay(eta=ETA).link_pack_tickets()
            if record.mobile_lead_line_ids.filtered(
                lambda l: (l.product_id.has_sharing_data_bond)
            ):
                record.with_delay(eta=ETA + 100).link_mobile_tickets_in_pack()

        if "sim_delivery_in_course" in fields and not record.sim_delivery_in_course:
            if not record.correos_tracking_code:
                for line in record.lead_line_ids:
                    if not line.is_mobile or line.mobile_isp_info_has_sim:
                        continue
                    SetSIMReturnedMobileTicket(line.ticket_number).run()
            else:
                for line in record.lead_line_ids:
                    if not line.is_mobile or line.mobile_isp_info_has_sim:
                        continue
                    date_service = MobileActivationDateService(
                        self.env,
                        line.is_portability(),
                    )
                    try:
                        SetSIMRecievedMobileTicket(
                            line.ticket_number,
                            date_service.get_activation_date(),
                            date_service.get_introduced_date(),
                        ).run()
                    except TicketNotReadyToBeUpdatedWithSIMReceivedData:
                        pass
