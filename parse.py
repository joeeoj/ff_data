import json
import pathlib

import pendulum

from config import DATA_DIR


DT_FMT = 'dddd MMMM D, YYYY at H:mm A'
LOCAL_TZ = "America/Los_Angeles"
TOTAL_FAAB = 100
POSITION_MAP = {
    0: 'QB',
    2: 'RB',
    4: 'WR',
    6: 'TE',
    16: 'D/ST',
    17: 'K',
    20: 'BE',
    21: 'IR',
    23: 'FLEX',
}


def load_json(fname: pathlib.PosixPath) -> dict:
    with open(DATA_DIR / fname) as f:
        data = json.load(f)
    return data


def parse_ts(ts: int, iso_format: bool = True) -> str:
    dt = pendulum.from_timestamp(ts / 1_000).in_timezone(LOCAL_TZ)
    return dt.isoformat() if iso_format else dt.format(DT_FMT)


def parse_members(members: dict) -> dict:
    # team id -> manager name
    lookup = {}
    for m in members:
        lookup[m['id']] = {
            'first_name': m['firstName'],
            'last_name': m['lastName'],
            'full_name': ' '.join([m['firstName'], m['lastName']]),
        }
    return lookup


def parse_teams(teams: list[dict], manager_lookup: dict) -> list[dict]:
    results = []
    for team in teams:
        for manager_id in team['owners']:
            results.append({
                'team_id': team['id'],
                'team_abbrev': team['abbrev'],
                'team_name': ' '.join([team['location'], team['nickname']]),
                'manager_id': manager_id,
                'manager_first_name': manager_lookup.get(manager_id).get('first_name'),
                'manager_last_name': manager_lookup.get(manager_id).get('last_name'),

                'draft_day_projected_rank': team['draftDayProjectedRank'],
                'current_projected_rank': team['currentProjectedRank'],
                'playoff_seed': team['playoffSeed'],
                'points_for': team['record']['overall']['pointsFor'],
                'points_against': team['record']['overall']['pointsAgainst'],
                'wins': team['record']['overall']['wins'],
                'losses': team['record']['overall']['losses'],
                'ties': team['record']['overall']['ties'],
                'games_back': team['record']['overall']['gamesBack'],

                'waiver_rank': team['waiverRank'],
                'faab_remaining': TOTAL_FAAB - team['transactionCounter']['acquisitionBudgetSpent'],
                'acquisitions': team['transactionCounter']['acquisitions'],
                'drops': team['transactionCounter']['drops'],
                'move_to_active': team['transactionCounter']['moveToActive'],
                'move_to_ir': team['transactionCounter']['moveToIR'],
                'trades': team['transactionCounter']['trades'],
            })
    return results


def parse_transactions(data: dict, weeks: list[str], team_lookup: dict, manager_lookup: dict) -> list[dict]:
    transactions = []
    for week in weeks:
        for txn in data[week]['transactions']:
            if txn['type'] == 'DRAFT' or 'items' not in txn.keys():  # skip for now
                continue

            for item in txn['items']:
                transactions.append({
                    'txn_id': txn['id'],
                    'related_txn_id': txn.get('relatedTransactionId'),
                    'week': txn['scoringPeriodId'],
                    'type': txn['type'],
                    'status': txn['status'],
                    'bid_amount': txn['bidAmount'],
                    'waiver_order': txn['subOrder'],
                    # 'manager_name': manager_lookup.get(txn.get('memberId'), {}).get('full_name'),
                    'team_name': team_lookup.get(txn.get('teamId'), {}).get('team_name'),
                    'team_abbrev': team_lookup.get(txn.get('teamId'), {}).get('team_abbrev'),
                    'proposed_date': parse_ts(txn['proposedDate']),
                    'expiration_date': parse_ts(txn.get('expirationDate')) if txn.get('expirationDate') else None,

                    'move_type': item['type'],
                    'player_name': player_lookup.get(item['playerId']),
                    'from_team': team_lookup.get(item.get('fromTeamId'), {}).get('team_name'),
                    'to_team': team_lookup.get(item.get('toTeamId'), {}).get('team_name'),
                    'from_slot': POSITION_MAP.get(item.get('fromLineupSlotId')),
                    'to_slot': POSITION_MAP.get(item.get('toLineupSlotId')),
                })
    return transactions


if __name__ == '__main__':
    data = load_json(DATA_DIR / 'data.json')
    player_lookup = {int(k): v for k,v in load_json('player_lookup.json').items()}  # str -> int
    weeks = list(data.keys())

    # data is always current so we can use the first week (or any week)
    manager_lookup = parse_members(data['1']['members'])
    manager_lookup['NightlyLeagueUpdateTaskProcessor'] = {'full_name': 'Nightly Task Processor'}
    manager_lookup['TradeTaskProcessor'] = {'full_name': 'Trade Task Processor'}

    # same can use the first week
    teams = parse_teams(data['1']['teams'], manager_lookup)

    team_lookup = {}
    for t in teams:
        team_lookup[t['team_id']] = {
            'team_name': t['team_name'],
            'team_abbrev': t['team_abbrev']
        }

    transactions = parse_transactions(data, weeks, team_lookup, manager_lookup)

    with open(DATA_DIR / 'transactions.json', 'wt') as f:
        json.dump(transactions, f, indent=2)

    status = data[weeks[-1]]['status']
    waiver_last_execution_local = parse_ts(status['waiverLastExecutionDate'], iso_format=False)
    print(f'Waivers last processed: {waiver_last_execution_local}')
