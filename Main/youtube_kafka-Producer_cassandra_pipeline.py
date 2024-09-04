from googleapiclient.discovery import build
from kafka import KafkaProducer
from cassandra.cluster import Cluster
import json

# Initialize YouTube API
YOUTUBE_API_KEY = '**************************' 
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Kafka settings
KAFKA_TOPIC = 'channel_stats'
KAFKA_SERVER = 'localhost:9092'
producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER,
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

CASSANDRA_KEYSPACE = 'youtube_data'
# Connect to the local Cassandra instance
cluster = Cluster(['127.0.0.1'])
session = cluster.connect(CASSANDRA_KEYSPACE)

def fetch_channel_stats(channel_id):
    # Fetch channel statistics
    request = youtube.channels().list(
        part='statistics,snippet',
        id=channel_id
    )
    response = request.execute()
    return response

def fetch_video_stats(channel_id):
    # Fetch the list of videos in the channel
    request = youtube.search().list(
        part='id,snippet',
        channelId=channel_id,
        maxResults=50,
        order='date'  # To get the latest videos
    )
    response = request.execute()
    video_data = {}

    for item in response['items']:
        if item['id']['kind'] == 'youtube#video':
            video_id = item['id']['videoId']
            video_data[video_id] = {
                'title': item['snippet']['title'],
                'publishedAt': item['snippet']['publishedAt']
            }

    # Fetch video statistics
    for video_id in video_data.keys():
        request = youtube.videos().list(
            part='statistics',
            id=video_id
        )
        response = request.execute()
        for item in response['items']:
            video_data[video_id].update({
                'viewCount': item['statistics'].get('viewCount', 0),
                'likeCount': item['statistics'].get('likeCount', 0),
                'dislikeCount': item['statistics'].get('dislikeCount', 0),
                'commentCount': item['statistics'].get('commentCount', 0)
            })

    return video_data

def send_to_kafka(data):
    producer.send(KAFKA_TOPIC, data)
    producer.flush()

from datetime import datetime

def save_channel_stats_to_cassandra(channel_id, subscriber_count, view_count, video_count, total_likes, total_dislikes, total_comments):
    try:
        current_time = datetime.utcnow()
        session.execute("""
            INSERT INTO channel_stats_history (channel_id, timestamp, subscriber_count, view_count, video_count, total_likes, total_dislikes, total_comments)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (channel_id, current_time, subscriber_count, view_count, video_count, total_likes, total_dislikes, total_comments))
    except Exception as e:
        print(f"Error inserting channel stats: {e}")

def save_video_stats_to_cassandra(video_id, title, published_date, likes, views, comments, channel_id):
    # Convert to integers
    likes = int(likes)
    views = int(views)
    comments = int(comments)
    
    session.execute("""
        INSERT INTO video_stats (video_id, title, published_date, likes, views, comments, channel_id, last_updated)
        VALUES (%s, %s, %s, %s, %s, %s, %s, toTimestamp(now()))
    """, (video_id, title, published_date, likes, views, comments, channel_id))

def print_channel_stats(channel_id):
    channel_stats = fetch_channel_stats(channel_id)
    video_stats = fetch_video_stats(channel_id)

    # Extract channel statistics
    channel_data = channel_stats['items'][0]
    
    # Convert statistics to integers
    subscriber_count = int(channel_data['statistics']['subscriberCount'])
    view_count = int(channel_data['statistics']['viewCount'])
    video_count = int(channel_data['statistics']['videoCount'])

    # Initialize aggregate statistics
    total_likes = 0
    total_dislikes = 0
    total_comments = 0

    # Save video stats to Cassandra
    for video_id, stats in video_stats.items():
        # Ensure stats are converted to integers
        likes = int(stats['likeCount'])
        views = int(stats['viewCount'])
        comments = int(stats['commentCount'])
        
        save_video_stats_to_cassandra(
            video_id,
            stats['title'],
            stats['publishedAt'],
            likes,
            views,
            comments,
            channel_id
        )

        # Aggregate statistics
        total_likes += likes
        total_dislikes += int(stats.get('dislikeCount', 0))  # Default to 0 if 'dislikeCount' is missing
        total_comments += comments

    # Convert aggregate statistics to integers
    total_likes = int(total_likes)
    total_dislikes = int(total_dislikes)
    total_comments = int(total_comments)

    # Save channel stats to Cassandra
    try:
        current_time = datetime.utcnow()
        session.execute("""
            INSERT INTO channel_stats_history (channel_id, timestamp, subscriber_count, view_count, video_count, total_likes, total_dislikes, total_comments)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (channel_id, current_time, subscriber_count, view_count, video_count, total_likes, total_dislikes, total_comments))
    except Exception as e:
        print(f"Error inserting channel stats: {e}")

    # Prepare data for Kafka
    data = {
        'subscriber_count': subscriber_count,
        'view_count': view_count,
        'video_count': video_count,
        'total_likes': total_likes,
        'total_dislikes': total_dislikes,
        'total_comments': total_comments,
        'videos': video_stats  # Include individual video stats
    }

    # Send data to Kafka
    send_to_kafka(data)

    # Print channel stats for debugging purposes
    print(f"Subscriber Count: {subscriber_count}")
    print(f"View Count: {view_count}")
    print(f"Video Count: {video_count}")
    print(f"Total Likes: {total_likes}")
    print(f"Total Dislikes: {total_dislikes}")
    print(f"Total Comments: {total_comments}")




if __name__ == "__main__":
    channel_id = 'UCxOzbkk0bdVl6-tH1Fcajfg'
    print_channel_stats(channel_id)
