import requests
import logging
import backoff
from typing import Dict, Any
from requests.exceptions import HTTPError

logger = logging.getLogger(__name__)


class VariantValidatorNormalizationError(Exception):
    """Raised when normalization or transcript resolution via VariantValidator fails."""
    pass

class VariantValidatorError(Exception):
    """Raised when VariantValidator API returns an error."""
    pass


def giveup_on_non_429(e):
    """Only retry if the error is a 429 (Too Many Requests)."""
    return not (isinstance(e, HTTPError) and e.response.status_code == 429)


class VariantValidatorMutationAdapter:
    """
    Adapter for the VariantValidator API.

    This adapter implements two independent calls:
      1. normalize_mutation: 
         Uses the endpoint:
         <norm_base_url>/<target_assembly>/<variant_description>/<select_transcripts>
      2. resolve_transcripts:
         Uses the endpoint:
         <tools_base_url>/<transcript_id>
    
    The caller is responsible for providing the correct inputs.
    """
    def __init__(self,
                 norm_base_url: str = "https://rest.variantvalidator.org/VariantValidator/variantvalidator/",
                 tools_base_url: str = "https://rest.variantvalidator.org/VariantValidator/tools/gene2transcripts/",
                 fmt_base_url: str = "https://rest.variantvalidator.org/VariantFormatter/variantformatter/"):
        self.NORM_BASE_URL = norm_base_url
        self.TOOLS_BASE_URL = tools_base_url
        self.FMT_BASE_URL = fmt_base_url
        self.session = requests.Session()

    def close(self):
        """Clean up the underlying session."""
        self.session.close()


    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout),
        max_tries=5,
        giveup=giveup_on_non_429
    )
    def normalize_mutation(self, genome_build: str, variant_description: str, select_transcripts: str) -> Dict:
        """
        Normalize the mutation using the VariantValidator API.

        Raises:
            VariantValidatorNormalizationError: If normalization fails, returns empty data,
                or returns a warning flag.
        """
        url = f"{self.NORM_BASE_URL}{genome_build}/{variant_description}/{select_transcripts}"
        logger.info(f"Normalizing mutation via URL: {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()

            norm_data = response.json()
            logger.debug(f"Raw normalization data: {norm_data}")

            # 1) Empty response
            if not norm_data:
                raise VariantValidatorNormalizationError(
                    f"Empty normalization data for {variant_description}"
                )

            # 2) Warning flag from VariantValidator
            if norm_data.get("flag") == "warning":
                # Gather all warning messages into one string
                warnings = []
                # There may be top-level keys like validation_warning_1, validation_warning_2, …
                for key, sub in norm_data.items():
                    if key.startswith("validation_warning_") and isinstance(sub, dict):
                        # Some nested keys are lists of strings
                        wlist = sub.get("validation_warnings") or []
                        warnings.extend(wlist)
                        # Also LOVD messages if present
                        lovd = sub.get("lovd_messages", {})
                        warnings.extend(lovd.values())
                message = "; ".join(warnings) or "Unknown normalization warning"
                logger.error(f"VariantValidator warning for {variant_description}: {message}")
                raise VariantValidatorNormalizationError(
                    f"Normalization warning for {variant_description}: {message}"
                )

            # 3) Success
            logger.debug(f"Normalization data: {norm_data}")
            return norm_data

        except HTTPError as http_err:
            # Let backoff retry on 429
            if response.status_code == 429:
                logger.warning(f"Rate limit exceeded for {variant_description}. Retrying…")
                raise
            logger.error(f"HTTP error occurred: {http_err}")
            raise VariantValidatorNormalizationError(
                f"HTTP error occurred: {http_err}"
            ) from http_err

        except Exception as e:
            logger.error(f"Error normalizing mutation {variant_description}: {e}")
            raise VariantValidatorNormalizationError(
                f"Error normalizing mutation {variant_description}"
            ) from e


    @backoff.on_exception(
        backoff.expo,
        (requests.exceptions.HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout),
        max_tries=5,
        giveup=giveup_on_non_429
    )
    def resolve_transcripts(self, transcript_id: str) -> Dict:
        """
        Resolve available transcripts for a given gene using the gene2transcripts endpoint.

        Parameters:
            transcript_id (str): The transcript identifier (may not include a version, e.g., "NM_001110792").

        Returns:
            dict: The JSON response from VariantValidator containing transcript information.

        Raises:
            VariantValidatorNormalizationError: If the API call fails or returns empty data.
        """
        url = f"{self.TOOLS_BASE_URL}{transcript_id}"
        logger.info(f"Resolving transcripts via URL: {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            if not data:
                raise VariantValidatorNormalizationError(f"Empty transcript data for {transcript_id}")
            logger.debug(f"Transcript resolution data: {data}")
            return data
        except HTTPError as http_err:
            if response.status_code == 429:
                logger.warning(f"Rate limit exceeded for transcript {transcript_id}. Retrying...")
                raise http_err
            else:
                logger.error(f"HTTP error occurred while resolving transcript: {http_err}")
                raise VariantValidatorNormalizationError(f"HTTP error occurred: {http_err}") from http_err
        except Exception as e:
            logger.error(f"Error resolving transcript {transcript_id}: {e}")
            raise VariantValidatorNormalizationError(f"Error resolving transcript {transcript_id}") from e


    @backoff.on_exception(
        backoff.expo,
        (HTTPError, requests.exceptions.ConnectionError, requests.exceptions.Timeout),
        max_tries=5,
        giveup=giveup_on_non_429
    )
    def format_variant(
        self,
        genomic_hgvs: str,
        select_transcripts: str,
        genome_build: str,
        transcript_model: str = "refseq",
        use_hgvs: bool = False
    ) -> Dict[str, Any]:
        """
        Fetch transcript- and protein-level HGVS via VariantFormatter.

        GET /VariantFormatter/variantformatter/{build}/{genomic_hgvs}/{select_transcripts}/{use_hgvs}

        - genomic_hgvs: e.g. "NC_000023.11:g.154030912G>A"
        - select_transcripts: e.g. "NM_004992.4|NM_001110792.2"
        - use_hgvs: if True, returns HGVS-formatted coords in certain fields
        """
        flag = "True" if use_hgvs else "False"
        # quote the genomic HGVS so characters like ":" and ">" are URL-safe
        encoded_genomic_hgvs = requests.utils.quote(genomic_hgvs, safe="")
        url = f"{self.FMT_BASE_URL}{genome_build}/{encoded_genomic_hgvs}/{transcript_model}/{select_transcripts}/{flag}"
        logger.info(f"Formatting variant via URL: {url}")
        try:
            response = self.session.get(url)
            response.raise_for_status()
            data = response.json()
            entry = data.get(genomic_hgvs)
            if not entry or entry.get("errors"):
                errs = entry.get("errors") if entry else data.get("errors")
                raise VariantValidatorNormalizationError(f"Formatter errors for {genomic_hgvs}: {errs}")
            return entry[genomic_hgvs]
        except HTTPError as http_err:
            if response.status_code == 429:
                logger.warning(f"Rate limit exceeded for formatter {genomic_hgvs}, retrying...")
                raise
            logger.error(f"HTTP error during formatting: {http_err}")
            raise VariantValidatorNormalizationError(str(http_err)) from http_err
        except Exception as e:
            logger.error(f"Error formatting variant {genomic_hgvs}: {e}")
            raise VariantValidatorNormalizationError(str(e)) from e
