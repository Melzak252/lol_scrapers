import pytest
from requests_html import HTML

from lol_scrapers.request.strategies import champion, tft_items, synergies


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


@pytest.mark.parametrize("strategy, expected", [
    (champion.ChampionStrategy(), (False, type(None))),
    (tft_items.TftItemsStrategy(), (True, HTML)),
    (synergies.SynergyStrategy(), (True, HTML)),
])
def test_request(lol_request, strategy, expected):
    isvalid_expected, expected_type = expected
    isvalid, html = lol_request.request(strategy)
    assert isvalid == isvalid_expected
    assert isinstance(html, expected_type)


@pytest.mark.parametrize("role, champion_tokens, expected", [
    ("mid", "kassadin", (True, HTML)),
    ("Kai'sa", "", (True, HTML)),
    ("", "", (False, type(None))),
    ("Tahm", ("Kench",), (True, HTML)),
    ("Tahm", "Kench", (True, HTML)),
    ("Nunu", ("&", "Willump"), (True, HTML)),
    ("", ("Nunu", "&", "Willump"), (False, type(None)))
])
def test_champion_request(role, champion_tokens, expected, lol_request):
    isvalid_expected, expected_type = expected
    isvalid, html = lol_request.request(champion.ChampionStrategy(), role=role, champion=champion_tokens)
    assert isvalid == isvalid_expected
    assert isinstance(html, expected_type)
