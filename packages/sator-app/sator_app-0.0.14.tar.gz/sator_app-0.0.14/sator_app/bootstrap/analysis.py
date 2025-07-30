from typing import List
from sator_app.bootstrap.base import BaseBuilder

from sator_core.ports.driven.classifiers.diff import DiffClassifierPort
from sator_core.ports.driven.repositories.product import ProductRepositoryPort
from sator_core.ports.driven.analyzers.patch import PatchAttributesAnalyzerPort


from sator_core.use_cases.analysis.attributes import (
    PatchAttributesAnalysis, ProductAttributesAnalysis, VulnerabilityAttributesAnalysis
)


class AnalysisBuilder(BaseBuilder):
    def __init__(
            self, prod_repos: List[ProductRepositoryPort], diff_classifier: DiffClassifierPort,
            patch_attrs_analyzer: PatchAttributesAnalyzerPort, **kwargs
    ):
        super().__init__(**kwargs)
        self.product_repositories = prod_repos
        self.patch_attributes_analyzer = patch_attrs_analyzer
        self.diff_classifier = diff_classifier

    def create_patch_attributes_analysis(self) -> PatchAttributesAnalysis:
        return PatchAttributesAnalysis(
            patch_analyzer=self.patch_attributes_analyzer,
            storage_port=self.storage_port
        )

    def create_product_attributes_analysis(self) -> ProductAttributesAnalysis:
        return ProductAttributesAnalysis(
            oss_gateways=self.oss_gateways,
            storage_port=self.storage_port
        )

    def create_vulnerability_attributes_analysis(self) -> VulnerabilityAttributesAnalysis:
        return VulnerabilityAttributesAnalysis(
            prod_repos=self.product_repositories,
            storage_port=self.storage_port
        )
