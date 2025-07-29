import argparse
from .data import get_fruit_info
from .search import search_by_color

def main():
    parser = argparse.ArgumentParser(description="Fruitpedia CLI")
    parser.add_argument("--info", help="Get info about a fruit")
    parser.add_argument("--search-color", help="Search fruits by color")
    args = parser.parse_args()

    if args.info:
        print(get_fruit_info(args.info))
    elif args.search_color:
        print(search_by_color(args.search_color))
