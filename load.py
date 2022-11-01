import csv
import json
import pathlib
import sqlite3

from config import DATA_DIR


def load_json(fname: pathlib.PosixPath) -> list[dict]:
    with open(fname) as f:
        data = json.load(f)
    return data


def load_csv(fname: pathlib.PosixPath) -> list[dict]:
    with open(fname) as f:
        csvreader = csv.DictReader(f)
        data = [row for row in csvreader]
    return data


def create_insert_statement(table_name: str, data: list[dict]) -> str:
    columns = ','.join(data[0].keys())
    placeholders = ','.join('?' * len(data[0].keys()))
    return f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'


def insert_data(table_name: str, data: list[dict], conn: sqlite3.Connection, cursor: sqlite3.Cursor) -> None:
    query = create_insert_statement(table_name, data)
    cursor.executemany(query, [tuple(row.values()) for row in data])
    conn.commit()


if __name__ == '__main__':
    conn = sqlite3.connect('football.db')
    cursor = conn.cursor()

    teams = load_json(DATA_DIR / 'teams.json')
    insert_data('teams', teams, conn, cursor)

    schedules = load_json(DATA_DIR / 'schedules.json')
    insert_data('schedules', schedules, conn, cursor)

    rosters = load_json(DATA_DIR / 'rosters.json')
    insert_data('rosters', rosters, conn, cursor)

    bye_weeks = load_csv(DATA_DIR / 'bye_weeks.csv')
    insert_data('bye_weeks', bye_weeks, conn, cursor)

    scores = load_json(DATA_DIR / 'scores.json')
    insert_data('scores', scores, conn, cursor)

    transactions = load_json(DATA_DIR / 'transactions.json')
    insert_data('transactions', transactions, conn, cursor)
