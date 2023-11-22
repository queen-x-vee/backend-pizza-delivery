from fastapi import APIRouter, status, Depends
#from fastapi.responses import JSONResponse
from database import engine, Session
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder


auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

session = Session(bind=engine)

@auth_router.get("/")
async def hello( Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()


    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")

    return {"message": "Hello World"}

#pydantic is a tool that helps us validate the data that we pass it to an api

@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel): #user of type SignUpModel
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this Email already exists")
    
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this Username already exists")
    
    new_user=User( #new_user is an instance of User
        username=user.username,
        email=user.email,
        password =generate_password_hash(user.password), #we are going to hash password with werkzeug
        is_staff=user.is_staff,
        is_active=user.is_active,
    )

    session.add(new_user)

    session.commit()

    return new_user



#login route

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: LoginModel, Authorize:AuthJWT = Depends()):
    db_user=session.query(User).filter(User.username==user.username).first() 
    
    #if user exists, then provide jwt tokens
    if db_user and check_password_hash(db_user.password, user.password):
        access_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username)

        response={
            "access": access_token,
            "refresh": refresh_token
        }

        return jsonable_encoder(response)
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Username or Password")









