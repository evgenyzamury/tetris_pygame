import sqlite3

database_path = 'data/tetris.db'


def get_statistic():  # получаем статистику активного игрока из базы данных
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """SELECT best_score, all_score, play_time FROM stats INNER JOIN players on players.id = stats.player_id
                    WHERE player = (SELECT player FROM players WHERE active_player = 1)"""
    result = cur.execute(query).fetchone()
    # player_id, best_score all_score play_time
    con.close()
    print(result)
    best_score = result[0]
    all_score = result[1]
    play_time = result[2] // 60
    return best_score, all_score, play_time


def save_result_in_db(score, time):  # обновляем и сохраняем статистику игрока
    new_record = False  # Переменная для проверки нового рекорда
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """SELECT best_score, all_score, play_time FROM stats INNER JOIN players on players.id = stats.player_id
                    WHERE player = (SELECT player FROM players WHERE active_player = 1)"""
    result = cur.execute(query).fetchone()
    best_score = result[0]
    all_score = result[1] + score
    print(result[2])
    print(time)
    all_time = result[2] + time
    print(all_time)
    if score > best_score:
        new_record = True
        best_score = score
    query = """UPDATE
            stats
        SET
            best_score = ?,
            all_score = ?,
            play_time = ?
        WHERE player_id = (SELECT id FROM players WHERE active_player = 1)"""
    cur.execute(query, (best_score, all_score, all_time))
    con.commit()
    con.close()
    print('данные в бд сохранены', best_score, all_score, all_time)
    return new_record


def get_player_settings():
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """SELECT * FROM settings INNER JOIN players on players.id = settings.player_id
                       WHERE player = (SELECT player FROM players WHERE active_player = 1)"""
    result = cur.execute(query).fetchone()
    music_volume, block_volume, difficulty, language, theme = result[1], result[2], result[3], result[4], result[5]
    return music_volume, block_volume, difficulty, language, theme


def get_player_name():
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = "SELECT player FROM players WHERE active_player = 1"
    player = cur.execute(query).fetchone()[0]
    con.close()
    return player


def get_players_name():
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = "SELECT player FROM players"
    players = cur.execute(query).fetchall()
    con.close()
    players = [player[0] for player in players]
    return players


def create_player(name):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query_active_settings = """SELECT 
                                    music_volume, block_volume, difficulty, language, theme 
                                FROM 
                                    settings    
                                WHERE player_id = (SELECT id FROM players WHERE active_player = 1)
                                """
    # узнаём активные настройки и применяем их к новому игроку
    music_volume, block_volume, difficulty, language, theme = cur.execute(query_active_settings).fetchone()
    query = "UPDATE players SET active_player = 0 WHERE id = (SELECT id FROM players WHERE active_player = 1)"
    cur.execute(query)  # убираем активного игрока
    query = "INSERT INTO players(player, active_player) VALUES (?, 1)"
    cur.execute(query, (name,))  # создаём нового игрока

    query = "SELECT id FROM players WHERE active_player = 1"
    players_id = cur.execute(query).fetchone()[0]  # узнаём id у нового игрока

    query = f"""INSERT INTO stats VALUES({players_id}, 0, 0, 0)"""  # статистика нового игрока
    cur.execute(query)

    query = f"""INSERT INTO settings 
    VALUES({players_id}, {music_volume}, {block_volume}, {difficulty}, '{language}', {theme});"""
    cur.execute(query)  # настройки нового игрока
    con.commit()
    con.close()


def change_player(name):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = "UPDATE players SET active_player = 0 WHERE id = (SELECT id FROM players WHERE active_player = 1)"
    cur.execute(query)  # убираем активного игрока
    query = "UPDATE players SET active_player = 1 WHERE player = ?"
    cur.execute(query, (name,))
    con.commit()
    con.close()


def update_player_settings(music_volume, block_volume, difficulty, language, theme):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """UPDATE settings SET music_volume = ?, block_volume = ?, difficulty = ?, language = ?, theme = ?
                           WHERE player_id = (SELECT id FROM players WHERE active_player = 1)"""
    cur.execute(query, (music_volume, block_volume, difficulty, language, theme))
    con.commit()
    con.close()


def create_table():
    con = sqlite3.connect('data/tetris.db')
    cur = con.cursor()
    query = """CREATE TABLE players (
    id            INTEGER     UNIQUE
                              NOT NULL
                              PRIMARY KEY AUTOINCREMENT,
    player        TEXT        NOT NULL,
    active_player INTEGER (1) );
    """
    cur.execute(query)
    query = """CREATE TABLE stats (
    player_id  INTEGER REFERENCES tetris (id) 
                       UNIQUE,
    best_score INTEGER,
    all_score  INTEGER,
    play_time  INTEGER); """
    cur.execute(query)
    query = """INSERT INTO players VALUES(1, 'guest', 1);"""
    cur.execute(query)
    query = """INSERT INTO stats VALUES(1, 0, 0, 0);"""
    cur.execute(query)
    query = """CREATE TABLE settings (
    player_id    INTEGER REFERENCES players (id),
    music_volume INTEGER,
    block_volume INTEGER,
    difficulty   INTEGER,
    language     TEXT,
    theme        INTEGER
    );
    """
    cur.execute(query)
    query = """INSERT INTO settings VALUES(1, 50, 50, 0, 'en', 0);"""
    cur.execute(query)
    con.commit()
    con.close()
