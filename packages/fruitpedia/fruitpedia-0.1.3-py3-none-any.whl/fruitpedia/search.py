from .data import fruit_data

def search_by_color(color):
    return [name for name, info in fruit_data.items() if info["color"].lower() == color.lower()]

def list_all_colors():
    return sorted(set(info["color"].lower() for info in fruit_data.values()))
