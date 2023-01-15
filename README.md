
# Data Modeling with Postgres

This project models user activity data for a music streaming app called Sparkify to optimize queries for understanding what songs users are listening to by creating a Postgres relational database and ETL pipeline to build up Fact and Dimension tables and insert data into new tables

### ETL Pipeline
- sql_queries.py  
    - Contains all the sql queries, and is imported to all the other files.

- create_tables.py
    - Create the sparkify database, drops all existing tables, and creates new tables.
- etl.ipynb
    -  Reads and process a single file from song_data and log_data and loads them in the tables and has the ETL process for each table.
- etl.ipynb
    - Reads and process all files from song_Data and log_data and loads them in the tables.

- test.ipynb
    - Contains sanity checks.



### How to run the project
- Install Postgres server and psycopg2.
- Run create_tables.py to create the working database and tables.
    - ``` python3 create_tables.py ``` 
- Run etl.ipynb to check that every thing is working.
- Run create_tables to drop the changes done by etl.ipynb.
- Run etl.py to process and load all data to the database.
- Run test.ipynb for the sanity checks.

### Database Schema (Star Schema)

Dimension tables:
```
users
    - user_id int	PRIMARY KEY,
    - first_name varchar,
    - last_name varchar,
    - gender varchar,
    - level varchar
```
```
songs                       
    - song_id varchar PRIMARY KEY,
    - title varchar NOT NULL,
    - artist_id varchar ,
    - year int,
    - duration numeric NOT NULL
```
```
artists                       
    - artist_id varchar PRIMARY KEY,
    - name varchar NOT NULL,
    - location varchar,
    - latitude float,
    - longitude float
```
```
time                       
    - start_time TIMESTAMP PRIMARY KEY,
    - hour int,
    - day int,
    - week int,
    - month int,
    - year int,
    - weekday varchar
```
Fact table

```
songplays                       
    - songplay_id SERIAL PRIMARY KEY,
    - start_time TIMESTAMP NOT NULL,
    - user_id int NOT NULL,
    - level varchar,
    - song_id varchar ,
    - artist_id varchar,
    - session_id int,
    - location varchar,
    - user_agent varchar
```