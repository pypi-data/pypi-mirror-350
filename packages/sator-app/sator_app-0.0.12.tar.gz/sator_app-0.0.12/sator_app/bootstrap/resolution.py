from typing import List

from sator_app.bootstrap.base import BaseBuilder

from sator_core.ports.driven.repositories.oss import OSSRepositoryPort
from sator_core.ports.driven.repositories.product import ProductRepositoryPort
from sator_core.ports.driven.repositories.vulnerability import VulnerabilityRepositoryPort

from sator_core.use_cases.resolution.metadata import VulnerabilityMetadataResolution, ProductMetadataResolution
from sator_core.use_cases.resolution.references import (
    ProductReferencesResolution, VulnerabilityReferencesResolution, PatchReferencesResolution
)


class ResolutionBuilder(BaseBuilder):
    def __init__(
            self, vuln_repos: List[VulnerabilityRepositoryPort], prod_repos: List[ProductRepositoryPort],
            oss_repos: List[OSSRepositoryPort], **kwargs
    ):
        super().__init__(**kwargs)
        self.vulnerability_repositories = vuln_repos
        self.product_repositories = prod_repos
        self.oss_repositories = oss_repos

    def create_vulnerability_metadata_resolution(self) -> VulnerabilityMetadataResolution:
        return VulnerabilityMetadataResolution(
            vuln_repositories=self.vulnerability_repositories,
            storage_port=self.storage_port
        )

    def create_vulnerability_references_resolution(self) -> VulnerabilityReferencesResolution:
        return VulnerabilityReferencesResolution(
            vulnerability_repositories=self.vulnerability_repositories,
            storage_port=self.storage_port
        )

    def create_product_metadata_resolution(self) -> ProductMetadataResolution:
        return ProductMetadataResolution(
            product_repositories=self.product_repositories,
            storage_port=self.storage_port
        )

    def create_product_references_resolution(self) -> ProductReferencesResolution:
        return ProductReferencesResolution(
            product_repositories=self.product_repositories,
            storage_port=self.storage_port
        )

    def create_patch_references_resolution(self) -> PatchReferencesResolution:
        return PatchReferencesResolution(
            oss_repositories=self.oss_repositories,  # Empty list as default
            oss_gateways=self.oss_gateways,  # Already a list from BaseBuilder
            storage_port=self.storage_port
        )
