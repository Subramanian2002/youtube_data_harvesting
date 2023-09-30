import streamlit as st
import pymongo
import main1 as m
import insert_to_sql1 as i
from isodate import parse_duration
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["YTH"]
mycol = mydb["channel_data"]


#Streamlit 
st.write("# YouTube Data Harvesting ")
if 'ch_data' not in st.session_state:
    st.session_state.ch_data = []
      

channel_id = st.sidebar.text_input("Enter Channel_id:")

# Check if the "Fetch Data" button is clicked
if st.sidebar.button("Fetch Data"):
    if channel_id:
        existing_channel = mycol.find_one({"channel_details.Channel_Id": channel_id})
        if existing_channel:
            st.warning("This channel_id ia already exists in the database.")
        else:    
            data = m.main(channel_id)
            st.session_state.ch_data.append(data)
            if data:
                mycol.insert_one(data)
            else:
                st.warning("Please enter a channel ID before store data.")
    else:
        st.warning("Please enter a channel ID before fetching data.")


if st.session_state.ch_data:
     st.write(st.session_state.ch_data[-1])

channel_names = [channel['channel_details'][0]['Channel_Name'] for channel in mycol.find()]



st.sidebar.selectbox('Channels', channel_names[::-1])
if st.sidebar.button('store_in_sql'):
    i.insert_sql()


username = 'root'
password = '1234'
host = 'localhost'
port = '3306'
database_name = 'youtube_data_harvesting'
db_url = f'mysql://{username}:{password}@{host}:{port}/{database_name}'

conn = st.experimental_connection('youtube_data_harvesting', type='sql', url=db_url,autocommit=True)


table_options = ["--select-query--",
                 "What are the names of all the videos and their corresponding channels?", 
                 "Which channels have the most number of videos, and how many videos dothey have?", 
                 "What are the top 10 most viewed videos and their respective channels?",
                 "How many comments were made on each video, and what are their corresponding video names?",
                 "Which videos have the highest number of likes, and what are their corresponding channel names?",
                 "What is the total number of likes and what are their corresponding video names?",
                 "What is the total number of views for each channel, and what are their corresponding channel names?",
                 "What are the names of all the channels that have published videos in the year 2022?",
                 "What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                 "Which videos have the highest number of comments, and what are their corresponding channel names?"]
selected_table = st.sidebar.selectbox("Questions", table_options)

# Display the selected table data when a table is selected
if selected_table == "What are the names of all the videos and their corresponding channels?":
    
    data = conn.query("""select c.channel_name,v.video_name from channels as c inner join videos as v on c.channel_id = v.channel_id;""",ttl=None)
    
    st.dataframe(data)
elif selected_table == "Which channels have the most number of videos, and how many videos dothey have?":
   data = conn.query("""select c.channel_name,count(v.video_id) as video_count from channels as c
                        inner join videos as v on c.channel_id = v.channel_id 
                        group by c.channel_name
                        order by video_count desc
                        limit 1;""",ttl=None)
  
   st.dataframe(data)
elif selected_table == "What are the top 10 most viewed videos and their respective channels?":
  data = conn.query("""select c.channel_name , v.video_name, v.view_count from videos as v
                        inner join channels as c on c.channel_id = v.channel_id
                        order by v.view_count desc 
                        limit 10;""",ttl=None)
  st.dataframe(data)
elif selected_table == "How many comments were made on each video, and what are their corresponding video names?":
   data = conn.query("""select video_name,comment_count from videos;""",ttl=None)
   st.dataframe(data) 
elif selected_table == "Which videos have the highest number of likes, and what are their corresponding channel names?":
   data = conn.query("""select c.channel_name,v.video_name , v.like_count max_likes from videos as v
                        inner join channels as c on v.channel_id = c.channel_id
                        order by v.like_count desc
                        limit 10;""",ttl=None)
   st.dataframe(data)
elif selected_table == "What is the total number of likes and what are their corresponding video names?":
   data = conn.query("""select video_name,like_count from videos;""")
   st.dataframe(data)
elif selected_table == "What is the total number of views for each channel, and what are their corresponding channel names?":
   data = conn.query("""select channel_name,channel_views from channels
                        order by channel_views desc;""",ttl=None)
   st.dataframe(data)
elif selected_table == "What are the names of all the channels that have published videos in the year 2022?":
   data = conn.query("""select distinct c.channel_name
                        from channels AS c
                        inner join  videos as v on c.channel_id = v.channel_id
                        where year(v.published_date) = 2022;""",ttl=None)
   st.dataframe(data)
elif selected_table == "What is the average duration of all videos in each channel, and what are their corresponding channel names?":
   data = conn.query("""select c.channel_name,avg(v.video_duration) as avg_duration from channels as c
                        inner join videos as v on c.channel_id = v.channel_id
                        group by c.channel_name order by avg_duration desc;""",ttl=None)
   st.dataframe(data) 
elif selected_table == "Which videos have the highest number of comments, and what are their corresponding channel names?":
   data = conn.query("""select v.video_name, v.comment_count ,c.channel_name from channels as c
                        inner join videos as v on c.channel_id = v.channel_id
                        order by v.comment_count desc
                        limit 10;""",ttl=None)

   st.dataframe(data)                         



