import argparse
import sys
import base64
import binascii
import urllib.parse
import re
import codecs
import html
import time
from typing import Optional, List, Union
from concurrent.futures import ThreadPoolExecutor
import os

# Morse code dictionary for encoding/decoding
MORSE_CODE_DICT = {
    'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---',
    'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---',
    'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--',
    'Z': '--..', '1': '.----', '2': '..---', '3': '...--', '4': '....-', 
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 
    '0': '-----', ',': '--..--', '.': '.-.-.-', '?': '..--..', '/': '-..-.', 
    '-': '-....-', '(': '-.--.', ')': '-.--.-', ' ': '/'
}

# Caching for URL decoding
from functools import lru_cache

@lru_cache(maxsize=2048)
def _cached_url_decode(text: str) -> str:
    return urllib.parse.unquote(text)

class stringshift:
    @staticmethod
    def morse_encode(text: str) -> str:
        return ' '.join(MORSE_CODE_DICT.get(c.upper(), '') for c in text)

    @staticmethod
    def morse_decode(morse_code: str) -> str:
        reversed_dict = {v: k for k, v in MORSE_CODE_DICT.items()}
        return ''.join(reversed_dict.get(code, '') for code in morse_code.split())

    @staticmethod
    def rot13(text: str) -> str:
        return codecs.encode(text, 'rot_13')

    @staticmethod
    def encode(text: str, fmt: str) -> str:
        fmt = fmt.lower()
        if fmt == "base64":
            return base64.b64encode(text.encode()).decode()
        elif fmt == "hex":
            return text.encode().hex()
        elif fmt == "url":
            return urllib.parse.quote(text)
        elif fmt == "base32":
            return base64.b32encode(text.encode()).decode()
        elif fmt == "rot13":
            return stringshift.rot13(text)
        elif fmt == "binary":
            return ' '.join(format(ord(c), '08b') for c in text)
        elif fmt == "html":
            return html.escape(text)
        elif fmt == "morse":
            return stringshift.morse_encode(text)
        else:
            raise ValueError(f"Unsupported encode format: {fmt}")

    @staticmethod
    def decode(text: str, fmt: str) -> str:
        fmt = fmt.lower()
        if fmt == "base64":
            try:
                return base64.b64decode(text).decode()
            except Exception as e:
                raise ValueError(f"Base64 decode error: {e}")
        elif fmt == "hex":
            try:
                return bytes.fromhex(text).decode()
            except Exception as e:
                raise ValueError(f"Hex decode error: {e}")
        elif fmt == "url":
            if len(text) > 4096:  # Bypass cache for large texts
                return urllib.parse.unquote(text)
            return _cached_url_decode(text)
        elif fmt == "base32":
            try:
                return base64.b32decode(text).decode()
            except Exception as e:
                raise ValueError(f"Base32 decode error: {e}")
        elif fmt == "rot13":
            return stringshift.rot13(text)
        elif fmt == "binary":
            try:
                return ''.join(chr(int(b, 2)) for b in text.split())
            except Exception as e:
                raise ValueError(f"Binary decode error: {e}")
        elif fmt == "html":
            return html.unescape(text)
        elif fmt == "morse":
            return stringshift.morse_decode(text)
        else:
            raise ValueError(f"Unsupported decode format: {fmt}")

    @staticmethod
    def detect_format(text: str) -> str:
        text = text.strip()

        base64_pattern = re.compile(r'^[A-Za-z0-9+/]+={0,2}$')
        hex_pattern = re.compile(r'^[0-9a-fA-F]+$')
        binary_pattern = re.compile(r'^[01\s]+$')
        url_encoded_pattern = re.compile(r'%[0-9a-fA-F]{2}')
        morse_pattern = re.compile(r'^[.\- /]+$')
        
        if base64_pattern.match(text) and len(text) % 4 == 0:
            return "base64"
        elif hex_pattern.match(text) and len(text) % 2 == 0:
            return "hex"
        elif binary_pattern.match(text):
            return "binary"
        elif url_encoded_pattern.search(text):
            return "url"
        elif morse_pattern.match(text):
            return "morse"
        return ""

    @staticmethod
    def batch_process(texts: List[str], operation: str = "decode", fmt: str = None, workers: int = None) -> List[str]:
        """Process multiple texts in parallel"""
        workers = workers or min(32, (os.cpu_count() or 1) + 4)
        with ThreadPoolExecutor(max_workers=workers) as executor:
            if operation == "encode":
                return list(executor.map(lambda t: stringshift.encode(t, fmt), texts))
            else:
                if fmt is None:
                    return list(executor.map(lambda t: stringshift.decode(t, stringshift.detect_format(t) or "url"), texts))
                return list(executor.map(lambda t: stringshift.decode(t, fmt), texts))

