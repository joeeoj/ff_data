"""Separate from the download file because it takes a few minutes (though not too slow futures)"""
import json
import concurrent.futures

from espn_api.football import League

from config import LEAGUE_ID, YEAR, ESPN_S2, SWID, DATA_DIR


def get_player_info(player_name: str, player_id: int) -> dict:
    p = league.player_info(player_name)

    if p is not None:
        return {
            "player_id": player_id,
            "player_name": player_name,
            "position": p.position,
            "pro_team": p.proTeam,
        }
    return None


if __name__ == "__main__":
    league = League(league_id=LEAGUE_ID, year=YEAR, espn_s2=ESPN_S2, swid=SWID)

    player_names_and_ids = []
    for k, v in league.player_map.items():
        if isinstance(v, int):
            player_names_and_ids.append((k, v))

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        future_player = {executor.submit(get_player_info, *p) for p in player_names_and_ids}
        for future in concurrent.futures.as_completed(future_player):
            try:
                data = future.result()
                results.append(data)
            except Exception as exc:
                print("Exception: %s" % exc)

    results = [d for d in results if d is not None]
    print(len(results))

    with open(DATA_DIR / "players.json", "wt") as f:
        json.dump(results, f, indent=2)
