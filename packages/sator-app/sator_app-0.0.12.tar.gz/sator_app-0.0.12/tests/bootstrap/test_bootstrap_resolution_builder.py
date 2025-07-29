import unittest

from unittest.mock import MagicMock

from sator_app.bootstrap.resolution import ResolutionBuilder

from sator_core.ports.driven.gateways.oss import OSSGatewayPort
from sator_core.ports.driven.repositories.oss import OSSRepositoryPort
from sator_core.ports.driven.persistence.storage import StoragePersistencePort
from sator_core.ports.driven.repositories.product import ProductRepositoryPort
from sator_core.ports.driven.repositories.vulnerability import VulnerabilityRepositoryPort

from sator_core.use_cases.resolution.metadata import VulnerabilityMetadataResolution, ProductMetadataResolution
from sator_core.use_cases.resolution.references import (
    ProductReferencesResolution, VulnerabilityReferencesResolution, PatchReferencesResolution
)


class TestResolutionBuilder(unittest.TestCase):
    def setUp(self):
        # Mock dependencies
        self.mock_oss_gateway = MagicMock(spec=OSSGatewayPort)
        self.mock_storage = MagicMock(spec=StoragePersistencePort)
        self.mock_vuln_repos = [MagicMock(spec=VulnerabilityRepositoryPort)]
        self.mock_prod_repos = [MagicMock(spec=ProductRepositoryPort)]
        self.mock_oss_repos = [MagicMock(spec=OSSRepositoryPort)]  # Mock of OSSRepositoryPort

        # Initialize builder with mocked dependencies
        self.builder = ResolutionBuilder(
            vuln_repos=self.mock_vuln_repos,
            prod_repos=self.mock_prod_repos,
            oss_repos=self.mock_oss_repos,
            storage_port=self.mock_storage,
            oss_gateways=[self.mock_oss_gateway]
        )

    def test_create_vulnerability_metadata_resolution(self):
        """Test creation of VulnerabilityMetadataResolution instance"""
        resolution = self.builder.create_vulnerability_metadata_resolution()

        self.assertIsInstance(resolution, VulnerabilityMetadataResolution)
        self.assertEqual(resolution.vuln_repositories, self.mock_vuln_repos)
        self.assertEqual(resolution.storage_port, self.mock_storage)

    def test_create_vulnerability_references_resolution(self):
        """Test creation of VulnerabilityReferencesResolution instance"""
        resolution = self.builder.create_vulnerability_references_resolution()

        self.assertIsInstance(resolution, VulnerabilityReferencesResolution)
        self.assertEqual(resolution.vulnerability_repositories, self.mock_vuln_repos)
        self.assertEqual(resolution.storage_port, self.mock_storage)

    def test_create_product_metadata_resolution(self):
        """Test creation of ProductMetadataResolution instance"""
        resolution = self.builder.create_product_metadata_resolution()

        self.assertIsInstance(resolution, ProductMetadataResolution)
        self.assertEqual(resolution.product_repositories, self.mock_prod_repos)
        self.assertEqual(resolution.storage_port, self.mock_storage)

    def test_create_product_references_resolution(self):
        """Test creation of ProductReferencesResolution instance"""
        resolution = self.builder.create_product_references_resolution()

        self.assertIsInstance(resolution, ProductReferencesResolution)
        self.assertEqual(resolution.product_repositories, self.mock_prod_repos)
        self.assertEqual(resolution.storage_port, self.mock_storage)

    def test_create_patch_references_resolution(self):
        """Test creation of PatchReferencesResolution instance"""
        resolution = self.builder.create_patch_references_resolution()

        self.assertIsInstance(resolution, PatchReferencesResolution)
        self.assertEqual(resolution.oss_repositories, self.mock_oss_repos)  # Check mock OSS repositories are passed
        self.assertEqual(resolution.oss_gateways, [self.mock_oss_gateway])  # Check mock OSS gateway is in the list
        self.assertEqual(resolution.storage_port, self.mock_storage)


if __name__ == "__main__":
    unittest.main()
