import requests
from bs4 import BeautifulSoup

from .constants import TEAM_ABBR
from .utils.html_helpers import safe_text_from_cell


def get_roster(team_abbr: TEAM_ABBR, year: int) -> list:
    url = f"https://www.basketball-reference.com/teams/{team_abbr}/{year}.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find(name="table", attrs={"id": "roster"})
    if not table:
        return []

    roster = []
    for row in table.find_all("tr")[1:]:
        player = {}
        player["number"] = safe_text_from_cell(row, "number")
        player["player"] = safe_text_from_cell(row, "player", is_link=True)
        player_link = row.find("td", {"data-stat": "player"})
        player_id = ""
        if player_link:
            link = player_link.find("a")
            if link and "href" in link.attrs:
                player_id = link["href"].split("/")[-1].split(".")[0]
        player["player_id"] = player_id
        player["pos"] = safe_text_from_cell(row, "pos")
        player["height"] = safe_text_from_cell(row, "height")
        player["weight"] = safe_text_from_cell(row, "weight")
        player["birth_date"] = safe_text_from_cell(row, "birth_date")
        player["years_experience"] = safe_text_from_cell(row, "years_experience")
        roster.append(player)

    return roster
