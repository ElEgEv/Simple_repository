from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File
from typing import Optional, Annotated
from datetime import timedelta

from config import Config
from src.core.repository import user_repository
from src.core.models.models import User
from src.secure.main_secure import role_required, create_token, OAuth2PasswordRequestForm, authenticate_user, verify_token
from src.utils.file_operation import check_image_formant
from src.secure.secure_entity import Role


config = Config()

ACCESS_TOKEN_EXPIRE_MINUTES = int(config.__getattr__("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_DAYS = int(config.__getattr__("REFRESH_TOKEN_EXPIRE_DAYS"))


router = APIRouter(
    prefix="/api/users",
    tags=["Users CRUD"],
)


# get token
@router.post("/auth")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login or password")
    
    access_token = create_token({"sub": form_data.username, "role": user["role"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token({"sub": form_data.username}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh")
def refresh_token(refresh_token: str):
    payload = verify_token(refresh_token)
    user_email = payload.get("sub")

    if not user_email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    
    user = user_repository.get_user_by_email(user_email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_access_token = create_token({"sub": user["login"], "role": user["role"]}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return {"access_token": new_access_token, "token_type": "bearer"}


@router.get("/")
async def get_users(secure_data: dict = Depends(role_required(Role.ADMIN))):
    page = user_repository.get_all_users()
    return page


@router.get("/{id}")
async def get_user_by_id(id: int, secure_data: dict = Depends(role_required(Role.USER))):
    user = user_repository.get_user_by_id(id)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    return user


@router.get("/login/")
async def get_user_by_email(login: str, secure_data: dict = Depends(role_required(Role.USER))):
    user = user_repository.get_user_by_email(login)
    
    if not user:
        raise HTTPException(status_code=404, detail=f"User with login {login} not found")
    
    return user


@router.post("/register")
async def create_user(
    login: Annotated[str, Form()] = None,
    password: Annotated[str, Form()] = None,
    avatar: Optional[UploadFile] = File(None)
):
    if avatar:
        result = check_image_formant([avatar])

        if not result:
            raise HTTPException(status_code=500, detail={
                    "status": "error",
                    "msg": f"All image must be in png/jpg/jpeg format"
                })
            
    create_user = user_repository.create_user(User(login=login, password=password), avatar)

    if not create_user:
        raise HTTPException(status_code=500, detail=f"User with this login already exists")
    
    access_token = create_token({"sub": create_user['login'], "role": create_user['role']}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_token({"sub": create_user['login']}, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS))

    return {
        "message" : "User create success",
        "data" : create_user,
        "access_token": access_token, 
        "refresh_token": refresh_token, 
        "token_type": "bearer"
    }


@router.put("/update")
async def update_user(
    id: Annotated[int, Form()] = None,
    login: Annotated[str, Form()] = None,
    password: Annotated[str, Form()] = None,
    cur_avatar: Annotated[str, Form()] = None,
    avatar: Optional[UploadFile] = File(None),
    secure_data: dict = Depends(role_required(Role.USER))
):
    if avatar:
        result = check_image_formant([avatar])

        if not result:
            raise HTTPException(status_code=500, detail={
                    "status": "error",
                    "msg": f"All image must be in png/jpg/jpeg format"
                })
    
    user = User(id=id, login=login, password=password, avatar=cur_avatar)
    
    result = user_repository.update_user(id, user, avatar)

    if not result:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return  {
        "message" : f"User with id {id} update success",
        "data" : result
    }


@router.delete("/{id}")
async def delete_user(id: int, secure_data: dict = Depends(role_required(Role.ADMIN))):
    result = user_repository.delete_user_by_id(id)
    
    if not result:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")

    return {"message" : "User delete success"}