CREATE TABLE IF NOT EXISTS teams (
    id INTEGER PRIMARY KEY,
    team_id INTEGER,
    team_abbrev VARCHAR(4),
    team_name VARCHAR(100),
    manager_id VARCHAR(40),
    manager_first_name VARCHAR(20),
    manager_last_name VARCHAR(20),
    draft_day_projected_rank INTEGER,
    current_projected_rank INTEGER,
    playoff_seed INTEGER,
    points_for FLOAT,
    points_against FLOAT,
    wins INTEGER,
    losses INTEGER,
    ties INTEGER,
    games_back FLOAT,
    waiver_rank INTEGER,
    faab_remaining INTEGER,
    acquisitions INTEGER,
    drops INTEGER,
    move_to_active INTEGER,
    move_to_ir INTEGER,
    trades INTEGER
);

CREATE TABLE IF NOT EXISTS bye_weeks (
    id INTEGER PRIMARY KEY,
    pro_team VARCHAR(3),
    bye_week INTEGER
);

CREATE TABLE IF NOT EXISTS rosters (
    id INTEGER PRIMARY KEY,
    team_abbrev VARCHAR(4),
    team_name VARCHAR(100),
    player_name VARCHAR(50),
    position VARCHAR(4),
    acquisition_type VARCHAR(10),
    pro_team VARCHAR(3),
    injured BOOLEAN,
    projected_total_points FLOAT,
    total_points FLOAT,

    FOREIGN KEY(team_abbrev) REFERENCES teams(team_abbrev),
    FOREIGN KEY(pro_team) REFERENCES bye_weeks(pro_team)
);

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY,
    week INTEGER NOT NULL,
    home_team VARCHAR(100),
    home_score FLOAT,
    away_team VARCHAR(100),
    away_score FLOAT
);

CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY,
    txn_id VARCHAR(36),
    related_txn_id VARCHAR(36),
    week INTEGER,
    type VARCHAR(20),
    status VARCHAR(20),
    bid_amount INTEGER,
    waiver_order INTEGER,
    team_name VARCHAR(100),
    team_abbrev VARCHAR(4),
    proposed_date DATETIME,
    expiration_date DATETIME,
    move_type VARCHAR(20),
    player_name VARCHAR(50),
    from_team VARCHAR(100),
    to_team VARCHAR(100),
    from_slot VARCHAR(4),
    to_slot VARCHAR(4),

    FOREIGN KEY(team_abbrev) REFERENCES teams(team_abbrev)
);

CREATE INDEX IF NOT EXISTS team_abbrev_idx ON transactions(team_abbrev);
CREATE INDEX IF NOT EXISTS team_name_idx ON transactions(team_name);
CREATE INDEX IF NOT EXISTS proposed_date_idx ON transactions(proposed_date);
