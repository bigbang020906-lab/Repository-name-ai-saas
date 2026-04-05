
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import time, jwt

SECRET = "secret123"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users = {}

class User(BaseModel):
    username: str
    password: str

class Prompt(BaseModel):
    text: str

def create_token(username):
    return jwt.encode({"user": username}, SECRET, algorithm="HS256")

def get_user(token: str):
    try:
        data = jwt.decode(token, SECRET, algorithms=["HS256"])
        return data["user"]
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/auth/register")
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="User exists")
    users[user.username] = {"password": user.password, "credits": 10}
    return {"msg": "Registered"}

@app.post("/auth/login")
def login(user: User):
    if user.username not in users or users[user.username]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid")
    token = create_token(user.username)
    return {"token": token}

@app.get("/user")
def get_user_data(token: str):
    username = get_user(token)
    return users[username]

@app.post("/generate")
def generate(prompt: Prompt, token: str):
    username = get_user(token)

    if users[username]["credits"] <= 0:
        raise HTTPException(status_code=403, detail="Out of credits")

    users[username]["credits"] -= 1

    # FAKE AI (replace with OpenRouter)
    result = f"[AI FREE] Generated: {prompt.text} - {time.time()}"

    return {"result": result, "credits": users[username]["credits"]}
