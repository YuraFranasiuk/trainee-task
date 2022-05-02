from sqlalchemy import Column
from sqlalchemy.orm import Session

import models, schemas


def create_user(db: Session, user: schemas.UserBase):
    db_user = models.User(**user.dict())

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(
        models.User.username == username
    ).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(
        models.User.email == email
    ).first()

def update_user_password(db: Session, id: str, password: str):
    res = db.query(models.User).filter(
        models.User.id == id
    ).update({models.User.password: password})
    db.commit()

    return res

def delete_user(db: Session, id: int):
    res = db.query(models.User).filter(models.User.id == id).delete()
    db.commit()

    return res

def get_users(db: Session):
    return db.query(models.User).all()
