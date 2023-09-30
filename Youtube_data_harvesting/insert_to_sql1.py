def insert_sql():
    import pymongo

    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["YTH"]
    mycol = mydb["channel_data"]
    my_data =list(mycol.find())
    from datetime import datetime
    import mysql.connector as sql
    conn =sql.connect(user = 'root',password = '1234',host = 'localhost',database = 'youtube_data_harvesting')
    cursor = conn.cursor()

    channel_query = """INSERT INTO channels(channel_id,channel_name,channel_views,channel_description,channel_subscription_count) 
                      VALUES(%s,%s,%s,%s,%s)"""
    playlist_query = """insert into playlist(playlist_id,channel_id,playlist_name)values(%s,%s,%s);"""
    video_query = """insert into videos(video_id,channel_id,video_name,video_description,
                        published_date,view_count,like_count,favorite_count,
                        comment_count,video_duration,thumbnail,caption_satatus) 
                        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    comment_query = """insert into comments(comment_id,video_id,comment_text,comment_author,comment_published_date)values(%s,%s,%s,%s,%s);"""
    for i in my_data:
        cursor.execute("select * from channels where Channel_Id =%s",(i['channel_details'][0]['Channel_Id'],))
        existing_data = cursor.fetchone()
        if existing_data:
            pass
        else:
            for j in i['channel_details']:
                values =(j['Channel_Id'],
                        j['Channel_Name'],
                        int(j['Channel_Views']),
                        j['Channel_Description'],
                        int(j['Subscription_Count']))
                cursor.execute(channel_query,values)  
                conn.commit()
            for j in i['channel_playlists']:
                values =(j['playlist_id'],
                        j['channel_id'],
                        j['playlist_name'])
                cursor.execute(playlist_query,values) 
                conn.commit() 
            for j in i['video_details']:
                values =(j['video_id'],
                        j['channel_id'],
                        j['video_name'],
                        j['video_description'],
                        j['publishedat'],
                        int(j['view_count']),
                        int(j['like_count']),
                        int(j['favorite_count']),
                        int(j['comment_count']),
                        j['video_duration'],
                        j['thumbnail'],
                        j['caption'])
                cursor.execute(video_query,values) 
                conn.commit()
            for j in i['comment_details']:
                values =(j['comment_id'],
                        j['video_id'],
                        j['comment_text'],
                        j['comment_author'],
                        datetime.strptime(j['comment_publishedat'],"%Y-%m-%dT%H:%M:%SZ"))
                cursor.execute(comment_query,values)       
                conn.commit()             

    cursor.close()
    
    