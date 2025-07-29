import logging
from semantic_kernel.functions import kernel_function
from rettxmutation.models.gene_models import GeneMutation, RawMutation
from .mutation_service import MutationService


logger = logging.getLogger(__name__)


class MutationNormalizerPlugin:

    PLUGIN_NAME = "mutation_normalizer_plugin"


    @kernel_function(
        name="get_gene_mutations",
        description="Get a GeneMutation object from an input HGVS string."
    )
    def get_gene_mutations(self, input_mutations: list[RawMutation]) -> list[GeneMutation]:
        """
        Kernel function to get a GeneMutation objects from an input HGVS string.
        """
        # Initialize the MutationService with the primary and secondary transcripts.
        mutation_service = MutationService(
            primary_transcript="NM_004992.4",
            secondary_transcript="NM_001110792.2",
            target_assembly="GRCh38"
        )

        gene_mutations = []
        for input_hgvs in input_mutations:
            try:
                gene_mutation = mutation_service.get_gene_mutation(input_hgvs)
                gene_mutations.append(gene_mutation)
            except Exception as e:
                logger.error(f"Error processing mutation {input_hgvs}: {e}")
                raise
        return gene_mutations
