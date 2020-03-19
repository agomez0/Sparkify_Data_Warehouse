import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# GLOBAL VARIABLES
LOG_DATA = config.get("S3","LOG_DATA")
LOG_PATH = config.get("S3", "LOG_JSONPATH")
SONG_DATA = config.get("S3", "SONG_DATA")
IAM_ROLE = config.get("IAM_ROLE","ARN")

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events;"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs;"
songplay_table_drop = "DROP TABLE IF EXISTS songplay;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE staging_events (
    artist VARCHAR,
    auth VARCHAR,
    firstName VARCHAR,
    gender VARCHAR,
    itemInSession INTEGER,
    length FLOAT,
    level VARCHAR,
    location VARCHAR,
    method VARCHAR,
    page VARCHAR,
    registration FLOAT,
    sessionId INTEGER,
    song VARCHAR,
    status INTEGER,
    ts INTEGER,
    userAgent VARCHAR,
    userId INTEGER
);
""")

staging_songs_table_create = ("""
CREATE TABLE staging_songs(
    song_id VARCHAR,
    num_songs INTEGER,
    title VARCHAR,
    artist_id VARCHAR,
    artist_latitude FLOAT,
    artist longitude FLOAT,
    artist_location VARCHAR,
    artist_name VARCHAR,
    title VARCHAR,
    duration FLOAT,
    year INT
);
""")

songplay_table_create = ("""
CREATE TABLE songplay (
    songplay_id INTEGER NOT NULL PRIMARY KEY,
    start_time TIMESTAMP NOT NULL,
    user_id INTEGER NOT NULL,
    level VARCHAR(15) NOT NULL,
    song_id VARCHAR(255) NOT NULL,
    artist_id VARCHAR(255) NOT NULL,
    session_id INTEGER NOT NULL,
    location VARCHAR(80) NOT NULL,
    user_agent VARCHAR(80) NOT NULL
);
""")

user_table_create = ("""
CREATE TABLE users (
    user_id INTEGER NOT NULL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    gender VARCHAR(7) NOT NULL,
    level VARCHAR(15) NOT NULL
);
""")

song_table_create = ("""
CREATE TABLE songs (
    song_id VARCHAR(255) NOT NULL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id VARCHAR(255) NOT NULL,
    year INTEGER,
    duration FLOAT
);
""")

artist_table_create = ("""
CREATE TABLE artists (
    artist_id VARCHAR(255) NOT NULL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    location VARCHAR(55),
    latitude FLOAT,
    longitude FLOAT
);
""")

time_table_create = ("""
CREATE TABLE time (
    start_time TIMESTAMP PRIMARY KEY,
    hour INTEGER,
    day INTEGER,
    week INTEGER,
    month INTEGER,
    year INTEGER,
    weekday BOOLEAN
);
""")

# STAGING TABLES

staging_events_copy = ("""
COPY staging_events FROM {}
CREDENTIALS 'aws_iam_role={}'
COMPUPDATE OFF region 'us-west-2'
TIMEFORMAT as 'epochmillisecs'
TRUNCATECOLUMNS BLANKSASNULL EMPTYASNULL
FORMAT AS JSON {};
""").format(LOG_DATA, IAM_ROLE, LOG_PATH)

staging_songs_copy = ("""
COPY staging_songs FROM {}
CREDENTIALS 'aws_iam_role={}'
COMPUPDATE OFF region 'us-west-2'
TRUNCATECOLUMNS BLANKASNULL EMPTYASNULL;
""").format(SONG_DATA, IAM_ROLE)

# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplay (songplay_id, start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
SELECT se.session_id AS songplay_id,
    to_timestamp(to_char(se.ts, '9999-99-99 99:99:99'),'YYYY-MM-DD HH24:MI:SS') AS start_time,
    se.userId AS user_id,
    se.level AS level,
    ss.song_id AS song_id,
    ss.artist_id AS artist_id,
    se.location AS location,
    se.userAgent AS user_agent,
FROM songplay_events se
JOIN songplay_songs ss
ON se.artist = ss.artist_name
WHERE se.page = 'NextSong';
""")

user_table_insert = ("""
INSERT INTO users (user_id, first_name, last_name, gender, level)
SELECT DISTINCT userId AS user_id,
    firstName AS first_name,
    lastName AS last_name,
    gender AS gender,
    level AS level
FROM staging_events;
""")

song_table_insert = ("""
INSER INTO songs (song_id, title, artist_id, year, duration)
SELECT DISTINCT song_id AS song_id,
    title AS title,
    artist_id AS artist_id,
    year AS year,
    duration AS duration
FROM staging_songs;
""")

artist_table_insert = ("""
INSERT INTO artists (artist_id, name, location, latitude, longitude)
SELECT DISTINCT artist_id AS artsit_id,
    artist_name AS name,
    artist_location AS lcoation,
    artist_latitude AS latitude,
    artist_longitude AS longitude
FROM staging_songs;
""")

time_table_insert = ("""
INSERT INTO time (start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT to_timestamp(to_char(se.ts, '9999-99-99 99:99:99'),'YYYY-MM-DD HH24:MI:SS') AS start_time,
    EXTRACT (hour from ts) AS hour,
    EXTRACT (day from ts) AS day,
    EXTRACT (week from ts) AS day,
    EXTRACT (month from ts) AS month,
    EXTRACT (year from ts) AS year,
    EXTRACT (weekday from ts) AS weekday
FROM staging_events;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
