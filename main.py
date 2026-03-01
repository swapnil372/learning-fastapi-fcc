import random

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI()

class POST(BaseModel):
    title: str
    content: str
    published: bool = True

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
    return {
        "all_posts": my_posts
    }

def find_post(id):
    for post in my_posts:
        if post['id'] == id:
            return post

@app.get("/posts/{id}")
def get_one_post(id: int):
    post = find_post(id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the post with id : {id} was not found")

    return post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: POST):
    post = post.model_dump()
    post['id'] = random.randint(4, 100000)
    my_posts.append(post)
    return {
        "new_post": post
    }

def find_index(id):
    for i, post in enumerate(my_posts):
        if post['id'] == id:
            return i

@app.put("/posts/{id}")
def update_post(id: int, post: POST):
    index = find_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the post with id : {id} was not found")
    updated_post = post.model_dump()
    updated_post['id'] = id
    my_posts[index] = updated_post
    return {
        "updated_post": updated_post
    }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index(id)
    if index == None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"the post with id : {id} was not found")
    
    deleted_post = my_posts.pop(index)
    return {
        "deleted_post": deleted_post
    }
