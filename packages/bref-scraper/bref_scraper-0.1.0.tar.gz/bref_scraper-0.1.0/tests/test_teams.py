import pytest
from bref_scraper.teams import get_roster

# A few valid teams and years with known public rosters
TEST_CASES = [
    ("DEN", 2023),  # Nuggets championship year
    ("BOS", 2022),
    ("MIA", 2020),  # Bubble Finals run
]


@pytest.mark.parametrize("team_abbr, year", TEST_CASES)
def test_get_roster_structure(team_abbr, year):
    roster = get_roster(team_abbr, year)
    assert isinstance(roster, list)
    assert len(roster) > 5  # Should return at least a starting 5

    for player in roster:
        assert "player" in player
        assert "player_id" in player
        assert "pos" in player
        assert "birth_date" in player
        assert player["player_id"]  # should not be empty string
