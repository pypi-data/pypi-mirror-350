import re
from typing import List, Set, Union


class MutationTokenizator:
    """
    A string tokenizer for mutation strings (HGVS-like format).
    
    This tokenizer generates as many separate tokens as possible from mutation strings
    by systematically breaking them down using a clean algorithmic approach.
    
    Algorithm:
    1. Normalize input (trim, optionally lowercase)
    2. Include the whole string as a token
    3. Split transcript vs mutation (by colon)
    4. Extract pieces by splitting on HGVS separators
    5. Create atomic piece tokens
    6. Create consecutive-piece combinations
    7. Filter and sort by length
    
    Examples:
        NM_004992.4:c.916C>T -> NM_004992.4, c.916C>T, 916C>T, 916C, C>T, etc.
        NP_004983.1:p.(Arg306Cys) -> NP_004983.1, p.Arg306Cys, Arg306Cys, Arg306, 306, Cys, etc.
    """
      # HGVS separators for splitting mutation parts
    HGVS_SEPARATORS = [':', '(', ')', '.', '_', '+', '-', '>', '<']
    
    # HGVS prefixes that should be treated as separators
    HGVS_PREFIXES = ['c.', 'p.', 'g.', 'm.', 'n.', 'r.']
      # Minimum token length (tokens shorter than this are filtered out)
    MIN_TOKEN_LENGTH = 3

    @classmethod
    def tokenize(cls,
                 mutation_string: str,
                 include_original: bool = True, 
                 lowercase: bool = False,
                 min_token_length: int = None, 
                 return_as_string: bool = False,
                 separator: str = ' '):
        """
        Tokenize a mutation string into all possible meaningful components.
        
        Args:
            mutation_string (str): The mutation string to tokenize (e.g., "NM_004992.4:c.916C>T")
            include_original (bool): Whether to include the original string in the tokens
            lowercase (bool): Whether to convert to lowercase for normalization
            min_token_length (int): Minimum token length (default: class MIN_TOKEN_LENGTH)
            return_as_string (bool): If True, return tokens as space-separated string; if False, return as list
            separator (str): Separator to use when return_as_string=True (default: space)
            
        Returns:
            Union[List[str], str]: List of unique tokens or space-separated string, sorted by length (descending)
        """
        if not mutation_string or not isinstance(mutation_string, str):
            return "" if return_as_string else []
        
        if min_token_length is None:
            min_token_length = cls.MIN_TOKEN_LENGTH
        
        tokens = set()
        
        # 1. Normalize Input
        normalized = mutation_string.strip()
        if lowercase:
            normalized = normalized.lower()
        
        # 2. Include the Whole String
        if include_original and len(normalized) >= min_token_length:
            tokens.add(normalized)
        
        # 3. Transcript vs. Mutation Split
        if ':' in normalized:
            transcript_part, mutation_part = normalized.split(':', 1)
            transcript_part = transcript_part.strip()
            mutation_part = mutation_part.strip()
            
            # Add transcript as its own token
            if transcript_part and len(transcript_part) >= min_token_length:
                tokens.add(transcript_part)
            
            # Process the mutation part
            if mutation_part:
                mutation_tokens = cls._process_mutation_part(mutation_part, min_token_length)
                tokens.update(mutation_tokens)
        else:
            # If no colon, treat entire string as mutation part
            mutation_tokens = cls._process_mutation_part(normalized, min_token_length)
            tokens.update(mutation_tokens)
        
        # 7. Filter & Sort
        filtered_tokens = [token for token in tokens if len(token) >= min_token_length]
        sorted_tokens = sorted(filtered_tokens, key=len, reverse=True)
        
        # Return as string or list based on parameter
        if return_as_string:
            return separator.join(sorted_tokens)
        else:
            return sorted_tokens
    
    @classmethod
    def _process_mutation_part(cls, mutation_part: str, min_token_length: int) -> Set[str]:
        """
        Process the mutation part of the string according to the algorithm.
        
        Args:
            mutation_part (str): The mutation part to process
            min_token_length (int): Minimum token length
            
        Returns:
            Set[str]: Set of tokens extracted from the mutation part
        """
        tokens = set()
          # Add the mutation part itself as a token
        if len(mutation_part) >= min_token_length:
            tokens.add(mutation_part)
        
        # Special handling for parentheses patterns like p.(Arg306Cys) -> p.Arg306Cys
        parentheses_tokens = cls._extract_parentheses_variants(mutation_part)
        tokens.update(var for var in parentheses_tokens if len(var) >= min_token_length)
        
        # 4. Piece Extraction
        pieces = cls._extract_pieces(mutation_part)
        
        # Special handling for substitution patterns (preserve > patterns)
        substitution_tokens = cls._extract_substitution_patterns(mutation_part)
        tokens.update(sub for sub in substitution_tokens if len(sub) >= min_token_length)
        
        # 5. Break down pieces into atomic components and generate all combinations
        for piece in pieces:
            if len(piece) >= min_token_length:
                tokens.add(piece)
            
            # Break down each piece into atomic components (letters/numbers)
            atomic_components = cls._break_into_atomic_components(piece)
            
            # Add atomic components as tokens
            for component in atomic_components:
                if len(component) >= min_token_length:
                    tokens.add(component)
            
            # Generate consecutive combinations of atomic components
            tokens.update(cls._generate_consecutive_combinations(atomic_components, min_token_length))
        
        # 6. Also generate consecutive combinations of the original pieces
        tokens.update(cls._generate_consecutive_combinations(pieces, min_token_length))
        
        return tokens

    @classmethod
    def _extract_parentheses_variants(cls, text: str) -> Set[str]:
        """
        Extract variants for parentheses patterns.
        
        For example: "p.(Arg306Cys)" -> {"p.Arg306Cys"}
                    "c.(916C>T)" -> {"c.916C>T"}
        
        Args:
            text (str): Text to extract parentheses variants from
            
        Returns:
            Set[str]: Set of parentheses variants
        """
        tokens = set()
        
        # Look for patterns like "prefix.(content)" and create "prefix.content"
        paren_patterns = re.findall(r'([A-Za-z]+\.)\(([^)]+)\)', text)
        for prefix, content in paren_patterns:
            # Create token with prefix and content (removing parentheses)
            combined = f"{prefix}{content}"
            tokens.add(combined)
        
        return tokens

    @classmethod
    def _extract_pieces(cls, text: str) -> List[str]:
        """
        Extract pieces by splitting on HGVS separators and removing HGVS prefixes.
        
        Args:
            text (str): Text to split into pieces
            
        Returns:
            List[str]: List of non-empty pieces
        """
        # First, remove HGVS prefixes (c., p., etc.)
        working_text = text
        for prefix in cls.HGVS_PREFIXES:
            working_text = working_text.replace(prefix, ' ')
        
        # Create regex pattern for all separators (excluding > for special handling)
        separators_without_gt = [sep for sep in cls.HGVS_SEPARATORS if sep not in ['>', '<']]
        separator_pattern = '[' + re.escape(''.join(separators_without_gt)) + ']'
        
        # Split by separators (but not > or <)
        pieces = re.split(separator_pattern, working_text)
        
        # For > and < patterns, we need special handling to preserve substitution patterns
        final_pieces = []
        for piece in pieces:
            if '>' in piece or '<' in piece:
                # Don't split on > or <, keep the substitution pattern intact
                final_pieces.append(piece.strip())
            else:
                final_pieces.append(piece.strip())
        
        # Filter out empty pieces
        pieces = [piece for piece in final_pieces if piece]
        
        return pieces
    
    @classmethod
    def _generate_consecutive_combinations(cls, pieces: List[str], min_token_length: int) -> Set[str]:
        """
        Generate all consecutive combinations of pieces.
        
        Args:
            pieces (List[str]): List of pieces to combine
            min_token_length (int): Minimum token length
            
        Returns:
            Set[str]: Set of consecutive combinations
        """
        tokens = set()
        
        # Generate all consecutive combinations
        for i in range(len(pieces)):
            for j in range(i + 1, len(pieces) + 1):
                # Join pieces from i to j-1
                combination = ''.join(pieces[i:j])
                if len(combination) >= min_token_length:
                    tokens.add(combination)
        
        return tokens

    @classmethod
    def _extract_substitution_patterns(cls, text: str) -> Set[str]:
        """
        Extract substitution patterns like C>T, Arg>Cys to preserve them as meaningful tokens.
        
        Args:
            text (str): Text to extract substitution patterns from
            
        Returns:
            Set[str]: Set of substitution patterns
        """
        tokens = set()
        
        # Find substitution patterns with > or <
        substitution_patterns = re.findall(r'[A-Za-z]+[><][A-Za-z]+', text)
        tokens.update(substitution_patterns)
        
        return tokens

    @classmethod
    def _break_into_atomic_components(cls, piece: str) -> List[str]:
        """
        Break down a piece into atomic components (sequences of letters or numbers).
        
        For example: "Arg306Cys" -> ["Arg", "306", "Cys"]
                    "916C" -> ["916", "C"]
                    "T445" -> ["T", "445"]
        
        Args:
            piece (str): Piece to break down
            
        Returns:
            List[str]: List of atomic components
        """
        if not piece:
            return []
        
        # Use regex to find sequences of letters or numbers
        components = re.findall(r'[A-Za-z]+|\d+', piece)
        
        return [comp for comp in components if comp]

    @classmethod
    def tokenize_to_string(cls, mutation_string: str, separator: str = ' ', include_original: bool = True,
                          lowercase: bool = False, min_token_length: int = None) -> str:
        """
        Tokenize a mutation string and return as a separated string.
        
        Args:
            mutation_string (str): The mutation string to tokenize
            separator (str): Separator to use between tokens (default: space)
            include_original (bool): Whether to include the original string
            lowercase (bool): Whether to convert to lowercase for normalization
            min_token_length (int): Minimum token length            
        Returns:
            str: Separated tokens
        """
        tokens = cls.tokenize(mutation_string, include_original=include_original,
                             lowercase=lowercase, min_token_length=min_token_length)
        return separator.join(tokens)

    @classmethod
    def get_unique_tokens(cls,
                          gene_mutation_list: List[str],
                          lowercase: bool = False,
                          min_token_length: int = None) -> List[str]:
        """
        Get unique tokens from a list of mutation strings, returned as a list.
        
        Args:
            gene_mutation_list (List[str]): List of gene mutation strings to tokenize
            lowercase (bool): Whether to convert to lowercase for normalization
            min_token_length (int): Minimum token length
            
        Returns:
            List[str]: List of unique tokens across all strings, sorted by length (descending)
        """
        all_tokens = set()

        for mutation_string in gene_mutation_list:
            tokens = cls.tokenize(mutation_string,
                                  lowercase=lowercase,
                                  min_token_length=min_token_length,
                                  return_as_string=False)  # Always get as list
            all_tokens.update(tokens)
        
        return sorted(list(all_tokens), key=len, reverse=True)

    @classmethod
    def get_unique_tokens_as_string(cls,
                                    gene_mutation_list: List[str],
                                    separator: str = ' ',
                                    lowercase: bool = False,
                                    min_token_length: int = None) -> str:
        """
        Get unique tokens from a list of mutation strings, returned as a separated string.
        
        Args:
            gene_mutation_list (List[str]): List of gene mutation strings to tokenize
            separator (str): Separator to use between tokens (default: space)
            lowercase (bool): Whether to convert to lowercase for normalization
            min_token_length (int): Minimum token length
            
        Returns:
            str: Unique tokens joined by separator, sorted by length (descending)
        """
        tokens = cls.get_unique_tokens(gene_mutation_list, lowercase=lowercase, min_token_length=min_token_length)
        return separator.join(tokens)
