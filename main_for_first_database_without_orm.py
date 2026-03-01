import random
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor

app = FastAPI()

class POST(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    conn = psycopg2.connect(host='localhost', database='socialmedia', user='postgres', password='password12345', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("connection is successful")
except Exception as error:
    print("error: ", error)

my_posts = [
    {
        "id": 1,
        "title": "post 1",
        "content": "content of post 1",
        "published": True
    },
    {
        "id": 2,
        "title": "post 2",
        "content": "content of post 2",
        "published": False
    },
    {
        "id": 3,
        "title": "post 3",
        "content": "content of post 3",
        "publiished": True
    }
]

@app.get("/posts")
def get_all_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {
        "all_posts": posts
    }

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

@app.get("/posts/{id}")
def get_one_post(id: int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (id,))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the post with id : {id} was not found")
    return post

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: POST):
    cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    post = cursor.fetchone()
    conn.commit()
    return {
        "new_post": post
    }

def find_index(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i

@app.put("/posts/{id}")
def update_post(id: int, post: POST):
    cursor.execute(""" UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *  """, (post.title, post.content, post.published, id))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"the post was not found with id { id }")
    return {
        "updated_post": updated_post 
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (id, ))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the post with id : {id} was not found")
    return {
        "deleted_post": deleted_post
    }
