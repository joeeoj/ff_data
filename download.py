import json

from espn_api.football import League
import pendulum
import requests

from config import LEAGUE_ID, YEAR, ESPN_S2, SWID, DATA_DIR


COOKIES = { "espn_s2": ESPN_S2, "SWID": SWID }
PARAMS = {
    "scoringPeriodId": 1,
    "view": ["mDraftDetail", "mStatus", "mSettings", "mTeam", "mTransactions2", "modular", "mNav"],
}
URL = f'https://fantasy.espn.com/apis/v3/games/ffl/seasons/{YEAR}/segments/0/leagues/{LEAGUE_ID}?'


def download_data(week: int) -> dict:
    """This gets more transaction data than the espn api object"""
    params = PARAMS.copy()
    params['scoringPeriodId'] = week
    r = requests.get(URL, cookies=COOKIES, params=params)
    return r.json()


if __name__ == '__main__':
    league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)
    player_lookup = {k: v for k,v in league.player_map.items() if isinstance(k, int)}

    rosters, schedules = [], []
    for team in league.teams:  # always the current roster
        for week, opponent in enumerate(team.schedule, start=1):
            schedules.append({
                'week': week,
                'team_abbrev': team.team_abbrev,
                'team_name': team.team_name,
                'opponent_abbrev': opponent.team_abbrev,
                'opponent_name': opponent.team_name,
            })

        for player in team.roster:
            rosters.append({
                'team_abbrev': team.team_abbrev,
                'team_name': team.team_name,
                'player_name': player.name,
                'position': player.position,
                'acquisition_type': player.acquisitionType,
                'pro_team': player.proTeam,
                'injured': player.injured,
                'projected_total_points': player.projected_total_points,
                'total_points': player.total_points,
            })

    with open(DATA_DIR / 'schedules.json', 'wt') as f:
        json.dump(schedules, f, indent=2)

    with open(DATA_DIR / 'rosters.json', 'wt') as f:
        json.dump(rosters, f, indent=2)

    data = {}  # data saved by week, mainly for txns
    for week in range(1, league.current_week + 1):
        data[week] = download_data(week)

    with open(DATA_DIR / 'data.json', 'wt') as f:
        json.dump(data, f, indent=2)

    with open(DATA_DIR / 'player_lookup.json', 'wt') as f:
        json.dump(player_lookup, f, indent=2)

    # don't advance for scores if Tue or Wed
    current_week = league.current_week - 1 if pendulum.now().day_of_week in (2, 3) else league.current_week

    scores = []
    for week in range(1, current_week + 1):
        for bs in league.box_scores(week=week):
            scores.append({
                'week': week,
                'home_team': bs.home_team.team_name,
                'home_score': bs.home_score,
                'away_team': bs.away_team.team_name,
                'away_score': bs.away_score,
            })

    with open(DATA_DIR / 'scores.json', 'wt') as f:
        json.dump(scores, f, indent=2)
