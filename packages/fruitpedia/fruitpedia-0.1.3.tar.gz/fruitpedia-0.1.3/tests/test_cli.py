import subprocess
import sys
import json
import csv
import os
import tempfile
import pytest

# Unified CLI call wrapper with UTF-8 decoding and error handling
def run_cli(args):
    result = subprocess.run(
        [sys.executable, "-m", "fruitpedia.cli"] + args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
        errors="replace",  # Ensures emojis don't crash on Windows
        text=True
    )
    return result

def test_fruit_info_found():
    result = run_cli(["--info", "apple"])
    assert result.returncode == 0
    assert result.stdout and "🍎 Fruit Information:" in result.stdout
    assert "Color: Red" in result.stdout
    assert "Taste: Sweet" in result.stdout
    assert "Nutrients: fiber, vitamin C" in result.stdout

def test_fruit_info_not_found():
    result = run_cli(["--info", "unknownfruit"])
    assert result.returncode == 0
    assert "❌ Fruit not found." in result.stdout

def test_search_by_color():
    result = run_cli(["--search-color", "red"])
    assert result.returncode == 0
    assert result.stdout and "🎨 Fruits with color" in result.stdout
    assert "- apple" in result.stdout.lower()  # case insensitive

def test_list_colors():
    result = run_cli(["--list-colors"])
    assert result.returncode == 0
    assert result.stdout and "🎨 Available Fruit Colors:" in result.stdout

def test_export_json():
    output_file = os.path.join(os.getcwd(), "apple_output.json")
    if os.path.exists(output_file):
        os.remove(output_file)

    result = run_cli(["--info", "apple", "--export", "json"])
    assert result.returncode == 0
    assert os.path.exists(output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        assert isinstance(data, dict)
        assert data["name"].lower() == "apple"

    os.remove(output_file)

def test_export_csv():
    output_file = os.path.join(os.getcwd(), "red_output.csv")
    if os.path.exists(output_file):
        os.remove(output_file)

    result = run_cli(["--search-color", "red", "--export", "csv"])
    assert result.returncode == 0
    assert os.path.exists(output_file)

    with open(output_file, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) > 0
        assert "name" in rows[0]

    os.remove(output_file)
