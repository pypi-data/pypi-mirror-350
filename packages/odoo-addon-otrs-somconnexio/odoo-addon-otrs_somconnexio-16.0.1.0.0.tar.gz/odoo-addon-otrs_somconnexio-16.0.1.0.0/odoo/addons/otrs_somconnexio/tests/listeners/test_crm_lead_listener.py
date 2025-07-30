from mock import patch, ANY

from odoo.addons.somconnexio.tests.helper_service import crm_lead_create
from odoo.addons.somconnexio.tests.sc_test_case import SCComponentTestCase

from otrs_somconnexio.exceptions import TicketNotReadyToBeUpdatedWithSIMReceivedData


class TestCRMLeadListener(SCComponentTestCase):
    @classmethod
    def setUpClass(cls):
        super(TestCRMLeadListener, cls).setUpClass()
        # disable tracking test suite wise
        cls.env = cls.env(
            context=dict(
                cls.env.context,
                tracking_disable=True,
                test_queue_job_no_delay=False,
            )
        )

    def setUp(self, *args, **kwargs):
        super().setUp(*args, **kwargs)
        self.partner_id = self.browse_ref("somconnexio.res_partner_2_demo")

        self.mobile_crm_lead = crm_lead_create(
            self.env, self.partner_id, "mobile", portability=True
        )
        self.mobile_crm_lead.correos_tracking_code = "tracking-code"
        self.mobile_crm_lead.action_set_remesa()

    @patch(
        "odoo.addons.otrs_somconnexio.listeners.crm_lead_listener.MobileActivationDateService"  # noqa
    )
    @patch(
        "odoo.addons.otrs_somconnexio.listeners.crm_lead_listener.SetSIMRecievedMobileTicket"  # noqa
    )
    def test_set_SIM_revieved_mobile_ticket(
        self, MockSetSIMRecievedMobileTicket, MockMobileActivationDateService
    ):
        self.mobile_crm_lead.sim_delivery_in_course = True

        self.mobile_crm_lead.sim_delivery_in_course = False

        MockMobileActivationDateService.assert_called_once_with(ANY, True)
        MockMobileActivationDateService.return_value.get_activation_date.assert_called_once_with()  # noqa
        MockMobileActivationDateService.return_value.get_introduced_date.assert_called_once_with()  # noqa
        MockSetSIMRecievedMobileTicket.assert_called_once_with(
            self.mobile_crm_lead.lead_line_ids[0].ticket_number, ANY, ANY
        )
        MockSetSIMRecievedMobileTicket.return_value.run.assert_called_once_with()

    @patch(
        "odoo.addons.otrs_somconnexio.listeners.crm_lead_listener.MobileActivationDateService"  # noqa
    )
    @patch(
        "odoo.addons.otrs_somconnexio.listeners.crm_lead_listener.SetSIMRecievedMobileTicket"  # noqa
    )
    def test_set_SIM_revieved_mobile_ticket_raise_error_pass(
        self, MockSetSIMRecievedMobileTicket, _
    ):
        self.mobile_crm_lead.sim_delivery_in_course = True

        MockSetSIMRecievedMobileTicket.return_value.run.side_effect = (
            TicketNotReadyToBeUpdatedWithSIMReceivedData("1234")
        )

        self.mobile_crm_lead.sim_delivery_in_course = False

        MockSetSIMRecievedMobileTicket.assert_called_once_with(
            self.mobile_crm_lead.lead_line_ids[0].ticket_number, ANY, ANY
        )
        MockSetSIMRecievedMobileTicket.return_value.run.assert_called()

    @patch(
        "odoo.addons.otrs_somconnexio.listeners.crm_lead_listener.SetSIMReturnedMobileTicket"  # noqa
    )
    def test_set_SIM_returned_mobile_ticket(self, MockSetSIMReturnedMobileTicket):
        self.mobile_crm_lead.sim_delivery_in_course = True
        self.mobile_crm_lead.correos_tracking_code = "828282828"

        self.mobile_crm_lead.correos_tracking_code = False
        self.mobile_crm_lead.sim_delivery_in_course = False

        MockSetSIMReturnedMobileTicket.assert_called_once_with(
            self.mobile_crm_lead.lead_line_ids[0].ticket_number
        )
        MockSetSIMReturnedMobileTicket.return_value.run.assert_called_once_with()

    def test_create_ticket(self):
        queue_jobs_before = self.env["queue.job"].search_count([])

        self.mobile_crm_lead.action_set_won()

        queue_jobs_after = self.env["queue.job"].search_count([])

        self.assertEqual(queue_jobs_before, queue_jobs_after - 1)

        jobs_domain = [
            ("method_name", "=", "create_ticket"),
            ("model_name", "=", "crm.lead.line"),
        ]
        queued_job = self.env["queue.job"].search(jobs_domain)

        self.assertTrue(queued_job)

    def test_link_pack_tickets(self):
        queue_jobs_before = self.env["queue.job"].search_count([])

        self.mobile_crm_lead.lead_line_ids.is_from_pack = True
        self.mobile_crm_lead.action_set_won()

        queue_jobs_after = self.env["queue.job"].search_count([])

        self.assertEqual(queue_jobs_before, queue_jobs_after - 1)

        queue_jobs_before = queue_jobs_after

        crm_lead_to_link = crm_lead_create(
            self.env,
            self.partner_id,
            "pack",
        )
        crm_lead_to_link.action_set_remesa()
        crm_lead_to_link.action_set_won()

        queue_jobs_after = self.env["queue.job"].search_count([])
        jobs_domain = [
            ("method_name", "=", "link_pack_tickets"),
            ("model_name", "=", "crm.lead"),
        ]
        queued_job = self.env["queue.job"].search(jobs_domain)

        self.assertEqual(queue_jobs_before, queue_jobs_after - 3)
        self.assertTrue(queued_job)

    def test_link_mobile_tickets_in_pack(self):
        queue_jobs_before = self.env["queue.job"].search_count([])

        self.mobile_crm_lead.lead_line_ids.product_id = self.env.ref(
            "somconnexio.50GBCompartides2mobils"
        )
        self.mobile_crm_lead.action_set_won()

        queue_jobs_after = self.env["queue.job"].search_count([])

        jobs_domain = [
            ("method_name", "=", "link_mobile_tickets_in_pack"),
            ("model_name", "=", "crm.lead"),
        ]
        queued_job = self.env["queue.job"].search(jobs_domain)

        self.assertEqual(queue_jobs_before, queue_jobs_after - 2)
        self.assertTrue(queued_job)
