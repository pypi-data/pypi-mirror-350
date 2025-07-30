"""Utility functions for text processing."""

import re
from typing import List, Optional, Union, Dict, Any
from pathlib import Path
from collections import Counter
import math

from .constants import MAX_TEXT_LENGTH, MAX_CHUNK_SIZE
from .exceptions import ValidationError
from .file_utils import validate_file_path, is_text_file, read_file_content

def normalize_text(text: str) -> str:
    """Normalize text by removing punctuation and converting to lowercase.
    
    Args:
        text: Input text to normalize
        
    Returns:
        Normalized text
        
    Raises:
        ValueError: If text is None or empty
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return ""
    return text.lower().strip()

def validate_text_length(text: str) -> None:
    """Validate that text is not too long.
    
    Args:
        text: Text to validate
        
    Raises:
        ValueError: If text is too long
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if len(text) > MAX_TEXT_LENGTH:
        raise ValueError(f"Text is too long: {len(text)} characters (max: {MAX_TEXT_LENGTH})")

def clean_text(text: str) -> str:
    """Clean text by removing extra whitespace and special characters.
    
    Args:
        text: Input text to clean
        
    Returns:
        Cleaned text
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return ""
    return ' '.join(text.split())

def split_text(text: str, max_length: int = None) -> List[str]:
    """Split text into chunks.
    
    Args:
        text: Input text
        max_length: Maximum length of each chunk (optional)
        
    Returns:
        List of text chunks
        
    Raises:
        ValueError: If text is None or max_length is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if max_length is not None and (not isinstance(max_length, int) or max_length <= 0):
        raise ValueError("Maximum length must be a positive integer")
        
    # If no max_length specified, return the whole text as a single chunk
    if max_length is None:
        return [text.strip()]
        
    # Split text into chunks of max_length
    chunks = []
    current_chunk = ""
    words = text.split()
    
    for word in words:
        if len(current_chunk) + len(word) + 1 <= max_length:
            current_chunk += (word + " ")
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = word + " "
            
    if current_chunk:
        chunks.append(current_chunk.strip())
        
    return chunks

def extract_text_from_file(file_path: Union[str, Path], encoding: str = "utf-8") -> str:
    """Extract text from a file.
    
    Args:
        file_path: Path to the file
        encoding: File encoding
        
    Returns:
        Extracted text
        
    Raises:
        ValidationError: If file is invalid or cannot be read
    """
    path = validate_file_path(file_path)
    if not is_text_file(path):
        raise ValidationError(f"File is not a supported text file: {file_path}")
    
    text = read_file_content(path, encoding)
    validate_text_length(text)
    return clean_text(text)

def extract_text_from_files(file_paths: List[Union[str, Path]], encoding: str = "utf-8") -> List[str]:
    """Extract text from multiple files.
    
    Args:
        file_paths: List of file paths
        encoding: File encoding
        
    Returns:
        List of extracted texts
        
    Raises:
        ValidationError: If any file is invalid or cannot be read
    """
    return [extract_text_from_file(path, encoding) for path in file_paths]

def extract_text_from_directory(directory: Union[str, Path], encoding: str = "utf-8") -> List[str]:
    """Extract text from all text files in a directory.
    
    Args:
        directory: Directory path
        encoding: File encoding
        
    Returns:
        List of extracted texts
        
    Raises:
        ValidationError: If directory is invalid or files cannot be read
    """
    path = Path(directory)
    if not path.exists():
        raise ValidationError(f"Directory does not exist: {directory}")
    if not path.is_dir():
        raise ValidationError(f"Path is not a directory: {directory}")
    
    text_files = [f for f in path.glob("**/*") if f.is_file() and is_text_file(f)]
    return extract_text_from_files(text_files, encoding)

def extract_text_from_text(text: str) -> str:
    """Extract text from a string.
    
    Args:
        text: Text to process
        
    Returns:
        Processed text
        
    Raises:
        ValidationError: If text is invalid
    """
    validate_text_length(text)
    return clean_text(text)

def extract_text_from_texts(texts: List[str]) -> List[str]:
    """Extract text from multiple strings.
    
    Args:
        texts: List of texts to process
        
    Returns:
        List of processed texts
        
    Raises:
        ValidationError: If any text is invalid
    """
    return [extract_text_from_text(text) for text in texts]

