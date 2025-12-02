from gellax.core import process_items


def test_process_items_basic():
    items = ["abc", "  def ", "123"]
    res = process_items(items)
    assert res == ["cba", "fed", "321"]


def test_process_items_skips_non_str():
    items = ["ok", 5, None]
    res = process_items(items)
    assert res == ["ko"]
