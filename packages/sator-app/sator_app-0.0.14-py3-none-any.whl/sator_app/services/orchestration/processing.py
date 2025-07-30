from typing import Dict, Any

from sator_app.services.processing import (
    PatchProcessingService, ProductProcessingService, VulnerabilityProcessingService
)


class ProcessingOrchestrationService:
    """
    Orchestration service that coordinates the entire analysis workflow across
    vulnerability, product, and patch processing services.
    """
    
    def __init__(
            self,
            vulnerability_processing: VulnerabilityProcessingService,
            product_processing: ProductProcessingService,
            patch_processing: PatchProcessingService
    ):
        """
        Initialize the orchestration service with the required processing services.
        
        Args:
            vulnerability_processing: Service for processing vulnerability data
            product_processing: Service for processing product data
            patch_processing: Service for processing patch data
        """
        self.vulnerability_processing = vulnerability_processing
        self.product_processing = product_processing
        self.patch_processing = patch_processing
    
    def orchestrate_analysis(self, vulnerability_id: str) -> Dict[str, Any]:
        """
        Orchestrate the complete analysis workflow for a given vulnerability.
        
        Args:
            vulnerability_id: The identifier of the vulnerability to analyze

        Returns:
            A dictionary containing the results of the analysis across all domains
        """
        results = {
            "vulnerability_id": vulnerability_id,
            "vulnerability": None,
            "product": None,
            "patch": None
        }

        # Step 1: Process vulnerability information
        vulnerability_locator = self.vulnerability_processing.process_vulnerability(vulnerability_id)
        results["vulnerability"] = vulnerability_locator

        # If we couldn't process the vulnerability, we can't continue with product and patch
        if not vulnerability_locator:
            return results

        # Step 2: Process product information if available from vulnerability
        product_locator = self.product_processing.process_product(
            vendor=vulnerability_locator.product.vendor, name=vulnerability_locator.product.name
        )

        results["product"] = product_locator

        if not product_locator:
            # If product processing fails, we can still return the vulnerability information
            return results

        # Step 3: Process patch information
        patch_locator = self.patch_processing.process_patch(vulnerability_id, product_locator.product_id)
        results["patch"] = patch_locator
        
        return results
