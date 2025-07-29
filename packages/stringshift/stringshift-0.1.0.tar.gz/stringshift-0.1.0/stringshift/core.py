import urllib.parse
import html
import codecs
import unicodedata
from functools import lru_cache
from typing import Optional, Union, Literal
from concurrent.futures import ThreadPoolExecutor
import os

# Optional chardet import with fallback
try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False

# Type aliases
NormalizationForm = Literal['NFC', 'NFD', 'NFKC', 'NFKD']

class DecodeError(Exception):
    """Custom exception for decoding failures"""
    def __init__(self, original: str, error: Exception):
        self.original = original
        self.error = error
        super().__init__(f"Failed to decode: {original[:50]}... (Error: {str(error)})")

@lru_cache(maxsize=2048)
def _cached_url_decode(text: str) -> str:
    """Optimized URL decoding with caching"""
    return urllib.parse.unquote(text)

def decode_url(text: str) -> str:
    """Decodes percent-encoded text with smart caching"""
    if len(text) > 4096:  # Bypass cache for large texts
        return urllib.parse.unquote(text)
    return _cached_url_decode(text)

def decode_html(text: str) -> str:
    """Decodes HTML entities to their characters"""
    return html.unescape(text)

def decode_escapes(text: str) -> str:
    """Handles hex/unicode escape sequences"""
    try:
        return codecs.escape_decode(text.encode('latin-1'))[0].decode('utf-8')
    except ValueError as e:
        raise DecodeError(text, e)

def decode_hex(text: str) -> str:
    """Converts hex strings to readable text"""
    try:
        clean_text = text.replace('0x', '').replace(' ', '')
        return bytes.fromhex(clean_text).decode('utf-8')
    except ValueError as e:
        raise DecodeError(text, e)

def normalize_text(text: str, form: NormalizationForm = 'NFC') -> str:
    """Applies Unicode normalization"""
    return unicodedata.normalize(form, text)

def detect_encoding(data: bytes) -> str:
    """Auto-detects text encoding with fallback"""
    if HAS_CHARDET:
        result = chardet.detect(data)
        return result['encoding'] or 'utf-8'
    # Common encodings to try if chardet not available
    for encoding in ['utf-8', 'latin-1', 'ascii']:
        try:
            data.decode(encoding)
            return encoding
        except UnicodeDecodeError:
            continue
    return 'utf-8'  # Default fallback

def auto_decode(data: bytes) -> str:
    """Intelligently converts bytes to text with robust fallback"""
    encoding = detect_encoding(data)
    try:
        return data.decode(encoding)
    except UnicodeDecodeError:
        # Final fallback with replacement characters for invalid bytes
        return data.decode('utf-8', errors='replace')

def decode_all(
    text: Union[str, bytes],
    normalization: Optional[NormalizationForm] = None,
    fallback: Optional[str] = None
) -> str:
    """
    Universal text decoder with:
    - URL decoding
    - HTML entity conversion
    - Escape sequence handling
    - Optional normalization
    - Graceful fallback handling
    """
    try:
        if isinstance(text, bytes):
            text = auto_decode(text)
        
        result = decode_escapes(text)
        result = decode_url(result)
        result = decode_html(result)
        
        if normalization:
            result = normalize_text(result, form=normalization)
            
        return result
    except Exception as e:
        if fallback is not None:
            return fallback
        raise DecodeError(
            text if isinstance(text, str) else text.decode('ascii', errors='replace'), 
            e
        )

def batch_decode(
    texts: list[Union[str, bytes]],
    workers: Optional[int] = None,
    **kwargs
) -> list[str]:
    """
    Parallel processing for bulk text conversion
    kwargs are passed to decode_all()
    """
    workers = workers or min(32, (os.cpu_count() or 1) + 4)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(lambda t: decode_all(t, **kwargs), texts))