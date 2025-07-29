from urllib.parse import unquote
import codecs
import html

def decode_url(text: str) -> str:
    """Decode URL-encoded text (%22 → ")"""
    return unquote(text)

def decode_escapes(text: str) -> str:
    """Decode hex/unicode escapes (\x22 → ", \u0020 → space)"""
    try:
        return text.encode('latin-1').decode('unicode-escape')
    except UnicodeDecodeError:
        return text

def decode_html(text: str) -> str:
    """Decode HTML entities (&quot; → ")"""
    return html.unescape(text)

def decode_all(text: str) -> str:
    """Process decoders in optimal order"""
    # 1. First unescape sequences
    text = decode_escapes(text)
    # 2. Then decode URL components
    text = decode_url(text)
    # 3. Finally handle HTML entities
    text = decode_html(text)
    return text