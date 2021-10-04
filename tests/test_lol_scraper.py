import pytest


@pytest.mark.parametrize("champion_name,expected", [
    ("Kassadin", "kassadin"),
    ("Kai'sa", "kaisa"),
    ("", ""),
    (("Tahm", "Kench"), "tahmkench"),
    ("wukong", "monkeyking"),
    (("Nunu", "&", "Willump"), "nunu")
])
def test_refactor_name(champion_name, expected, lol_request):
    assert lol_request._refactor_champ_name(champion_name) == expected