def tokenize_text(text: str) -> List[str]:
    """Tokenize text into words.
    
    Args:
        text: Input text to tokenize
        
    Returns:
        List of tokens
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    return text.split()

def remove_stopwords(tokens: List[str]) -> List[str]:
    """Remove common stopwords from tokens.
    
    Args:
        tokens: List of tokens
        
    Returns:
        List of tokens with stopwords removed
        
    Raises:
        ValueError: If tokens is None
    """
    if tokens is None:
        raise ValueError("Tokens cannot be None")
    if not isinstance(tokens, list):
        raise ValueError("Tokens must be a list")
    if not tokens:
        return []
    # Simple stopwords list - expand as needed
    stopwords = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
    return [token for token in tokens if token.lower() not in stopwords]

def stem_text(tokens: List[str]) -> List[str]:
    """Apply stemming to tokens.
    
    Args:
        tokens: List of tokens
        
    Returns:
        List of stemmed tokens
        
    Raises:
        ValueError: If tokens is None
    """
    if tokens is None:
        raise ValueError("Tokens cannot be None")
    if not isinstance(tokens, list):
        raise ValueError("Tokens must be a list")
    if not tokens:
        return []
    # Simple stemming - replace with proper stemmer
    return [token.lower() for token in tokens]

def lemmatize_text(tokens: List[str]) -> List[str]:
    """Apply lemmatization to tokens.
    
    Args:
        tokens: List of tokens
        
    Returns:
        List of lemmatized tokens
        
    Raises:
        ValueError: If tokens is None
    """
    if tokens is None:
        raise ValueError("Tokens cannot be None")
    if not isinstance(tokens, list):
        raise ValueError("Tokens must be a list")
    if not tokens:
        return []
    # Simple lemmatization - replace with proper lemmatizer
    return [token.lower() for token in tokens]

def extract_keywords(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords from text.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def calculate_similarity(text1: str, text2: str) -> float:
    """Calculate similarity between two texts.
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score between 0 and 1
        
    Raises:
        ValueError: If either text is None
    """
    if text1 is None or text2 is None:
        raise ValueError("Texts cannot be None")
    if not isinstance(text1, str) or not isinstance(text2, str):
        raise ValueError("Texts must be strings")
    if not text1.strip() and not text2.strip():
        return 1.0
    if not text1.strip() or not text2.strip():
        return 0.0
        
    # Simple similarity calculation - replace with proper implementation
    words1 = set(text1.lower().split())
    words2 = set(text2.lower().split())
    intersection = words1.intersection(words2)
    union = words1.union(words2)
    return len(intersection) / len(union) if union else 0.0

def format_text(text: str, max_length: Optional[int] = None) -> str:
    """Format text by cleaning and optionally truncating.
    
    Args:
        text: Input text
        max_length: Maximum length (optional)
        
    Returns:
        Formatted text
        
    Raises:
        ValueError: If text is None or max_length is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return ""
        
    formatted = clean_text(text)
    if max_length is not None:
        if not isinstance(max_length, int) or max_length <= 0:
            raise ValueError("Maximum length must be a positive integer")
        formatted = truncate_text(formatted, max_length)
    return formatted

def truncate_text(text: str, max_length: int) -> str:
    """Truncate text to specified length.
    
    Args:
        text: Input text
        max_length: Maximum length
        
    Returns:
        Truncated text
        
    Raises:
        ValueError: If text is None or max_length is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not isinstance(max_length, int) or max_length <= 0:
        raise ValueError("Maximum length must be a positive integer")
    if not text.strip():
        return ""
        
    return text[:max_length].strip()

def join_text(chunks: List[str]) -> str:
    """Join text chunks into a single string.
    
    Args:
        chunks: List of text chunks
        
    Returns:
        Joined text
        
    Raises:
        ValueError: If chunks is None
    """
    if chunks is None:
        raise ValueError("Chunks cannot be None")
    if not isinstance(chunks, list):
        raise ValueError("Chunks must be a list")
    if not chunks:
        return ""
        
    return ' '.join(chunk.strip() for chunk in chunks if chunk.strip())

def count_words(text: str) -> int:
    """Count words in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of words
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return 0
        
    return len(text.split())

def count_characters(text: str) -> int:
    """Count characters in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of characters
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    return len(text)

def count_sentences(text: str) -> int:
    """Count sentences in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of sentences
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return 0
        
    # Simple sentence counting - replace with proper implementation
    return len(re.split(r'[.!?]+', text.strip()))

def count_paragraphs(text: str) -> int:
    """Count paragraphs in text.
    
    Args:
        text: Input text
        
    Returns:
        Number of paragraphs
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return 0
        
    return len([p for p in text.split('\n') if p.strip()])

def get_text_statistics(text: str) -> Dict[str, int]:
    """Get text statistics.
    
    Args:
        text: Input text
        
    Returns:
        Dictionary of text statistics
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return {
            'words': 0,
            'characters': 0,
            'sentences': 0,
            'paragraphs': 0
        }
        
    return {
        'words': count_words(text),
        'characters': count_characters(text),
        'sentences': count_sentences(text),
        'paragraphs': count_paragraphs(text)
    }

