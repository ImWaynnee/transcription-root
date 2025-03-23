def clean_transcription(text: str) -> str:
    """
    Clean up transcription text
    """
    # Remove leading/trailing whitespace
    text = text.strip()
    
    # Remove multiple spaces
    text = ' '.join(text.split())
    
    # Ensure proper capitalization of sentences
    sentences = text.split('. ')
    sentences = [s.capitalize() for s in sentences if s]
    text = '. '.join(sentences)
    
    return text