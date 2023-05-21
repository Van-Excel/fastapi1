# import FastAPI class which contains all functionality
from fastapi import FastAPI, HTTPException
from typing import List
from models import User, Gender, Role, UserUpdateRequest
from uuid import uuid4, UUID


# create an instance of the FastAPI class

app = FastAPI()


db: List[User] = [
    User(
        id=uuid4(),
        first_name='Van',
        last_name='Ahmed',
        gender=Gender.male,
        roles=[Role.admin],

    ),

    User(
        id=uuid4(),
        first_name='Adjoa',
        last_name='Kesewaa',
        gender=Gender.female,
        roles=[Role.admin, Role.user]

    )

]


@app.get("/")
async def root():
    return {'Name': 'Van'}


# sending a get request
@app.get('/api/v1/users')
async def fetch_users():
    return db


# sending a post request
@app.post('/api/v1/users')
async def register_user(user: User):
    db.append(user)
    return {'id': user.id}


@app.delete('/api/v1/users/{user_id}')
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return
    raise HTTPException(
        status_code=404,
        detail=f'user with user id{user_id} not found'
    )


@app.put('/api/v1/users/{user_id}')
async def update_users(user_update: UserUpdateRequest, user_id: UUID):

    # looping through users in database
    for user in db:

        # checking to see if user id is equal to the one in the url parameter
        if user.id == user_id:

            # checking to see if attribute of model used for updating is not empty
            if user_update.first_name is not None:
                # if it isn't we update the state of attribute in database with value
                # in the updateuser class
                user.first_name = user_update.first_name
            if user_update.last_name is not None:
                user.last_name = user_update.first_name
            if user_update.middle_name is not None:
                user.middle_name = user_update.middle_name
            if user_update.roles is not None:
                user.roles = user_update.roles
            return
    raise HTTPException(
        status_code=404,
        detail=f'user with user id{user_id} cannot be found'
    )
