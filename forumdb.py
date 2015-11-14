# Udacity.com /ud197 / Intro to Relational Databases
# L3: Python DB-API - Give that App a Backend
# file 2 of 2

# Assignment:
# Modify the GetAllPosts and AddPosT functions in the forumdb.py file to use database.
# The forumdb module is where the database interface code goes.

# Database access functions for the web forum.
import time
import psycopg2

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    DB = psycopg2.connect("dbname=forum")
    cursor = DB.cursor()

    #cursor.execute("DELETE FROM posts")
    cursor.execute("SELECT * FROM posts order by time desc")
    posts = ({'content': str(row[1]), 'time': str(row[0])} for row in cursor.fetchall())
    DB.close()
    return posts

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    t = time.strftime('%c', time.localtime())
    DB = psycopg2.connect("dbname=forum")
    cursor = DB.cursor()
    cursor.execute("INSERT into posts (content,time) VALUES ('%s', '%s')" % (content,t))
    DB.commit()
    DB.close()
