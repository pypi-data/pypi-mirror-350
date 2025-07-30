import requests
from bs4 import BeautifulSoup, Comment

from .constants import TEAM_ABBR
from .utils.html_helpers import safe_text_from_cell


def get_last_5_games(player_id: str) -> list:
    url = (
        f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}.html"
    )
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", attrs={"id": "last5"})
    if table is None:
        return []

    last_5_games = []
    for row in table.find_all("tr")[1:]:
        game = {
            stat: safe_text_from_cell(row, stat)
            for stat in [
                "game_result",
                "is_starter",
                "mp",
                "fg",
                "fga",
                "fg_pct",
                "fg3",
                "fg3a",
                "fg3_pct",
                "ft",
                "fta",
                "ft_pct",
                "orb",
                "drb",
                "trb",
                "ast",
                "stl",
                "blk",
                "tov",
                "pf",
                "pts",
                "game_score",
                "plus_minus",
            ]
        }
        game["date"] = safe_text_from_cell(row, "date", is_link=True)
        game["team_name_abbr"] = safe_text_from_cell(
            row, "team_name_abbr", is_link=True
        )
        game["opp_name_abbr"] = safe_text_from_cell(row, "opp_name_abbr", is_link=True)
        last_5_games.append(game)

    return last_5_games


def get_playoff_series_stats(player_id: str) -> list:
    url = f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}.html#all_playoffs_series"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    comments = soup.find_all(string=lambda text: isinstance(text, Comment))
    table = None
    for comment in comments:
        if 'id="playoffs_series"' in comment:
            comment_soup = BeautifulSoup(comment, "html.parser")
            table = comment_soup.find("table", {"id": "playoffs_series"})
            break
    if not table:
        return []

    playoff_series_stats = []
    for row in table.find_all("tr")[1:]:
        if "class" in row.attrs and "spacer" in row["class"]:
            continue
        if not safe_text_from_cell(row, "year_id", is_link=True):
            continue

        season = {
            stat: safe_text_from_cell(row, stat)
            for stat in [
                "age",
                "series_result",
                "games",
                "mp_per_g",
                "pts_per_g",
                "trb_per_g",
                "ast_per_g",
                "stl_per_g",
                "blk_per_g",
                "fg",
                "fga",
                "fg_pct",
                "fg3",
                "fg3a",
                "fg3_pct",
                "fg2",
                "fg2a",
                "fg2_pct",
                "efg_pct",
                "ft",
                "fta",
                "ft_pct",
                "orb",
                "drb",
                "trb",
                "ast",
                "stl",
                "blk",
                "tov",
                "pf",
                "pts",
            ]
        }
        season["year_id"] = safe_text_from_cell(row, "year_id", is_link=True)
        season["team_name_abbr"] = safe_text_from_cell(
            row, "team_name_abbr", is_link=True
        )
        season["opp_name_abbr"] = safe_text_from_cell(
            row, "opp_name_abbr", is_link=True
        )
        season["round"] = safe_text_from_cell(row, "ps_round", is_link=True)

        playoff_series_stats.append(season)

    return playoff_series_stats


def get_playoff_game_log(player_id: str, year: int) -> list:
    url = f"https://www.basketball-reference.com/players/{player_id[0]}/{player_id}/gamelog/{year}/#all_player_game_log_post"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", {"id": "player_game_log_post"})
    if table is None:
        return []

    playoff_game_log = []
    for row in table.find_all("tr")[1:]:
        if "class" in row.attrs and "spacer" in row["class"]:
            continue
        starter = safe_text_from_cell(row, "is_starter")
        if starter in ["Did Not Play", "Inactive"]:
            continue
        if not safe_text_from_cell(row, "ranker"):
            continue

        game = {
            stat: safe_text_from_cell(row, stat)
            for stat in [
                "game_result",
                "is_starter",
                "mp",
                "fg",
                "fga",
                "fg_pct",
                "fg3",
                "fg3a",
                "fg3_pct",
                "ft",
                "fta",
                "ft_pct",
                "orb",
                "drb",
                "trb",
                "ast",
                "stl",
                "blk",
                "tov",
                "pf",
                "pts",
                "game_score",
                "plus_minus",
            ]
        }
        game["date"] = safe_text_from_cell(row, "date", is_link=True)
        game["team_name_abbr"] = safe_text_from_cell(
            row, "team_name_abbr", is_link=True
        )
        game["opp_name_abbr"] = safe_text_from_cell(row, "opp_name_abbr", is_link=True)
        playoff_game_log.append(game)

    return playoff_game_log
