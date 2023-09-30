import mysql.connector as sql
conn =sql.connect(user = 'root',password = '1234',host = 'localhost',database ='youtube_data_harvesting')
cursor = conn.cursor()


query = """CREATE TABLE channels(
        channel_id varchar(255),
        channel_name varchar(255),
        channel_views int,
        channel_description text,
        channel_subscription_count int);"""
cursor.execute(query)  

query = """create table playlist(
           playlist_id varchar(255),
           channel_id varchar(255),
           playlist_name varchar(255));"""
cursor.execute(query) 

query = """create table videos(video_id varchar(255),
           channel_id varchar(255),
           video_name varchar(255),
           video_description varchar(255),
           published_date datetime,
           view_count int,
           like_count int,
           favorite_count int,
           comment_count int,
           video_duration int,
           thumbnail varchar(255),
           caption_satatus varchar(255));"""
cursor.execute(query)


query = """create table comments(comment_id varchar(255),
           video_id varchar(255),
           comment_text text,
           comment_author varchar(255),
           comment_published_date datetime);"""
cursor.execute(query)