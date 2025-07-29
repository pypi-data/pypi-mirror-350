import abc
from rettxmutation.models.gene_models import CoreGeneMutation

class IStandardMutationService(abc.ABC):
    """
    Standard Mutation Service interface.
    
    This interface defines a contract for converting an input HGVS mutation string
    into a standardized CoreGeneMutation object. It abstracts away any API-specific details.
    
    Implementations could use Mutalyzer or any alternative API, but the caller will only
    see this uniform interface.
    """
    
    @abc.abstractmethod
    def get_core_mutation(self, input_hgvs: str) -> CoreGeneMutation:
        """
        Convert an input mutation (e.g., "NM_001110792.2:c.952C>T") into a CoreGeneMutation.
        
        Parameters:
            input_hgvs (str): The input mutation in HGVS format.
            
        Returns:
            CoreGeneMutation: The standardized mutation domain model.
        """
        pass
