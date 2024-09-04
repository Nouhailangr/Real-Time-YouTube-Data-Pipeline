# Real-Time-YouTube-Data-Pipeline

## Table of Contents

1. [Introduction](#introduction)
2. [Project Overview](#project-overview)
3. [Tools Used](#tools-used)
4. [Project Steps](#project-steps)

## Introduction

In this project, we created a system to monitor and visualize YouTube channel and video statistics. Our goal was to track metrics such as subscriber count, video views, likes, comments, and other engagement statistics in real time.

## Project Overview

We designed a solution that collects data from a YouTube channel and its videos, processes this data, and visualizes it using various tools. The metrics we focus on include `subscriber_count`, `total_comments`, `total_dislikes`, `total_likes`, `video_count`, and `view_count` for the channel, and `video_id`, `title`, `likes`, `views`, and `comments` for individual videos.

![YouTube_RealTime_Pipeline_Diagram](https://github.com/user-attachments/assets/fbbbc6c1-a2b7-4420-bd11-fead53fc4272)

### Components
- **Data Collection:** We implemented scripts to fetch data from the YouTube Data API for both channel and video statistics.
- **Data Processing:** We processed and aggregated the data to derive meaningful insights.
- **Data Storage:** We stored the processed data in Cassandra for historical analysis and querying.
- **Data Visualization:** We used Grafana (or Apache Superset as an alternative) to create dashboards and visualizations of the data.
- **Workflow Orchestration:** We used Apache Airflow to manage and automate data workflows.

## Tools Used

- **YouTube Data API:** To fetch channel and video statistics.
- **Cassandra:** For data storage and querying.
- **Grafana:** For real-time dashboard visualization (alternatively, Apache Superset).
- **Kafka:** For data streaming and integration (if applicable).
- **Apache Airflow:** For workflow orchestration and automation.

## Project Steps

1. **Setup and Configuration**
   - We installed and configured the necessary tools and libraries.
   - We set up Cassandra and created keyspaces/tables for storing channel and video stats.
   - We configured API access and credentials for the YouTube Data API.
   - We installed and configured Apache Airflow for managing workflows.

2. **Data Collection**
   - We implemented scripts to fetch channel and video statistics from YouTube.
   - We stored the collected data in Cassandra.

3. **Data Processing**
   - We aggregated and processed the data as needed.
   - We performed necessary data cleaning and transformation.

4. **Data Storage**
   - We ensured data was correctly stored in Cassandra.

5. **Data Visualization**
   - We set up Grafana.
   - We connected the visualization tool to Cassandra.
   - We created dashboards to visualize channel and video statistics.
   - We configured charts and graphs to display metrics such as likes, views, and comments by video title.

6. **Workflow Orchestration**
   - We created Airflow DAGs (Directed Acyclic Graphs) to automate data collection, processing, and storage tasks.
   - We scheduled regular runs of data fetching and processing tasks using Airflow.

## Dashboard
<img width="1440" alt="YouTube_RealTime_Dashboard" src="https://github.com/user-attachments/assets/1730af0f-4ec5-4937-8e5e-803711cc5cce">



  
For any questions or support, please contact [nouhailangr275128@gmail.com](mailto:your_email@example.com).
