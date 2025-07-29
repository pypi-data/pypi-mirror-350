import logging
import numpy as np
from typing import List, Dict, Any
from rettxmutation.models.mutation_model import Mutation
from rettxmutation.models.gene_models import GeneMutation

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for creating and managing embeddings from GeneMutation objects.
    This service can be used to create embeddings for search, clustering,
    or similarity comparisons of genetic mutations.
    """

    def __init__(self, embedding_model=None):
        """
        Initialize the embedding service.

        Args:
            embedding_model: Optional model to use for generating embeddings.
                            If None, will use the default model.
        """
        self.embedding_model = embedding_model
        # Default dimensions for embeddings if not specified
        self.embedding_dimensions = 1536  # Common for many embedding models

    @staticmethod
    def mutation_to_embedding_string(mutation: GeneMutation) -> str:
        """
        Convert a GeneMutation to a string for embedding

        Args:
            mutation: The GeneMutation object to convert

        Returns:
            str: String representation of the mutation
        """
        parts = []

        # gene (use primary if present, else secondary)
        gene = (
            mutation.primary_transcript.gene_id
            if mutation.primary_transcript and mutation.primary_transcript.gene_id
            else getattr(mutation.secondary_transcript, "gene_id", "")
        )
        parts.append(f"Gene: {gene}")

        # primary transcript/protein
        if mutation.primary_transcript:
            pt = mutation.primary_transcript
            parts.append(f"Primary transcript: {pt.hgvs_transcript_variant}")
            if pt.protein_consequence_slr or pt.protein_consequence_tlr:
                prot = pt.protein_consequence_slr or pt.protein_consequence_tlr
                parts.append(f"Primary protein: {prot}")

        # secondary transcript/protein
        if mutation.secondary_transcript:
            st = mutation.secondary_transcript
            parts.append(f"Secondary transcript: {st.hgvs_transcript_variant}")
            if st.protein_consequence_slr or st.protein_consequence_tlr:
                sprot = st.protein_consequence_slr or st.protein_consequence_tlr
                parts.append(f"Secondary protein: {sprot}")

        # variant type
        parts.append(f"Variant type: {mutation.variant_type}")

        # genomic coords (pick both assemblies if present)
        if mutation.genomic_coordinates:
            for coord in mutation.genomic_coordinates.values():
                parts.append(f"{coord.assembly}: {coord.hgvs}")
        # legacy fallback
        elif mutation.genomic_coordinate:
            parts.append(f"Genomic coordinate: {mutation.genomic_coordinate}")

        # domain context
        parts.append("Rett Syndrome")

        return " | ".join(parts)

    @staticmethod
    def parse_hgvs_string(input: str) -> Mutation:
        """
        Get mutation details from an input string.

        Args:
            input: The input string to parse

        Returns:
            Mutation: The parsed mutation object
        """
        # This should be replaced with actual parsing logic
        # Example for OpenAI:
        # response = openai.Mutation.create(input=input)
        # mutation = response["data"]

        # Placeholder:
        mutation = Mutation.from_hgvs_string(input)
        return mutation

    def create_embedding(self, mutation: GeneMutation) -> np.ndarray:
        """
        Convert a GeneMutation object to an embedding vector.

        Args:
            mutation: The GeneMutation object to convert

        Returns:
            numpy.ndarray: The embedding vector
        """
        # Convert the mutation to a string representation
        text = self.mutation_to_embedding_string(mutation)

        # Generate embedding from the text
        if self.embedding_model:
            # Use the provided embedding model
            return self._get_embedding_from_model(text)
        else:
            # Use a default method (placeholder for connection to actual embedding service)
            logger.warning("No embedding model provided, returning random embedding as placeholder")
            return self._get_default_embedding()

    def create_embeddings(self, mutations: List[GeneMutation]) -> List[np.ndarray]:
        """
        Create embeddings for a list of mutations.

        Args:
            mutations: List of GeneMutation objects

        Returns:
            List of embedding vectors
        """
        return [self.create_embedding(mutation) for mutation in mutations]

    def _get_embedding_from_model(self, text: str) -> np.ndarray:
        """
        Get embedding from the embedding model.

        Args:
            text: The text to embed

        Returns:
            numpy.ndarray: The embedding vector
        """
        try:
            # This should be replaced with actual model call
            # Example for OpenAI:
            # response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
            # embedding = response["data"][0]["embedding"]

            # Placeholder:
            embedding = np.random.rand(self.embedding_dimensions)
            return embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return self._get_default_embedding()

    def _get_default_embedding(self) -> np.ndarray:
        """
        Return a default placeholder embedding.

        Returns:
            numpy.ndarray: A random embedding vector
        """
        return np.random.rand(self.embedding_dimensions)

    def find_similar_mutations(
        self,
        query_mutation: GeneMutation,
        mutation_library: List[GeneMutation],
        top_k: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find mutations similar to the query mutation.

        Args:
            query_mutation: The mutation to find similar mutations for
            mutation_library: The library of mutations to search
            top_k: The number of similar mutations to return

        Returns:
            List of dictionaries with mutation and similarity score
        """
        query_embedding = self.create_embedding(query_mutation)

        results = []
        for mutation in mutation_library:
            mutation_embedding = self.create_embedding(mutation)
            similarity = self._calculate_similarity(query_embedding, mutation_embedding)
            results.append({
                "mutation": mutation,
                "similarity": similarity
            })

        # Sort by similarity score (highest first)
        results.sort(key=lambda x: x["similarity"], reverse=True)

        # Return top_k results
        return results[:top_k]

    @staticmethod
    def _calculate_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Calculate cosine similarity between two vectors.

        Args:
            vec1: First vector
            vec2: Second vector

        Returns:
            float: Cosine similarity score between 0 and 1
        """
        # Cosine similarity: dot product divided by the product of magnitudes
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)

        # Avoid division by zero
        if norm1 == 0 or norm2 == 0:
            return 0.0

        return dot_product / (norm1 * norm2)
