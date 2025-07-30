import argparse
import sys
from . import __version__
from .core import Garlic

def main():
    parser = argparse.ArgumentParser(
        description='Garlic - A RAG-based company information retrieval system'
    )
    parser.add_argument(
        '--version', 
        action='version', 
        version=f'startgarlic {__version__}'
    )
    parser.add_argument(
        '--query', 
        type=str, 
        help='Query to process'
    )

    args = parser.parse_args()

    if args.query:
        try:
            garlic = Garlic()
            response = garlic.generate_response(args.query)
            print(response)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main() 