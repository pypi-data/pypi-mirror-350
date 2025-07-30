from sator_core.models.patch import PatchLocator

from sator_core.use_cases.resolution.references import PatchReferencesResolution
from sator_core.use_cases.annotation.attributes import PatchAttributesAnnotation
from sator_core.use_cases.extraction.attributes import PatchAttributesExtraction
from sator_core.use_cases.analysis.attributes import PatchAttributesAnalysis


class PatchProcessingService:
    def __init__(
            self, patch_annotation: PatchAttributesAnnotation,
            patch_extraction: PatchAttributesExtraction,
            patch_analysis: PatchAttributesAnalysis,
            patch_references: PatchReferencesResolution
    ):
        self.patch_references = patch_references
        self.patch_annotation = patch_annotation
        self.patch_extraction = patch_extraction
        self.patch_analysis = patch_analysis

    # TODO: should return something that assembles all the information
    def process_patch(self, vulnerability_id: str, product_id: str) -> PatchLocator | None:
        references = self.patch_references.search_patch_references(
            vulnerability_id=vulnerability_id, product_id=product_id
        )
        print(references)
        attributes = self.patch_extraction.extract_patch_attributes(vulnerability_id=vulnerability_id)
        print(attributes)

        if attributes:
            annotation = self.patch_annotation.annotate_patch_attributes(vulnerability_id=vulnerability_id)
            print(annotation)
            locator = self.patch_analysis.analyze_patch_attributes(vulnerability_id=vulnerability_id)
            print(locator)
            return locator

        return None