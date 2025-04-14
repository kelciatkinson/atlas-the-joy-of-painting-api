# atlas-the-joy-of-painting-api

## Bob Ross Episodes API

A database that houses data about Bob Ross's "The Joy of Painting" episodes, allowing viewers to filter episodes by broadcast month, subject matter, and color palette.

## Project Overview

This project implements an ETL (Extract, Transform, Load) process to import data from various sources into a structured MySQL database. In the future thegoal is to provide an API that allows users to filter Bob Ross's painting episodes based on various criteria.

### Features

Month-based filtering: Find episodes that aired in a specific month\
Subject filtering: Find episodes containing specific subjects (mountains, lakes, etc.)\
Color palette filtering: Find episodes where specific colors were used
## Database Structure

The database has a structure with these tables:

episode: Contains basic episode information (title, season, episode number, air date, month)\
color: List of unique colors used across all episodes\
subject: List of unique subjects painted across all episodes\
episode_color: Join table connecting episodes to their colors\
episode_subject: Join table connecting episodes to their subjects
## ETL Process

The ETL process handles:

Extraction of data from CSV file\
Transformation of data to fit the database schema, including:\
Deduplication of episodes\
Normalization of colors and subjects\
Loading data into the MySQL database
## Setup Instructions

### Prerequisites

Python 3.x\
MySQL Server\
Required Python packages: mysql-connector-python\
### Installation

Clone this repository

git clone https://github.com/kelciatkinson/atlas-the-joy-of-painting-api
cd atlas-the-joy-of-painting-api

Set up the database

mysql -u username -p < database/schema.sql

Install required Python packages

pip install -r requirements.txt

Configure database connection

# Edit db/config.py with your database credentials

Run the ETL process

python run_etl.py


## Sample Queries

Find episodes by month:\
sql\
SELECT episode_id, title, season, episode\
FROM episode\
WHERE month = 'January';

Find episodes with mountains:\
sql\
SELECT e.episode_id, e.title\
FROM episode e\
JOIN episode_subject es ON e.episode_id = es.episode_id\
JOIN subject s ON es.subject_id = s.subject_id\
WHERE s.subject_name = 'MOUNTAINS';

Find episodes using Phthalo Blue:\
sql\
SELECT e.episode_id, e.title\
FROM episode e\
JOIN episode_color ec ON e.episode_id = ec.episode_id\
JOIN color c ON ec.color_id = c.color_id\
WHERE c.color_name = 'Phthalo Blue';
