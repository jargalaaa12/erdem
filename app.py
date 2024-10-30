from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sport_type (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sport_type TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS team (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            team_name TEXT NOT NULL,
            established_date TEXT NOT NULL,
            logo TEXT,
            sport_type_id INTEGER,
            FOREIGN KEY (sport_type_id) REFERENCES sport_type(id)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            player_name TEXT NOT NULL,
            number INTEGER NOT NULL,
            gender TEXT NOT NULL,
            date_of_birth TEXT NOT NULL,
            team_id INTEGER,
            FOREIGN KEY (team_id) REFERENCES team(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Routes to handle CRUD operations
@app.route('/sport_type', methods=['POST'])
def add_sport_type():
    data = request.get_json()
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sport_type (sport_type) VALUES (?)", (data['sport_type'],))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Sport type added!'}), 201

@app.route('/team', methods=['POST'])
def add_team():
    data = request.get_json()
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO team (team_name, established_date, logo, sport_type_id) 
        VALUES (?, ?, ?, ?)''', 
        (data['team_name'], data['established_date'], data.get('logo'), data['sport_type_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Team added!'}), 201

@app.route('/player', methods=['POST'])
def add_player():
    data = request.get_json()
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO player (player_name, number, gender, date_of_birth, team_id) 
        VALUES (?, ?, ?, ?, ?)''', 
        (data['player_name'], data['number'], data['gender'], data['date_of_birth'], data['team_id']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Player added!'}), 201
@app.route('/players', methods=['GET'])
def get_players():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player")
    sport_types = cursor.fetchall()
    conn.close()
    return jsonify(sport_types), 200
@app.route('/teams', methods=['GET'])
def get_teams():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM team")
    sport_types = cursor.fetchall()
    conn.close()
    return jsonify(sport_types), 200
@app.route('/sport_types', methods=['GET'])
def get_sport_types():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sport_type")
    sport_types = cursor.fetchall()
    conn.close()
    return jsonify(sport_types), 200

# More routes can be added for fetching teams, players, etc.

if __name__ == '__main__':
    app.run(debug=True)
