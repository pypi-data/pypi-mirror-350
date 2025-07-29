__version__ = "1.0.0"
__all__ = [
    'decode_all',
    'decode_url',
    'decode_html',
    'decode_escapes',
    'decode_hex',
    'normalize_text',
    'batch_decode',
    'DecodeError'
]

from .core import (
    decode_all,
    decode_url,
    decode_html,
    decode_escapes,
    decode_hex,
    normalize_text,
    batch_decode,
    DecodeError
)