# -*- coding: utf-8 -*-
import argparse
import json
import csv
import os
from difflib import get_close_matches
import click
from .data import get_fruit_info, fruit_data
from .search import search_by_color, list_all_colors
import sys
import io

# Ensure stdout is UTF-8 on Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def format_fruit_info(info: dict, fruit_name: str) -> str:
    if not info:
        return f"❌ Fruit '{fruit_name}' not found."
    lines = [f"🍎 Fruit Information:"]  # include fruit name here
    for key, value in info.items():
        formatted_value = ', '.join(value) if isinstance(value, list) else value
        lines.append(f"  {key.capitalize()}: {formatted_value}")
    return '\n'.join(lines)

def format_fruit_list(fruits: list, color: str) -> str:
    if not fruits:
        return f"❌ No fruits found with color: {color}"
    header = f"🎨 Fruits with color '{color.capitalize()}':"
    fruit_list = '\n'.join([f"  - {fruit}" for fruit in sorted(fruits)])
    return f"{header}\n{fruit_list}"

def format_color_list(colors: list) -> str:
    header = "🎨 Available Fruit Colors:"
    color_list = '\n'.join(f"  - {color}" for color in sorted(colors))
    return f"{header}\n{color_list}"

def export_data(data, filename, fmt):
    if fmt == "json":
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    elif fmt == "csv":
        if isinstance(data, dict):
            data = [data]
        with open(filename, "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    print(f"✅ Exported to {filename}")

@click.command()
@click.option("--info", help="🔍 Get detailed info about a fruit")
@click.option("--search-color", help="🎨 List fruits by color")
@click.option("--list-colors", is_flag=True, help="📋 List all available fruit colors")
@click.option("--export", type=click.Choice(["json", "csv"]), help="💾 Export result to JSON or CSV")
def cli(info, search_color, list_colors, export):
    """🍉 Fruitpedia CLI using Click"""
    result_data = None

    if info:
        fruit_name = info
        data = get_fruit_info(fruit_name)
        if isinstance(data, dict) and data:
            print(format_fruit_info(data, fruit_name))
            result_data = {**{"name": fruit_name}, **data}
        else:
            suggestion = get_close_matches(fruit_name, fruit_data.keys(), n=1)
            print("❌ Fruit not found.")
            if suggestion:
                print(f"🔎 Did you mean: {suggestion[0]}?")
            # Exit gracefully with code 0 for tests
            #raise click.Exit(0)
            return

    elif search_color:
        fruits = search_by_color(search_color)
        print(format_fruit_list(fruits, search_color))
        result_data = [{"name": fruit, "color": search_color} for fruit in fruits]

    elif list_colors:
        colors = list_all_colors()
        print(format_color_list(colors))
        result_data = [{"color": color} for color in colors]

    else:
        print("❗ No command provided. Use --help for usage.")
        raise click.Exit(0)

    if export and result_data:
        filename = f"{info or search_color or 'fruitpedia'}_output.{export}"
        export_data(result_data, filename, export)

def main():
    parser = argparse.ArgumentParser(
        description="🍉 Fruitpedia CLI - Explore fruits by name, color, or export"
    )
    parser.add_argument("--info", help="🔍 Get detailed info about a fruit")
    parser.add_argument("--search-color", help="🎨 List fruits by color")
    parser.add_argument("--list-colors", action="store_true", help="📋 List all available fruit colors")
    parser.add_argument("--export", choices=["json", "csv"], help="💾 Export result to JSON or CSV")
    args = parser.parse_args()

    import sys
    args_list = []
    if args.info:
        args_list += ["--info", args.info]
    if args.search_color:
        args_list += ["--search-color", args.search_color]
    if args.list_colors:
        args_list.append("--list-colors")
    if args.export:
        args_list += ["--export", args.export]

    cli.main(args=args_list, standalone_mode=False)

if __name__ == "__main__":
    cli()
    # main()
