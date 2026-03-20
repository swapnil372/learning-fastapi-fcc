from fastapi import Depends, FastAPI, HTTPException, status
from . import models, schemas
from .database import engine, get_db
from typing import List

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

@app.get("/")
def home_page(db = Depends(get_db)):
    return "successfully connected to the database"


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db = Depends(get_db)):
    posts = db.query(models.Post).all()
    # print the SQL command with print(db.query(models.Post))
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    return post


@app.post("/posts", response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.delete("/posts/{id}", response_model=schemas.Post)
def delete_post(id: int, db = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    db.delete(post)
    db.commit()
    return post


@app.put('/posts/{id}', response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    # the above includes all the posts with the given id, but since id is unique, it will only return one post
    existing_post = post_query.first()
    if existing_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found")
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()