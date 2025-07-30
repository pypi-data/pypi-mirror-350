import unittest

from unittest.mock import MagicMock

from sator_app.bootstrap.extraction import ExtractionBuilder

from sator_core.ports.driven.gateways.oss import OSSGatewayPort
from sator_core.ports.driven.persistence.storage import StoragePersistencePort
from sator_core.ports.driven.extraction.attributes.patch import PatchAttributesExtractorPort
from sator_core.ports.driven.extraction.attributes.product import ProductAttributesExtractorPort
from sator_core.ports.driven.extraction.attributes.vulnerability import VulnerabilityAttributesExtractorPort

from sator_core.use_cases.extraction.attributes import (
    ProductAttributesExtraction,
    VulnerabilityAttributesExtraction,
    PatchAttributesExtraction
)


class TestExtractionBuilder(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_oss_gateway = MagicMock(spec=OSSGatewayPort)
        self.mock_storage = MagicMock(spec=StoragePersistencePort)
        self.mock_patch_extractor = MagicMock(spec=PatchAttributesExtractorPort)
        self.mock_product_extractor = MagicMock(spec=ProductAttributesExtractorPort)
        self.mock_vuln_extractor = MagicMock(spec=VulnerabilityAttributesExtractorPort)

        # Initialize builder with mocked dependencies
        self.builder = ExtractionBuilder(
            patch_attrs_extractor=self.mock_patch_extractor,
            product_attrs_extractor=self.mock_product_extractor,
            vuln_attrs_extractor=self.mock_vuln_extractor,
            storage_port=self.mock_storage,
            oss_gateways=[self.mock_oss_gateway]
        )

    def test_create_product_attributes_extraction(self):
        """Test creation of ProductAttributesExtraction instance"""
        extraction = self.builder.create_product_attributes_extraction()

        self.assertIsInstance(extraction, ProductAttributesExtraction)
        self.assertEqual(extraction.extractor_port, self.mock_product_extractor)
        self.assertEqual(extraction.storage_port, self.mock_storage)

    def test_create_vulnerability_attributes_extraction(self):
        """Test creation of VulnerabilityAttributesExtraction instance"""
        extraction = self.builder.create_vulnerability_attributes_extraction()

        self.assertIsInstance(extraction, VulnerabilityAttributesExtraction)
        self.assertEqual(extraction.attributes_extractor, self.mock_vuln_extractor)
        self.assertEqual(extraction.storage_port, self.mock_storage)

    def test_create_patch_attributes_extraction(self):
        """Test creation of PatchAttributesExtraction instance with OSS gateway"""
        extraction = self.builder.create_patch_attributes_extraction()

        self.assertIsInstance(extraction, PatchAttributesExtraction)
        self.assertEqual(extraction.oss_gateways, [self.mock_oss_gateway])
        self.assertEqual(extraction.attributes_extractor, self.mock_patch_extractor)
        self.assertEqual(extraction.storage_port, self.mock_storage)


if __name__ == "__main__":
    unittest.main()
