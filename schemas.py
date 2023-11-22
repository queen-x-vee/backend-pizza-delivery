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


class Settings(BaseModel):
     authjwt_secret_key: str='a0076b92217c27dd15701b85280212aa99fb52c0c48011a42b7f8081eed92a97' #to generate this toke, open terminal and type python, then import secrets, then secrets.token_hex()


class LoginModel(BaseModel):
     username: str
     password: str
