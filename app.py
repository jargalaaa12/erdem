from flask import Flask, request, jsonify
import sqlite3
import random

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>gg</h1>'

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

# onlyyy sport type iiin routes
@app.route('/sport_type', methods=['POST']) #sport type nemj ugnu
def add_sport_type():
    data = request.get_json()
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sport_type (sport_type) VALUES (?)", (data['sport_type'],))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Sport type added!'}), 201
@app.route('/sport_types', methods=['GET']) # bga sport type uudig harna
def get_sport_types():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sport_type")
    sport_types = cursor.fetchall()
    conn.close()
    return jsonify(sport_types), 200
@app.route('/count/sport_types', methods=['GET']) # niit heden sport type bgaag toolno
def count_sport_types():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sport_type")
    count = cursor.fetchone()[0]
    conn.close()
    return jsonify({'count': count}), 200
@app.route('/sport_type/<int:sport_type_id>', methods=['PUT'])
def update_sport_type(sport_type_id):
    data = request.get_json()
    if not data.get('sport_type'):
        return jsonify({'message': 'Missing required fields'}), 400

    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE sport_type
        SET sport_type = ?
        WHERE id = ?
    ''', (data['sport_type'], sport_type_id))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Sport type not found!'}), 404

    conn.close()
    return jsonify({'message': 'Sport type updated successfully!'}), 200
@app.route('/sport_type/<int:sport_type_id>', methods=['DELETE'])
def delete_sport_type(sport_type_id):
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM sport_type WHERE id = ?', (sport_type_id,))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Sport type not found!'}), 404

    conn.close()
    return jsonify({'message': 'Sport type deleted successfully!'}), 200

@app.route('/sport_type/<int:sport_type_id>', methods=['GET'])
def get_sport_type_by_id(sport_type_id):
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sport_type WHERE id = ?", (sport_type_id,))
    sport_type = cursor.fetchone()
    conn.close()

    if sport_type:
        return jsonify(sport_type), 200
    else:
        return jsonify({'message': 'Sport type not found!'}), 404


# Team iin buh routes
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
@app.route('/teams', methods=['GET'])
def get_teams():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM team")
    teams = cursor.fetchall()
    conn.close()
    return jsonify(teams), 200
@app.route('/count/teams', methods=['GET'])
def count_teams():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM team")
    count = cursor.fetchone()[0]
    conn.close()
    return jsonify({'count': count}), 200
@app.route('/team/<int:team_id>', methods=['PUT'])
def update_team(team_id):
    data = request.get_json()
    if not data.get('team_name') or not data.get('established_date') or not data.get('sport_type_id'):
        return jsonify({'message': 'Missing required fields'}), 400

    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()

    cursor.execute('''
        UPDATE team
        SET team_name = ?, established_date = ?, logo = ?, sport_type_id = ?
        WHERE id = ?
    ''', (data['team_name'], data['established_date'], data.get('logo'), data['sport_type_id'], team_id))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Team not found!'}), 404

    conn.close()
    return jsonify({'message': 'Team updated successfully!'}), 200
@app.route('/team/<int:team_id>', methods=['DELETE'])
def delete_team(team_id):
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM team WHERE id = ?', (team_id,))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Team not found!'}), 404

    conn.close()
    return jsonify({'message': 'Team deleted successfully!'}), 200
@app.route('/team/<int:team_id>', methods=['GET'])
def get_team_by_id(team_id):
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM team WHERE id = ?", (team_id,))
    team = cursor.fetchone()
    conn.close()

    if team:
        return jsonify(team), 200
    else:
        return jsonify({'message': 'Team not found!'}), 404


# buh playeriin routes 
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
    players = cursor.fetchall()
    conn.close()
    return jsonify(players), 200
@app.route('/count/players', methods=['GET'])
def count_players():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM player")
    count = cursor.fetchone()[0]
    conn.close()
    return jsonify({'count': count}), 200
@app.route('/player/<int:player_id>', methods=['PUT'])
def update_player(player_id):
    data = request.get_json()
    
    if not data.get('player_name') or not data.get('number') or not data.get('gender') or not data.get('date_of_birth') or not data.get('team_id'):
        return jsonify({'message': 'Missing required fields'}), 400
    
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE player
        SET player_name = ?, number = ?, gender = ?, date_of_birth = ?, team_id = ?
        WHERE id = ?
    ''', (data['player_name'], data['number'], data['gender'], data['date_of_birth'], data['team_id'], player_id))
    
    conn.commit()
    
    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Player not found!'}), 404
    
    conn.close()
    return jsonify({'message': 'Player updated successfully!'}), 200
@app.route('/player/<int:player_id>', methods=['DELETE'])
def delete_player(player_id):
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()

    cursor.execute('DELETE FROM player WHERE id = ?', (player_id,))

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({'message': 'Player not found!'}), 404

    conn.close()
    return jsonify({'message': 'Player deleted successfully!'}), 200
@app.route('/player/<int:player_id>', methods=['GET'])
def get_player_by_id(player_id):
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM player WHERE id = ?", (player_id,))
    player = cursor.fetchone()
    conn.close()

    if player:
        return jsonify(player), 200
    else:
        return jsonify({'message': 'Player not found!'}), 404



# bugdiig ni toolood haruulah
@app.route('/count/all', methods=['GET'])
def count_all():
    conn = sqlite3.connect('sports.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM sport_type")
    sport_type_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM team")
    team_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM player")
    player_count = cursor.fetchone()[0]

    conn.close()
    
    return jsonify({
        'sport_type_count': sport_type_count,
        'team_count': team_count,
        'player_count': player_count
    }), 200
if __name__ == '__main__':
    app.run(debug=True)
