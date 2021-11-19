import os
import pymongo
from dotenv import load_dotenv
from googleapiclient.discovery import build
from flask import Flask, render_template, request
import time
from functools import wraps
from threading import Thread

#Set up configuration 
load_dotenv()
api_key = os.environ['API_KEY']
client = pymongo.MongoClient(os.environ['MONGO_CONNECTION_STRING'])
db = client['YOUTUBE']
collection = db['vlogs']

#Create an index to perform search operation
collection.ensure_index([
      ('description', 'text'),
      ('title', 'text'),
  ],
  name="search_index",
  weights={
      'title':100,
      'description':25
  }
)