def configure_parser() -> argparse.ArgumentParser:
    """Build the argument parser with enhanced options"""
    parser = argparse.ArgumentParser(
        prog='stringshift',
        description='Advanced Text Encoding/Decoding Toolkit',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''Examples:
  Basic encode:    stringshift "Hello" -e base64
  Auto decode:     stringshift "SGVsbG8="
  Batch mode:      cat inputs.txt | stringshift --batch
  Parallel:        stringshift -i file.txt --workers 4'''
    )

    # Input options
    input_group = parser.add_argument_group('Input')
    input_mx = input_group.add_mutually_exclusive_group(required=False)
    input_mx.add_argument('input', nargs='?', help='Text to process')
    input_mx.add_argument('-i', '--input-file', help='Read from file')
    input_mx.add_argument('-b', '--batch', action='store_true', 
                         help='Process multiple lines from stdin')

    # Processing modes
    mode_group = parser.add_argument_group('Processing')
    mode_mx = mode_group.add_mutually_exclusive_group()
    mode_mx.add_argument('-e', '--encode', 
                        choices=["base64", "base32", "hex", "rot13", "binary", "url", "html", "morse"],
                        help='Encoding format')
    mode_mx.add_argument('-d', '--decode', 
                        choices=["base64", "base32", "hex", "rot13", "binary", "url", "html", "morse"],
                        help='Decoding format')

    # Advanced options
    adv_group = parser.add_argument_group('Advanced')
    adv_group.add_argument('--workers', type=int, default=0,
                         help='Parallel threads (0=auto)')
    adv_group.add_argument('--benchmark', action='store_true',
                         help='Show processing time')

    # Metadata
    parser.add_argument('-v', '--version', action='store_true',
                      help='Show version and exit')

    return parser

def interactive_mode():
    """Enhanced interactive mode with new features"""
    print("Interactive mode. Type 'exit' or 'quit' to leave.")
    print("Commands: encode|decode <format> <text>")
    print("Formats: base64, base32, hex, rot13, binary, url, html, morse\n")
    print("New: Use 'batch <encode|decode> <format>' for multiple lines")

    while True:
        try:
            inp = input("stringshift> ").strip()
            if inp.lower() in {"exit", "quit"}:
                print("Goodbye!")
                break
            if not inp:
                continue

            if inp.startswith("batch"):
                parts = inp.split(maxsplit=2)
                if len(parts) < 3:
                    print("Usage: batch <encode|decode> <format>")
                    continue
                _, cmd, fmt = parts
                print("Enter multiple lines (end with Ctrl+D):")
                texts = sys.stdin.read().splitlines()
                results = stringshift.batch_process(
                    [t for t in texts if t.strip()],
                    operation=cmd,
                    fmt=fmt
                )
                print('\n'.join(results))
                break

            parts = inp.split(maxsplit=2)
            if len(parts) < 3:
                print("Usage: encode|decode <format> <text>")
                continue

            cmd, fmt, text = parts
            cmd = cmd.lower()
            fmt = fmt.lower()

            if cmd == "encode":
                print(stringshift.encode(text, fmt))
            elif cmd == "decode":
                print(stringshift.decode(text, fmt))
            else:
                print("Unknown command. Use 'encode' or 'decode'.")
        except Exception as e:
            print(f"Error: {e}")

def main(args=None):
    """Enhanced main function with new features"""
    start_time = time.perf_counter()
    parser = configure_parser()
    
    if args is None:
        args = sys.argv[1:]

    parsed = parser.parse_args(args)

    if parsed.version:
        print("stringshift version 2.0")
        return

    if not any([parsed.input, parsed.input_file, parsed.batch]):
        interactive_mode()
        return

    try:
        # Input handling
        if parsed.input_file:
            with open(parsed.input_file, 'r') as f:
                input_data = f.read()
        elif parsed.batch:
            input_data = sys.stdin.read()
        else:
            input_data = parsed.input

        # Benchmarking
        if parsed.benchmark:
            print(f"Processing {len(input_data)} characters...", file=sys.stderr)

        # Processing
        if parsed.batch:
            texts = [line.strip() for line in input_data.splitlines() if line.strip()]
            results = stringshift.batch_process(
                texts,
                operation="encode" if parsed.encode else "decode",
                fmt=parsed.encode or parsed.decode,
                workers=parsed.workers if parsed.workers > 0 else None
            )
            print('\n'.join(results))
        else:
            if parsed.encode:
                result = stringshift.encode(input_data, parsed.encode)
            elif parsed.decode:
                result = stringshift.decode(input_data, parsed.decode)
            else:
                # Auto-detect
                fmt = stringshift.detect_format(input_data)
                if fmt:
                    result = stringshift.decode(input_data, fmt)
                else:
                    print("Unable to detect format and no encode/decode option specified.", file=sys.stderr)
                    sys.exit(1)
            print(result)

        if parsed.benchmark:
            elapsed = (time.perf_counter() - start_time) * 1000
            print(f"\nProcessed in {elapsed:.2f}ms", file=sys.stderr)

    except KeyboardInterrupt:
        print("\nOperation cancelled", file=sys.stderr)
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()