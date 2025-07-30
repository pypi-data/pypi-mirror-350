#!/usr/bin/env python3

import argparse
import sys
from .searcher import TorSearcher

def display_results(results, query):
    """Display search results in a formatted way."""
    if results:
        print(f"\nSearch results for: '{query}'\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   {result['link']}")
            if 'snippet' in result and result['snippet']:
                print(f"   {result['snippet']}")
            print()
        return True
    else:
        print("No results found or error occurred.")
        return False

def main():
    """Main function for CLI usage."""
    parser = argparse.ArgumentParser(description="Search the web anonymously through the Tor network")
    parser.add_argument("query", help="Search query")
    parser.add_argument("-n", "--num", type=int, default=10, 
                        help="Number of search results (default: 10)")
    parser.add_argument("-e", "--engine", choices=["google", "duckduckgo", "yandex"], default="duckduckgo",
                        help="Search engine to use (default: duckduckgo)")
    
    args = parser.parse_args()
    
    # Create searcher, search once, then disconnect
    searcher = TorSearcher()
    try:
        results = searcher.search(args.query, args.num, args.engine)
        display_results(results, args.query)
    finally:
        searcher.disconnect()

if __name__ == "__main__":
    main()