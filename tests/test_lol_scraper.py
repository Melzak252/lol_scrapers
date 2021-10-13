import pytest
from requests_html import HTML


@pytest.mark.parametrize("champion_name,expected", [
    ("Kassadin", "kassadin"),
    ("Kai'sa", "kaisa"),
    ("", ""),
    (("Tahm", "Kench"), "tahmkench"),
    ("wukong", "monkeyking"),
    (("Nunu", "&", "Willump"), "nunu")
])
def test_refactor_name(champion_name, expected, processor):
    assert processor._refactor(champion_name) == expected


@pytest.mark.parametrize("role, champion_name,expected", [
    ("mid", ("Kassadin",), (True, HTML)),
    ("Kai'sa", (), (True, HTML)),
    ("", "", (False, type(None))),
    ("Tahm", ("Kench",), (True, HTML)),
    ("wukong", (), (True, HTML)),
    ("", ("Nunu", "&", "Willump"), (False, type(None)))
])
def test_request(champion_name, expected, role, lol_request):
    isvalid_expected, html_type_expected = expected
    isvalid, html, _ = lol_request.request_champion_html(role, champion_name)
    assert isvalid_expected == isvalid
    assert isinstance(html, html_type_expected)
