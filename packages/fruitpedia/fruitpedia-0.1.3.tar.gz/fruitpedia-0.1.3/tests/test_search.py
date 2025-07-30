from fruitpedia.search import search_by_color

def test_search_by_color():
    assert "Banana" in search_by_color("Yellow")

