import unittest

from pydantic import AnyUrl
from unittest.mock import MagicMock

from sator_core.models.product import Product, ProductAttributes, ProductLocator, ProductReferences
from sator_app.services.processing.product import ProductProcessingService


test_product = Product(
    vendor="onlyoffice",
    name="document_server"
)

test_product_attributes = ProductAttributes(
    name="Document Server",
    product_id=test_product.id,
    keywords=["online office suite", "collaborative editing"],
    platforms=["Mac", "Windows", "Linux"]
)

test_product_references = ProductReferences(
    product_id=test_product.id,
    homepage=[AnyUrl("https://onlyoffice.com")],
    repositories=[AnyUrl("https://github.com/ONLYOFFICE/DocumentServer")]
)

test_product_locator = ProductLocator(
    product_id=test_product.id,
    platform="github",
    repository_path="ONLYOFFICE/DocumentServer"
)


class TestProductProcessingService(unittest.TestCase):
    def setUp(self):
        # Create mock dependencies
        self.mock_annotation = MagicMock()
        self.mock_extraction = MagicMock()
        self.mock_analysis = MagicMock()
        self.mock_references = MagicMock()

        # Initialize service with mocked dependencies
        self.service = ProductProcessingService(
            product_annotation=self.mock_annotation,
            product_extraction=self.mock_extraction,
            product_analysis=self.mock_analysis,
            product_references=self.mock_references
        )

    def test_process_product_returns_locator_when_attributes_exist(self):
        """Test full successful workflow with attributes found"""
        # Setup test data

        # Configure mocks
        self.mock_references.search_product_references.return_value = test_product_references
        self.mock_extraction.extract_product_attributes.return_value = test_product_attributes
        self.mock_analysis.analyze_product_attributes.return_value = test_product_locator

        # Execute
        result = self.service.process_product(test_product.vendor, test_product.name)

        # Verify calls
        self.mock_references.search_product_references.assert_called_once_with(
            vendor=test_product.vendor, name=test_product.name
        )
        self.mock_extraction.extract_product_attributes.assert_called_once_with(
            vendor=test_product.vendor, name=test_product.name
        )
        self.mock_annotation.annotate_product_attributes.assert_called_once_with(
            product_id=test_product.id
        )
        self.mock_analysis.analyze_product_attributes.assert_called_once_with(
            product_id=test_product.id
        )

        # Verify result
        self.assertEqual(result, test_product_locator)

    def test_process_product_returns_none_when_no_attributes(self):
        """Test early exit when no attributes found"""
        # Configure mocks
        self.mock_extraction.extract_product_attributes.return_value = None

        # Execute
        result = self.service.process_product("invalid", "product")

        # Verify calls
        self.mock_references.search_product_references.assert_called_once_with(
            vendor="invalid", name="product"
        )
        self.mock_extraction.extract_product_attributes.assert_called_once_with(
            vendor="invalid", name="product"
        )
        self.mock_annotation.annotate_product_attributes.assert_not_called()
        self.mock_analysis.analyze_product_attributes.assert_not_called()

        # Verify result
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
