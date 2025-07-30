from sator_app.bootstrap.base import BaseBuilder

from sator_core.ports.driven.extraction.attributes.patch import PatchAttributesExtractorPort
from sator_core.ports.driven.extraction.attributes.product import ProductAttributesExtractorPort
from sator_core.ports.driven.extraction.attributes.vulnerability import VulnerabilityAttributesExtractorPort


from sator_core.use_cases.extraction.attributes import (
    ProductAttributesExtraction, VulnerabilityAttributesExtraction, PatchAttributesExtraction
)


class ExtractionBuilder(BaseBuilder):
    def __init__(
            self, patch_attrs_extractor: PatchAttributesExtractorPort,
            product_attrs_extractor: ProductAttributesExtractorPort,
            vuln_attrs_extractor: VulnerabilityAttributesExtractorPort, **kwargs
    ):
        super().__init__(**kwargs)

        self.patch_attributes_extractor = patch_attrs_extractor
        self.product_attributes_extractor = product_attrs_extractor
        self.vulnerability_attributes_extractor = vuln_attrs_extractor

    def create_product_attributes_extraction(self) -> ProductAttributesExtraction:
        return ProductAttributesExtraction(
            extractor_port=self.product_attributes_extractor,
            storage_port=self.storage_port
        )

    def create_vulnerability_attributes_extraction(self) -> VulnerabilityAttributesExtraction:
        return VulnerabilityAttributesExtraction(
            attributes_extractor=self.vulnerability_attributes_extractor,
            storage_port=self.storage_port
        )

    def create_patch_attributes_extraction(self) -> PatchAttributesExtraction:
        return PatchAttributesExtraction(
            oss_gateways=self.oss_gateways,
            attributes_extractor=self.patch_attributes_extractor,
            storage_port=self.storage_port
        )
