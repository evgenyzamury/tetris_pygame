import sqlite3


database_path = 'data/tetris.db'


def get_statistic():
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """SELECT * FROM stats INNER JOIN players on players.id = stats.player_id
                    WHERE player = (SELECT player FROM players WHERE active_player = 1)"""
    result = cur.execute(query).fetchone()
    # player_id, best_score all_score play_time
    con.close()
    best_score = result[1]
    all_score = result[2]
    play_time = result[3]
    return best_score, all_score, play_time


def save_result_in_db(score, time):
    con = sqlite3.connect(database_path)
    cur = con.cursor()
    query = """SELECT * FROM stats INNER JOIN players on players.id = stats.player_id
                    WHERE player = (SELECT player FROM players WHERE active_player = 1)"""
    result = cur.execute(query).fetchone()
    best_score = result[1]
    all_score = result[2] + score
    all_time = result[3] + time
    if score > best_score:
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
