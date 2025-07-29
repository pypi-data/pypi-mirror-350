from .data import fruit_data

def search_by_color(color):
    return [name for name, info in fruit_data.items() if info["color"].lower() == color.lower()]
