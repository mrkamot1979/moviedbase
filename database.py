import sqlite3, datetime


CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    id INTEGER PRIMARY KEY,
    title TEXT,
    release_timestamp REAL
);
"""

CREATE_USERS_TABLE = """CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY
);
"""

CREATE_WATCHED_TABLE = """CREATE TABLE IF NOT EXISTS watched (
    user_username TEXT,
    movie_id INTEGER,
    FOREIGN KEY (user_username) REFERENCES users(username),
    FOREIGN KEY (movie_id) REFERENCES movies(id)
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
    connection.execute(CREATE_USERS_TABLE)
    connection.execute(CREATE_WATCHED_TABLE)
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

def watch_movie(username, title): #once a movie is watched, it is deleted in the movie database and then the details are entered onto the "watched" database
    connection.execute(DELETE_MOVIE, (title,))
    connection.execute(INSERT_WATCHED_MOVIE, (username, title))
    connection.commit()

def get_watched_movies(username):
    cursor = connection.cursor()
    cursor.execute(SELECT_WATCHED_MOVIES, (username, ))
    return cursor.fetchall()
