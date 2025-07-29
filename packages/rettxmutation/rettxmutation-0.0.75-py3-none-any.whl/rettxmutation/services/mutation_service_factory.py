from rettxmutation.services.mutation_service_interface import IStandardMutationService
from rettxmutation.services.mutalyzer_mutation_service import MutalyzerStandardMutationService
#from services.alternative_mutation_service import AlternativeMutationService

def create_mutation_service(provider: str = "mutalyzer", **kwargs) -> IStandardMutationService:
    """
    Factory method to create a mutation service based on the provider.

    Parameters:
        provider (str): Identifier for the mutation service provider (e.g., "mutalyzer", "alternative").
        kwargs: Additional parameters to pass to the service constructor.

    Returns:
        An instance of IMutationService.
    """
    provider = provider.lower()
    if provider == "mutalyzer":
        return MutalyzerStandardMutationService(**kwargs)
    elif provider == "alternative":
        raise ValueError(f"Not implemented: {provider}")
    else:
        raise ValueError(f"Unknown mutation service provider: {provider}")
