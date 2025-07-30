import pytest
from bref_scraper.players import (
    get_last_5_games,
    get_playoff_series_stats,
    get_playoff_game_log,
)

# Use known NBA player IDs (LeBron, Curry, Durant)
PLAYER_IDS = ["jamesle01", "curryst01", "duranke01"]


@pytest.mark.parametrize("player_id", PLAYER_IDS)
def test_get_last_5_games(player_id):
    games = get_last_5_games(player_id)
    assert isinstance(games, list)
    assert len(games) <= 5
    for game in games:
        assert "date" in game
        assert "pts" in game
        assert game["pts"].isdigit() or game["pts"] == ""


@pytest.mark.parametrize("player_id", PLAYER_IDS)
def test_get_playoff_series_stats(player_id):
    stats = get_playoff_series_stats(player_id)
    assert isinstance(stats, list)
    if stats:  # Some players may not have playoff data
        for series in stats:
            assert "year_id" in series
            assert "pts_per_g" in series


@pytest.mark.parametrize("player_id,year", [
    ("curryst01", 2022),
    ("duranke01", 2021),
    ("jamesle01", 2020)
])
def test_get_playoff_game_log(player_id, year):
    logs = get_playoff_game_log(player_id, year)
    assert isinstance(logs, list)
    for game in logs:
        assert "date" in game
        assert "pts" in game
        assert "game_result" in game
