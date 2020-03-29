# Sparkify Data Warehouse

Sparkify is a music streaming startup that needs help transitioning their fast-growing data to the cloud. The data is stored in S3, which is a directory of JSON logs on user activity on the app. There is also a directory with JSON metadata on the songs in the app.

The purpose of this project is to build an ETL pipeline that extracts data from S3 into Redhsift and transforms the data into dimensional tables for further analysis for the team to explore. The data is grabbed from S3 buckets and temporarily stored into staging tables. Then it is transformed into a star schema with a fact and dimensional tables.

Datasets:
* Song data: s3://udacity-dend/song_data
* Log data: s3://udacity-dend/log_data

Tables

Staging Tables: Temporary tables with the raw data from the S3 buckets
* staging_events - event data when songs are played
![Log Data](log-data.png)
    - artist
    - auth
    - firstName
    - gender
    - itemInSession
    - lastName
    - length
    - level
    - location
    - method
    - page
    - registration
    - sessionId
    - song
    - status
    - ts
    - userAgent
    - userId

* staging_songs - song and artist information
`{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", "artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}`
    - song_id
    - num_songs
    - title
    - artist_id
    - artist_latitude
    - artist_longitude
    - artist_location
    - artist_name
    - duration
    - year


Star Schema
Fact Table
* songplay - records in event data associated with song plays i.e. records with page NextSong
    - songplay_id
    - start_time
    - user_id
    -  level
    - song_id
    - artist_id
    - session_id
    - location
    - user_agent

Dimension Tables
* users - users in the app
    - user_id
    - first_name
    - last_name
    - gender
    - level

* songs - songs in music database
    - song_id
    - title
    - artist_id
    - year
    - duration

* artists - artists in music database
    - artist_id
    - name
    - location
    - lattitude
    - longitude

* time - timestamps of records in songplays broken down into specific units
    - start_time
    - hour
    - day
    - week
    - month
    - year
    - weekday

**How to run:**
1. Make a copy of `dwh_template.cfg` and rename it `dwh.cfg`
2. Open the file and input all your parameters for your database and your AWS key and secret code (Don't type in anything in 'ARN' and 'HOST' yet)
2. Travel to the downloaded directory via the command terminal
3. Type in `jupyter notebook`
4. Open the `CreateRedshiftCluster.ipynb` file and run all cells. This file creates an IAM role to access the S3 bucket and a Redshift cluster.
5. Make sure to uncomment the code in the DWH_ENDPOINT and DWH_ROLE_ARN cells
6. Obtain the DWH_endpoint value and input it in the '[CLUSTER]' section under 'HOST' in the `dwh.cfg` file 
7. Obtain the DWH_ROLE_ARN value and input it in the '[IAM_ROLE]' section under 'ARN' in the `dwh.cfg` file
8. Type `python create_tables.py` in the command terminal to run the script that creates SQL tables
9. Type `python etl.py` in the command terminal to run the script that transforms the data and loads it into appropriate tables

