import sqlite3, datetime


CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    title TEXT,
    release_timestamp REAL
);
"""

CREATE_WATCHLIST_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    watcher_name TEXT,
    title TEXT
    );
"""

INSERT_MOVIES = "INSERT INTO movies (title, release_timestamp) VALUES (?, ?);"
DELETE_MOVIE = "DELETE from movies WHERE title = ?;"
SELECT_ALL_MOVIES = "SELECT * FROM movies;"
SELECT_UPCOMING_MOVIES = "SELECT * FROM movies WHERE release_timestamp > ?;"
SELECT_WATCHED_MOVIES = "SELECT * FROM watched WHERE watcher_name = ?;"
INSERT_WATCHED_MOVIE = "INSERT INTO watched (watcher_name, title) VALUES (?, ?);"
SET_MOVIE_WATCHED = "UPDATE movies SET watched = 1 where title = ?;" 


connection = sqlite3.connect("data.db")

def create_tables():
    connection.execute(CREATE_MOVIES_TABLE)
    connection.execute(CREATE_WATCHLIST_TABLE)
    connection.commit()

def add_movie(title, release_timestamp):
    connection.execute(INSERT_MOVIES, (title, release_timestamp))
    connection.commit()

def get_movies(upcoming=False):
    cursor = connection.cursor()
    if upcoming:
        today_timestamp = datetime.datetime.today().timestamp()
        cursor.execute(SELECT_UPCOMING_MOVIES, (today_timestamp,)) #today_timestamp is a tuple so it needs a comma
    else:
        cursor.execute(SELECT_ALL_MOVIES)
    return cursor.fetchall()
    connection.commit()

def watch_movie(title):
    connection.execute(SET_MOVIE_WATCHED, (title,))
    connection.commit()

def get_watched_movies():
    cursor = connection.cursor()
    cursor.execute(SELECT_WATCHED_MOVIES)
    return cursor.fetchall()