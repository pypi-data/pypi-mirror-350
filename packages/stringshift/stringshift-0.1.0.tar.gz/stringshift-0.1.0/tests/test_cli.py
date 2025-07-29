import argparse
from stringshift.core import decode_all  # Replace 'stringshift' with your package name

def main():
    parser = argparse.ArgumentParser(description="Decode encoded text")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("text", nargs="?", help="Text to decode")
    group.add_argument("--version", action="store_true", help="Show version")
    
    args = parser.parse_args()
    
    if args.version:
        from stringshift import __version__
        print(__version__)
    else:
        print(decode_all(args.text))

if __name__ == "__main__":
    main()