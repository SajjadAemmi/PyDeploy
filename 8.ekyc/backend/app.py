from datetime import datetime, timedelta
from fastapi import FastAPI, UploadFile, HTTPException, Header, Depends
from celery_tasks import celery_app, face_task, speech_task, gesture_task, national_card_task
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import jwt
from database import User


app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class SignRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(email: dict) -> str:
    to_encode = email.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, "my-secret-key", algorithm="HS256")
    return token


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, "my-secret-key", algorithms=["HS256"])
        return payload.get("email")
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token.")


def get_current_user(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Missing or invalid authorization header"
        )
    token = authorization.split(" ")[1]
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    return email


@app.get("/")
def root():
    return {"Hello": "world"}


@app.post("/signup", status_code=201)
def signup(request: SignRequest):
    if User.objects(email=request.email).first():
        raise HTTPException(status_code=400, detail="Email already registered.")

    hashed_password = get_password_hash(request.password)
    user = User(email=request.email, hashed_password=hashed_password, level=1)
    user.save()
    return {"message": "User registered successfully."}


@app.post("/signin", response_model=TokenResponse)
def signin(request: SignRequest):
    user = User.objects(email=request.email).first()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    access_token = create_access_token(email={"email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/not-protected")
def test1():
    return {
        "message": "Hello everyone"
    }


@app.get("/protected")
def test2(current_user: str = Depends(get_current_user)):
    return {
        "message": f"Hello {current_user}, You have access to this route"
    }

@app.get("/get-user")
def test2(current_user: str = Depends(get_current_user)):
    user = User.objects(email=current_user).first()
    if user:
        return {
            "email": user.email,
            "level": user.level 
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid token.")

@app.post("/signout")
def signout(token: str = Depends(get_current_user)):
    if not token:
        raise HTTPException(status_code=401, detail="Invalid token.")
    return {"message": "Sign-out successful."}


@app.post("/auth/face")
async def face(image_file: UploadFile, current_user: str = Depends(get_current_user)):
    image = await image_file.read()
    task = face_task.delay(image)
    return {
        "task_id": task.id,
        "status": task.status
    }


@app.post("/auth/speech")
async def speech(voice_file: UploadFile, current_user: str = Depends(get_current_user)):
    voice = await voice_file.read()
    task = speech_task.delay(voice)
    return {
        "task_id": task.id,
        "status": task.status
    }


@app.post("/auth/gesture")
async def gesture(image_file: UploadFile, current_user: str = Depends(get_current_user)):
    image = await image_file.read()
    task = gesture_task.delay(image)
    return {
        "task_id": task.id,
        "status": task.status
    }


@app.post("/auth/national-card")
async def national_card(image_file: UploadFile, current_user: str = Depends(get_current_user)):
    image = await image_file.read()
    task = national_card_task.delay(image)
    return {
        "task_id": task.id,
        "status": task.status
    }


@app.get("/check-task")
def check_task(task_id: str):
    result = celery_app.AsyncResult(task_id)
    return {
        "status": result.state,
        "result": result.result
    }
