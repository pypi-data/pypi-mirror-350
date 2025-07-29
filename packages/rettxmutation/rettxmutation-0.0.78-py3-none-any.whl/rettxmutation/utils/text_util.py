import re


def check_genetic_info(document_text):
    mutation_pattern = re.compile(
        r'c\.\d+'
        r'(?:_\d+)?'
        r'(?:[ACGT]>[ACGT]|del|ins[ACGT]+|dup[ACGT]*)',
        flags=re.IGNORECASE
    )
    
    transcript_pattern = re.compile(r'NM_\d+\.\d+')
    
    # Normalizing whitespace
    text = ' '.join(document_text.split())

    regex_has_mutation = bool(mutation_pattern.search(text))
    regex_has_transcript = bool(transcript_pattern.search(text))
    
    return regex_has_mutation or regex_has_transcript