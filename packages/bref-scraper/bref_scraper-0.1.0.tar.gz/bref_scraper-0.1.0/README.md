# bref-scraper

**bref-scraper** is a Python package for scraping structured NBA data from [Basketball Reference](https://basketball-reference.com/). It provides tools to retrieve player game logs, playoff statistics, and team rosters programmatically using `requests` and `BeautifulSoup`.

---

## 🚀 Features

- ✅ Fetch last 5 games for any NBA player
- ✅ Extract full team rosters for a given year
- ✅ Retrieve playoff **series stats** per player (all years)
- ✅ Pull detailed **playoff game logs** by year
- ✅ Handles dynamic tables embedded in comments (e.g., `#all_playoffs_series`)
- ✅ Cleans and formats HTML tables into structured Python dictionaries
- ✅ Output is pandas-friendly (`list[dict]`)

---

## 📦 Installation

```bash
pip install bref-scraper
```

---

## 🧠 Quick Usage

```python
from bref_scraper.players import get_last_5_games
import pandas as pd

games = get_last_5_games("jamesle01")  # LeBron James
df = pd.DataFrame(games)
print(df[["date", "pts", "ast", "trb"]])
```

---

## 📘 API Reference

### 🏀 players.py

#### get_last_5_games(player_id: str) -> list
Returns the last 5 regular season games for a player as a list of dicts.

#### get_playoff_series_stats(player_id: str) -> list
Returns per-series playoff stats for all available years.

#### get_playoff_game_log(player_id: str, year: int) -> list
Returns per-game playoff stats for a given year.

---

### 🏀 teams.py

#### get_roster(team_abbr: str, year: int) -> list
Returns the full roster of a team for a given season, including player IDs.

---

## 🧪 Running Tests

```bash
pytest
```

---

## 📜 License

MIT License © 2025 [Jithen Shriyan](https://github.com/jithenms)
