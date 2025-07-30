import unittest

from unittest.mock import MagicMock

from sator_core.models.patch import PatchLocator
from sator_app.services.processing.patch import PatchProcessingService


class TestPatchProcessingService(unittest.TestCase):
    def setUp(self):
        # Create mock dependencies
        self.mock_annotation = MagicMock()
        self.mock_extraction = MagicMock()
        self.mock_analysis = MagicMock()
        self.mock_references = MagicMock()

        # Initialize service with mocked dependencies
        self.service = PatchProcessingService(
            patch_annotation=self.mock_annotation,
            patch_extraction=self.mock_extraction,
            patch_analysis=self.mock_analysis,
            patch_references=self.mock_references
        )

    def test_process_patch_returns_locator_when_attributes_exist(self):
        """Test full successful workflow with attributes found"""
        # Setup test data
        test_vulnerability_id = "CVE-2023-12345"
        test_product_id = "vendor/product"
        test_references = MagicMock()
        test_attributes = MagicMock()
        test_annotation = MagicMock()
        test_locator = MagicMock(spec=PatchLocator)

        # Configure mocks
        self.mock_references.search_patch_references.return_value = test_references
        self.mock_extraction.extract_patch_attributes.return_value = test_attributes
        self.mock_annotation.annotate_patch_attributes.return_value = test_annotation
        self.mock_analysis.analyze_patch_attributes.return_value = test_locator

        # Execute
        result = self.service.process_patch(test_vulnerability_id, test_product_id)

        # Verify calls
        self.mock_references.search_patch_references.assert_called_once_with(
            vulnerability_id=test_vulnerability_id, product_id=test_product_id
        )
        self.mock_extraction.extract_patch_attributes.assert_called_once_with(
            vulnerability_id=test_vulnerability_id
        )
        self.mock_annotation.annotate_patch_attributes.assert_called_once_with(
            vulnerability_id=test_vulnerability_id
        )
        self.mock_analysis.analyze_patch_attributes.assert_called_once_with(
            vulnerability_id=test_vulnerability_id
        )

        # Verify result
        self.assertEqual(result, test_locator)

    def test_process_patch_returns_none_when_no_attributes(self):
        """Test early exit when no attributes found"""
        # Setup test data
        test_vulnerability_id = "CVE-2023-12345"
        test_product_id = "vendor/product"
        test_references = MagicMock()

        # Configure mocks
        self.mock_references.search_patch_references.return_value = test_references
        self.mock_extraction.extract_patch_attributes.return_value = None

        # Execute
        result = self.service.process_patch(test_vulnerability_id, test_product_id)

        # Verify calls
        self.mock_references.search_patch_references.assert_called_once_with(
            vulnerability_id=test_vulnerability_id, product_id=test_product_id
        )
        self.mock_extraction.extract_patch_attributes.assert_called_once_with(
            vulnerability_id=test_vulnerability_id
        )
        self.mock_annotation.annotate_patch_attributes.assert_not_called()
        self.mock_analysis.analyze_patch_attributes.assert_not_called()

        # Verify result
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
