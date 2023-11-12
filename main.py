from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name='Bob', pk=0, kind='terrier'),
    1: Dog(name='Marli', pk=1, kind="bulldog"),
    2: Dog(name='Snoopy', pk=2, kind='dalmatian'),
    3: Dog(name='Rex', pk=3, kind='dalmatian'),
    4: Dog(name='Pongo', pk=4, kind='dalmatian'),
    5: Dog(name='Tillman', pk=5, kind='bulldog'),
    6: Dog(name='Uga', pk=6, kind='bulldog')
}

post_db = [
    Timestamp(id=0, timestamp=12),
    Timestamp(id=1, timestamp=10)
]


@app.get('/')
def root() -> str:
    return "Welcome!"


@app.post('/post', response_model=Timestamp, summary='Get Post')
def get_post():
    new_id = max(ts.id for ts in post_db) + 1
    new_timestamp: Timestamp = Timestamp(id=new_id, timestamp=int(round(datetime.now().timestamp())))
    post_db.append(new_timestamp)
    return new_timestamp


@app.get('/dog', response_model=List[Dog], summary='Get Dogs')
def get_dogs(kind: DogType):
    res = []
    for dog in dogs_db.values():
        if dog.kind == kind:
            res.append(dog)
    return res


@app.get('/dog/{pk}', response_model=Dog, summary='Get Dog By Pk')
def get_dog_by_pk(pk: int):
    for dog in dogs_db.values():
        if dog.pk == pk:
            return dog


@app.post('/dog', response_model=Dog, summary='Create Dog')
def create_dog(dog: Dog):
    new_key = max(dogs_db) + 1
    dogs_db[new_key] = dog
    return dog


@app.patch('/dog/{pk}', response_model=Dog, summary='Update Dog')
def update_dog(pk: int, dog: Dog):
    dogs_db[pk] = dog
    return dog