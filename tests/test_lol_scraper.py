import pytest
from requests_html import HTML

from lol_scrapers.request.strategies import champion, tft_items, synergies
from lol_scrapers.utils.processor import ChampionNameProcessor


@pytest.mark.parametrize("champion_name,expected", [
    (("Kassadin",), "kassadin"),
    (("Kai'sa",), "kaisa"),
    (("",), None),
    (("Tahm", "Kench"), "tahmkench"),
    (("wukong",), "monkeyking"),
    (("Nunu", "&", "Willump"), "nunu")
])
def test_refactor_name(champion_name, expected):
    _, _, name = ChampionNameProcessor(champion_name).process()
    assert name == expected


@pytest.mark.parametrize("strategy, expected", [
    (tft_items.TftItemsStrategy(), (True, HTML)),
    (synergies.SynergyStrategy(), (True, HTML)),
])
def test_request(lol_request, strategy, expected):
    isvalid_expected, expected_type = expected
    isvalid, html = lol_request.request(strategy)
    assert isvalid == isvalid_expected
    assert isinstance(html, expected_type)


@pytest.mark.parametrize("champion_tokens, expected", [
    (("mid", "kassadin"), (True, HTML)),
    (("Kai'sa",), (True, HTML)),
    (("", ""), (False, type(None))),
    (("Tahm", "Kench"), (True, HTML)),
    (("mid", "Wuk0ng"), (False, type(None))),
    (("Nunu", "&", "Willump"), (True, HTML)),
    (("", "Nunu", "&", "Willump"), (False, type(None))),
])
def test_champion_request(champion_tokens, expected, lol_request):
    isvalid_expected, expected_type = expected
    isvalid, html = lol_request.request(champion.ChampionStrategy(champion_tokens))
    assert isvalid == isvalid_expected
    assert isinstance(html, expected_type)
