#this schema is to help us validate the data
from pydantic import BaseModel
from typing import Optional

class SignUpModel(BaseModel):
     id: Optional[int]
     username: str
     email: str
     password: str
     is_staff:Optional[bool]
     is_active: Optional[bool]
     #orders = relationship("Order", back_populates="user")
     #sqlalchemy is the orm in this project

     class Config:
          orm_mode = True
          schema_extra = {
               "example": {
                    "username": "test",
                    "email": "test@email.com",
                    "password": "password",
                    "is_staff": False,
                    "is_active": True,
               }
          }