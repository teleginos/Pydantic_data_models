from fastapi import FastAPI, HTTPException

from pydantic import BaseModel

from typing import List

app = FastAPI()


class User(BaseModel):
    id: int
    username: str
    age: int


users: List[User] = []


@app.get("/users")
async def get_users() -> List[User]:
    return users


@app.post("/user/{username}/{age}")
async def post_user(username: str, age: int) -> User:
    user_id = users[-1].id + 1 if users else 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user


@app.put("/user/{user_id}/{username}/{age}")
async def put_user(user_id: int, username: str, age: int) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user

    raise HTTPException(status_code=404, detail="User was not found")


@app.delete("/user/{user_id}")
async def delete_user(user_id: int) -> User:
    for i, user in enumerate(users):
        if user.id == user_id:
            del_user = users.pop(i)
            return del_user
    raise HTTPException(status_code=404, detail="User was not found")
