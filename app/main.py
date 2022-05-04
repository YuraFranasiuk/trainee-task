from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine, Base
import crud, schemas


Base.metadata.create_all(engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/create-user', response_model=schemas.User)
def create_user(data: schemas.UserCreate, db: Session=Depends(get_db)):
    username_exist = crud.get_user_by_username(db, data.username)
    email_exist = crud.get_user_by_email(db, data.email)

    if username_exist and email_exist:
        raise HTTPException(status_code=400,
                            detail='username and email already registered')

    if username_exist:
        raise HTTPException(status_code=400, 
                            detail='username already registered')

    if email_exist:
        raise HTTPException(status_code=400, 
                            detail='email already registered')
    
    return crud.create_user(db, data)

@app.put('/update-password')
def update_password(data: schemas.UserUpdatePassword,
                    db: Session=Depends(get_db)):
    res = crud.update_user_password(db, **data.dict())

    if res == 0:
        raise HTTPException(status_code=400, 
                            detail='user not found')
    if res == 1:
        return {'result': 'password successful updated'}
    
@app.delete('/delete-user')
def delete_user(data: schemas.UserDelete, db: Session=Depends(get_db)):
    res = crud.delete_user(db, **data.dict())

    if res == 0:
        raise HTTPException(status_code=400, 
                            detail='user not found')
    if res == 1:
        return {'result': 'user successful deleted'}

@app.get('/get-user-list', response_model=list[schemas.User])
def get_user_list(db: Session=Depends(get_db)):
    return crud.get_users(db)

@app.post('/search', response_model=schemas.User)
def search(data: schemas.UserSearch, db: Session=Depends(get_db)):
    res = crud.get_user_by_username(db, data.username)

    if not res:
        raise HTTPException(status_code=400, 
                            detail='user not found')

    return res