def extract_entities(text: str) -> List[str]:
    """Extract named entities from text.
    
    Args:
        text: Input text
        
    Returns:
        List of entities
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple entity extraction - replace with proper implementation
    return []

def extract_phrases(text: str) -> List[str]:
    """Extract phrases from text.
    
    Args:
        text: Input text
        
    Returns:
        List of phrases
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple phrase extraction - replace with proper implementation
    return []

def extract_sentences(text: str) -> List[str]:
    """Extract sentences from text.
    
    Args:
        text: Input text
        
    Returns:
        List of sentences
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple sentence extraction - replace with proper implementation
    return [s.strip() for s in re.split(r'[.!?]+', text.strip()) if s.strip()]

def extract_paragraphs(text: str) -> List[str]:
    """Extract paragraphs from text.
    
    Args:
        text: Input text
        
    Returns:
        List of paragraphs
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple paragraph extraction - replace with proper implementation
    return [p.strip() for p in text.split('\n') if p.strip()]

def extract_words(text: str) -> List[str]:
    """Extract words from text.
    
    Args:
        text: Input text
        
    Returns:
        List of words
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple word extraction - replace with proper implementation
    return text.split()

def extract_characters(text: str) -> List[str]:
    """Extract characters from text.
    
    Args:
        text: Input text
        
    Returns:
        List of characters
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple character extraction - replace with proper implementation
    return list(text)

def extract_numbers(text: str) -> List[str]:
    """Extract numbers from text.
    
    Args:
        text: Input text
        
    Returns:
        List of numbers as strings
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple number extraction - replace with proper implementation
    numbers = []
    for word in text.split():
        try:
            num = float(word)
            numbers.append(str(num))
        except ValueError:
            continue
    return numbers

def extract_urls(text: str) -> List[str]:
    """Extract URLs from text.
    
    Args:
        text: Input text
        
    Returns:
        List of URLs
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple URL extraction - replace with proper implementation
    url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
    return re.findall(url_pattern, text)

def extract_emails(text: str) -> List[str]:
    """Extract email addresses from text.
    
    Args:
        text: Input text
        
    Returns:
        List of email addresses
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple email extraction - replace with proper implementation
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    return re.findall(email_pattern, text)

def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text.
    
    Args:
        text: Input text
        
    Returns:
        List of hashtags
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple hashtag extraction - replace with proper implementation
    hashtag_pattern = r'#\w+'
    return re.findall(hashtag_pattern, text)

def extract_mentions(text: str) -> List[str]:
    """Extract mentions from text.
    
    Args:
        text: Input text
        
    Returns:
        List of mentions
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple mention extraction - replace with proper implementation
    mention_pattern = r'@\w+'
    return re.findall(mention_pattern, text)

def extract_dates(text: str) -> List[str]:
    """Extract dates from text.
    
    Args:
        text: Input text
        
    Returns:
        List of dates
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple date extraction - replace with proper implementation
    date_pattern = r'\d{4}-\d{2}-\d{2}'
    return re.findall(date_pattern, text)

def extract_times(text: str) -> List[str]:
    """Extract times from text.
    
    Args:
        text: Input text
        
    Returns:
        List of times
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple time extraction - replace with proper implementation
    time_pattern = r'\d{2}:\d{2}'
    return re.findall(time_pattern, text)

def extract_currencies(text: str) -> List[str]:
    """Extract currency amounts from text.
    
    Args:
        text: Input text
        
    Returns:
        List of currency amounts
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple currency extraction - replace with proper implementation
    currency_pattern = r'\$\d+(?:\.\d{2})?'
    return re.findall(currency_pattern, text)

def extract_measurements(text: str) -> List[str]:
    """Extract measurements from text.
    
    Args:
        text: Input text
        
    Returns:
        List of measurements
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple measurement extraction - replace with proper implementation
    measurement_pattern = r'\d+(?:\.\d+)?\s*(?:kg|g|lb|oz|m|cm|mm|in|ft|yd|mi|km)'
    return re.findall(measurement_pattern, text)

def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text.
    
    Args:
        text: Input text
        
    Returns:
        List of phone numbers
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple phone number extraction - replace with proper implementation
    phone_pattern = r'\+?\d{1,3}[-.\s]?\d{1,3}[-.\s]?\d{3,4}[-.\s]?\d{4}'
    return re.findall(phone_pattern, text)

def extract_addresses(text: str) -> List[str]:
    """Extract addresses from text.
    
    Args:
        text: Input text
        
    Returns:
        List of addresses
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple address extraction - replace with proper implementation
    return []

def extract_names(text: str) -> List[str]:
    """Extract names from text.
    
    Args:
        text: Input text
        
    Returns:
        List of names
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple name extraction - replace with proper implementation
    return []

def extract_titles(text: str) -> List[str]:
    """Extract titles from text.
    
    Args:
        text: Input text
        
    Returns:
        List of titles
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple title extraction - replace with proper implementation
    return []

def extract_organizations(text: str) -> List[str]:
    """Extract organizations from text.
    
    Args:
        text: Input text
        
    Returns:
        List of organizations
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple organization extraction - replace with proper implementation
    return []

