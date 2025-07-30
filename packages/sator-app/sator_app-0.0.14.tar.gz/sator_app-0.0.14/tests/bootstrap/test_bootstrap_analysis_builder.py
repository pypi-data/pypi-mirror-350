from unittest.mock import MagicMock

from sator_app.bootstrap.analysis import AnalysisBuilder
from sator_core.use_cases.analysis.attributes import (
    PatchAttributesAnalysis,
    ProductAttributesAnalysis,
    VulnerabilityAttributesAnalysis,
)


def test_analysis_builder_creates_patch_attributes_analysis():
    # Arrange
    mock_storage = MagicMock()
    mock_patch_analyzer = MagicMock()
    mock_product_repos = [MagicMock()]
    mock_diff_classifier = MagicMock()
    mock_oss_gateways = [MagicMock()]

    builder = AnalysisBuilder(
        prod_repos=mock_product_repos,
        diff_classifier=mock_diff_classifier,
        patch_attrs_analyzer=mock_patch_analyzer,
        storage_port=mock_storage,  # this and oss_gateway likely set in BaseBuilder
        oss_gateways=mock_oss_gateways
    )

    # Act
    patch_analysis = builder.create_patch_attributes_analysis()
    product_analysis = builder.create_product_attributes_analysis()
    vulnerability_analysis = builder.create_vulnerability_attributes_analysis()

    # Assert
    assert isinstance(patch_analysis, PatchAttributesAnalysis)
    assert patch_analysis.storage_port is mock_storage
    assert patch_analysis.patch_analyzer is mock_patch_analyzer
    assert isinstance(product_analysis, ProductAttributesAnalysis)
    assert product_analysis.oss_gateways == mock_oss_gateways
    assert product_analysis.storage_port is mock_storage
    assert isinstance(vulnerability_analysis, VulnerabilityAttributesAnalysis)
    assert vulnerability_analysis.product_repositories == mock_product_repos
    assert vulnerability_analysis.storage_port is mock_storage
