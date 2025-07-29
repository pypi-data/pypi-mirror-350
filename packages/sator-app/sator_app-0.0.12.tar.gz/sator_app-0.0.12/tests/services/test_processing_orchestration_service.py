import unittest
from unittest.mock import MagicMock

from sator_app.services.orchestration import ProcessingOrchestrationService
from sator_app.services.processing import (
    PatchProcessingService, ProductProcessingService, VulnerabilityProcessingService
)


class TestProcessingOrchestrationService(unittest.TestCase):
    def setUp(self):
        # Create mock dependencies
        self.mock_vulnerability_processing = MagicMock(spec=VulnerabilityProcessingService)
        self.mock_product_processing = MagicMock(spec=ProductProcessingService)
        self.mock_patch_processing = MagicMock(spec=PatchProcessingService)

        # Initialize service with mocked dependencies
        self.service = ProcessingOrchestrationService(
            vulnerability_processing=self.mock_vulnerability_processing,
            product_processing=self.mock_product_processing,
            patch_processing=self.mock_patch_processing
        )

    def test_orchestrate_analysis_successful(self):
        """Test successful orchestration where all steps succeed"""
        # Setup test data
        test_vulnerability_id = "CVE-2023-12345"

        # Create mock locators
        mock_vulnerability_locator = MagicMock()
        mock_vulnerability_locator.product.vendor = "TestVendor"
        mock_vulnerability_locator.product.name = "TestProduct"

        mock_product_locator = MagicMock()
        mock_product_locator.product_id = "TestVendor/TestProduct"

        mock_patch_locator = MagicMock()

        # Configure mocks
        self.mock_vulnerability_processing.process_vulnerability.return_value = mock_vulnerability_locator
        self.mock_product_processing.process_product.return_value = mock_product_locator
        self.mock_patch_processing.process_patch.return_value = mock_patch_locator

        # Execute
        result = self.service.orchestrate_analysis(test_vulnerability_id)

        # Verify calls
        self.mock_vulnerability_processing.process_vulnerability.assert_called_once_with(test_vulnerability_id)
        self.mock_product_processing.process_product.assert_called_once_with(
            vendor=mock_vulnerability_locator.product.vendor,
            name=mock_vulnerability_locator.product.name
        )
        self.mock_patch_processing.process_patch.assert_called_once_with(
            test_vulnerability_id, mock_product_locator.product_id
        )

        # Verify result
        self.assertEqual(result["vulnerability_id"], test_vulnerability_id)
        self.assertEqual(result["vulnerability"], mock_vulnerability_locator)
        self.assertEqual(result["product"], mock_product_locator)
        self.assertEqual(result["patch"], mock_patch_locator)

    def test_orchestrate_analysis_vulnerability_processing_fails(self):
        """Test orchestration when vulnerability processing fails"""
        # Setup test data
        test_vulnerability_id = "CVE-2023-12345"

        # Configure mocks
        self.mock_vulnerability_processing.process_vulnerability.return_value = None

        # Execute
        result = self.service.orchestrate_analysis(test_vulnerability_id)

        # Verify calls
        self.mock_vulnerability_processing.process_vulnerability.assert_called_once_with(test_vulnerability_id)
        self.mock_product_processing.process_product.assert_not_called()
        self.mock_patch_processing.process_patch.assert_not_called()

        # Verify result
        self.assertEqual(result["vulnerability_id"], test_vulnerability_id)
        self.assertIsNone(result["vulnerability"])
        self.assertIsNone(result["product"])
        self.assertIsNone(result["patch"])

    def test_orchestrate_analysis_product_processing_fails(self):
        """Test orchestration when product processing fails"""
        # Setup test data
        test_vulnerability_id = "CVE-2023-12345"

        # Create mock locators
        mock_vulnerability_locator = MagicMock()
        mock_vulnerability_locator.product.vendor = "TestVendor"
        mock_vulnerability_locator.product.name = "TestProduct"

        # Configure mocks
        self.mock_vulnerability_processing.process_vulnerability.return_value = mock_vulnerability_locator
        self.mock_product_processing.process_product.return_value = None

        # Execute
        result = self.service.orchestrate_analysis(test_vulnerability_id)

        # Verify calls
        self.mock_vulnerability_processing.process_vulnerability.assert_called_once_with(test_vulnerability_id)
        self.mock_product_processing.process_product.assert_called_once_with(
            vendor=mock_vulnerability_locator.product.vendor,
            name=mock_vulnerability_locator.product.name
        )
        self.mock_patch_processing.process_patch.assert_not_called()

        # Verify result
        self.assertEqual(result["vulnerability_id"], test_vulnerability_id)
        self.assertEqual(result["vulnerability"], mock_vulnerability_locator)
        self.assertIsNone(result["product"])
        self.assertIsNone(result["patch"])

    def test_orchestrate_analysis_patch_processing_fails(self):
        """Test orchestration when patch processing fails"""
        # Setup test data
        test_vulnerability_id = "CVE-2023-12345"

        # Create mock locators
        mock_vulnerability_locator = MagicMock()
        mock_vulnerability_locator.product.vendor = "TestVendor"
        mock_vulnerability_locator.product.name = "TestProduct"

        mock_product_locator = MagicMock()
        mock_product_locator.product_id = "TestVendor/TestProduct"

        # Configure mocks
        self.mock_vulnerability_processing.process_vulnerability.return_value = mock_vulnerability_locator
        self.mock_product_processing.process_product.return_value = mock_product_locator
        self.mock_patch_processing.process_patch.return_value = None

        # Execute
        result = self.service.orchestrate_analysis(test_vulnerability_id)

        # Verify calls
        self.mock_vulnerability_processing.process_vulnerability.assert_called_once_with(test_vulnerability_id)
        self.mock_product_processing.process_product.assert_called_once_with(
            vendor=mock_vulnerability_locator.product.vendor,
            name=mock_vulnerability_locator.product.name
        )
        self.mock_patch_processing.process_patch.assert_called_once_with(
            test_vulnerability_id, mock_product_locator.product_id
        )

        # Verify result
        self.assertEqual(result["vulnerability_id"], test_vulnerability_id)
        self.assertEqual(result["vulnerability"], mock_vulnerability_locator)
        self.assertEqual(result["product"], mock_product_locator)
        self.assertIsNone(result["patch"])


if __name__ == "__main__":
    unittest.main()