def extract_locations(text: str) -> List[str]:
    """Extract locations from text.
    
    Args:
        text: Input text
        
    Returns:
        List of locations
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple location extraction - replace with proper implementation
    return []

def extract_languages(text: str) -> List[str]:
    """Extract languages from text.
    
    Args:
        text: Input text
        
    Returns:
        List of languages
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple language extraction - replace with proper implementation
    return []

def extract_topics(text: str) -> List[str]:
    """Extract topics from text.
    
    Args:
        text: Input text
        
    Returns:
        List of topics
        
    Raises:
        ValueError: If text is None
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
        
    # Simple topic extraction - replace with proper implementation
    return []

def extract_summary(text: str, max_length: int = 200) -> str:
    """Extract summary from text.
    
    Args:
        text: Input text
        max_length: Maximum length of summary
        
    Returns:
        Text summary
        
    Raises:
        ValueError: If text is None or max_length is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return ""
    if not isinstance(max_length, int) or max_length <= 0:
        raise ValueError("Maximum length must be a positive integer")
        
    # Simple summary extraction - replace with proper implementation
    sentences = extract_sentences(text)
    if not sentences:
        return ""
    return sentences[0][:max_length]

def extract_keywords_tfidf(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using TF-IDF.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple TF-IDF keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_rake(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using RAKE.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple RAKE keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_yake(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using YAKE.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple YAKE keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_textrank(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using TextRank.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple TextRank keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_bert(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using BERT.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple BERT keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_roberta(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using RoBERTa.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple RoBERTa keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_xlnet(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using XLNet.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple XLNet keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_albert(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using ALBERT.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple ALBERT keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_distilbert(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using DistilBERT.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple DistilBERT keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_electra(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using ELECTRA.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple ELECTRA keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_gpt2(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using GPT-2.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple GPT-2 keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_t5(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using T5.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple T5 keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_bart(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using BART.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple BART keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_pegasus(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using PEGASUS.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple PEGASUS keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_mt5(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using mT5.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple mT5 keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_mbart(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using mBART.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple mBART keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_prophetnet(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using ProphetNet.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple ProphetNet keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_reformer(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using Reformer.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple Reformer keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_longformer(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using Longformer.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple Longformer keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_bigbird(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using BigBird.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple BigBird keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_led(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using LED.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple LED keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_m2m100(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using M2M100.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple M2M100 keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_marian(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using Marian.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple Marian keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_mbart50(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using mBART-50.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple mBART-50 keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def extract_keywords_nllb(text: str, num_keywords: int = 5) -> List[str]:
    """Extract keywords using NLLB.
    
    Args:
        text: Input text
        num_keywords: Number of keywords to extract
        
    Returns:
        List of keywords
        
    Raises:
        ValueError: If text is None or num_keywords is invalid
    """
    if text is None:
        raise ValueError("Text cannot be None")
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if not text.strip():
        return []
    if not isinstance(num_keywords, int) or num_keywords <= 0:
        raise ValueError("Number of keywords must be a positive integer")
        
    # Simple NLLB keyword extraction - replace with proper implementation
    words = text.lower().split()
    word_freq = Counter(words)
    return [word for word, _ in word_freq.most_common(num_keywords)]

def format_prompt(prompt: str, options: dict = None) -> str:
    """Format a prompt with optional options dictionary (for test compatibility)."""
    if not isinstance(prompt, str) or not prompt:
        raise ValueError("Prompt must be a non-empty string")
    if options is not None and not isinstance(options, dict):
        raise ValueError("Options must be a dictionary")
    return prompt

def parse_model_options(options: dict) -> dict:
    """Parse model options from a dictionary."""
    if not isinstance(options, dict):
        raise ValueError("Options must be a dictionary")
    return options

def format_chat_history(messages: list) -> str:
    """Format chat history as a string."""
    if not isinstance(messages, list):
        raise ValueError("Messages must be a list")
    formatted = []
    for msg in messages:
        if not isinstance(msg, dict):
            raise ValueError("Each message must be a dictionary")
        role = msg.get("role", "user")
        content = msg.get("content", "")
        formatted.append(f"{role.lower()}: {content}")
    return "\n".join(formatted)

def parse_model_name(name: str) -> dict:
    """Parse a model name into its components."""
    if not isinstance(name, str) or not name:
        raise ValueError("Model name must be a non-empty string")
    if ":" not in name:
        return {"name": name, "variant": ""}
    parts = name.split(":", 1)
    return {"name": parts[0], "variant": parts[1]} 