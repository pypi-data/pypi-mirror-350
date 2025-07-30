from festivus import FestivalFinder

def test_month_filter():
    f = FestivalFinder()
    results = f.get_by_month(2025, 8)
    assert any(r['name'] == "Independence Day" for r in results)
