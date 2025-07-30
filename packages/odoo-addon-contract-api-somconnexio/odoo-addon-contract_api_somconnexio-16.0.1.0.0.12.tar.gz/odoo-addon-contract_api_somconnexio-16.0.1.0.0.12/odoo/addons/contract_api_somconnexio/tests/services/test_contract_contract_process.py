from mock import patch

from odoo.addons.somconnexio.tests.sc_test_case import SCTestCase


class TestContractProcess(SCTestCase):
    def setUp(self):
        super().setUp()
        self.ContractContractProcess = self.env["contract.contract.process"]

    @patch(
        "odoo.addons.contract_api_somconnexio.services.contract_process.mobile.MobileContractProcess.create"  # noqa
    )
    def test_create_mobile_contract(self, mock_mobile_contract_process_create):
        expected_contract = object
        mock_mobile_contract_process_create.return_value = expected_contract
        data = {
            "service_technology": "Mobile",
        }
        contract = self.ContractContractProcess.create(**data)

        self.assertEqual(contract, expected_contract)
        mock_mobile_contract_process_create.assert_called_once_with(**data)

    @patch(
        "odoo.addons.contract_api_somconnexio.services.contract_process.adsl.ADSLContractProcess.create"  # noqa
    )
    def test_create_adsl_contract(self, mock_adsl_contract_process_create):
        expected_contract = object
        mock_adsl_contract_process_create.return_value = expected_contract
        data = {
            "service_technology": "ADSL",
        }
        contract = self.ContractContractProcess.create(**data)

        self.assertEqual(contract, expected_contract)
        mock_adsl_contract_process_create.assert_called_once_with(**data)

    @patch(
        "odoo.addons.contract_api_somconnexio.services.contract_process.fiber.FiberContractProcess.create"  # noqa
    )
    def test_create_fiber_contract(self, mock_fiber_contract_process_create):
        expected_contract = object
        mock_fiber_contract_process_create.return_value = expected_contract
        data = {
            "service_technology": "Fiber",
        }
        contract = self.ContractContractProcess.create(**data)

        self.assertEqual(contract, expected_contract)
        mock_fiber_contract_process_create.assert_called_once_with(**data)

    @patch(
        "odoo.addons.contract_api_somconnexio.services.contract_process.router4g.Router4GContractProcess.create"  # noqa
    )
    def test_create_router4g_contract(self, mock_router4g_contract_process_create):
        expected_contract = object
        mock_router4g_contract_process_create.return_value = expected_contract
        data = {
            "service_technology": "4G",
        }
        contract = self.ContractContractProcess.create(**data)

        self.assertEqual(contract, expected_contract)
        mock_router4g_contract_process_create.assert_called_once_with(**data)

    @patch(
        "odoo.addons.contract_api_somconnexio.services.contract_process.switchboard.SBContractProcess.create"  # noqa
    )
    def test_create_switchboard_contract(self, mock_sb_contract_process_create):
        expected_contract = object
        mock_sb_contract_process_create.return_value = expected_contract
        data = {
            "service_technology": "Switchboard",
        }
        contract = self.ContractContractProcess.create(**data)

        self.assertEqual(contract, expected_contract)
        mock_sb_contract_process_create.assert_called_once_with(**data)
