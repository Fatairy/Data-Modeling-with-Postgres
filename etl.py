import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    '''
    Process and insert the files from the song_data to the song table and artist table in the database

            Parameters:
                    cur (object): A cursor for the connection of the database
                    filepath (String): string of the path of the song_data

            Returns:
                    Void
    '''
    df = pd.read_json(filepath,lines = True)
 
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    '''
    Process and insert the files from the log_data to the user table, time table and songplay table in the database

            Parameters:
                    cur (object): A cursor for the connection of the database
                    filepath (String): string of the path of the song_data

            Returns:
                    Void
    '''
    df = pd.read_json(filepath,lines = True)

    df = df[df.page == 'NextSong']


    t = pd.to_datetime(df.ts,unit = 'ms')
    
    # Convert the time data to df to insert in the time table
    time_data = [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.weekday]
    column_labels = ('start_time', 'hour', 'day', 'week', 'month', 'year', 'weekday')
    time_df = pd.DataFrame.from_dict(dict(zip(column_labels,time_data)))

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))


    user_df = df[['userId','firstName','lastName','gender','level']]

    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)


    for index, row in df.iterrows():
        
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        songplay_data =(t[index], row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent) 
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    '''
    Extract all the filepaths of the data then calls the func to process and insert the data into the database

            Parameters:
                    cur (object): A cursor for the connection of the database
                    conn (object): The connection to the database
                    filepath (string):  the directory path for the data
                    func (function): A function for the processing of the data

            Returns:
                    Void
    '''
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    '''
    Connect to the db and call the functions created then after its done close the connection
            Parameters:
                        Void
            Returns:
                        Void
    '''
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()