from sator_core.models.product import ProductLocator

from sator_core.use_cases.resolution.references.product import ProductReferencesResolution
from sator_core.use_cases.annotation.attributes.product import ProductAttributesAnnotation
from sator_core.use_cases.extraction.attributes.product import ProductAttributesExtraction
from sator_core.use_cases.analysis.attributes.product import ProductAttributesAnalysis


class ProductProcessingService:
    def __init__(
            self, product_annotation: ProductAttributesAnnotation,
            product_extraction: ProductAttributesExtraction,
            product_analysis: ProductAttributesAnalysis,
            product_references: ProductReferencesResolution
    ):
        self.product_references = product_references
        self.product_annotation = product_annotation
        self.product_extraction = product_extraction
        self.product_analysis = product_analysis

    # TODO: should return something that assembles all the information
    def process_product(self, vendor: str, name: str) -> ProductLocator | None:
        references = self.product_references.search_product_references(vendor=vendor, name=name)
        print(references)
        attributes = self.product_extraction.extract_product_attributes(vendor=vendor, name=name)
        print(attributes)

        if attributes:
            annotation = self.product_annotation.annotate_product_attributes(product_id=attributes.product_id)
            print(annotation)
            locator = self.product_analysis.analyze_product_attributes(product_id=attributes.product_id)
            print(locator)
            return locator

        return None
