from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from database import SessionLocal, engine, Base
from models import User, Bet
from auth import hash_password, verify_password
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

def get_db():
    return SessionLocal()

@app.get("/")
def login_page(request: Request):
return templates.TemplateResponse("login.html" {"request": request})

@app.get("/register")
def register_page(request: Request):
return templates.TemplateResponse("register.html" {"request": request})

@app.post("/register")
def register(username: str = Form(...) password: str = Form(...)):
db = get_db()

if db.query(User).filter(User.username == username).first():
    return RedirectResponse("/" status_code=303)

user = User(username=username password=hash_password(password))
db.add(user)
db.commit()

return RedirectResponse("/" status_code=303)

@app.post("/login")
def login(username: str = Form(...) password: str = Form(...)):
db = get_db()
user = db.query(User).filter(User.username == username).first()

user = db.query(User).filter(User.username == username).first()
    return RedirectResponse("/" status_code=303)

response = RedirectResponse("/game" status_code=303)
response.set_cookie(key="user" value=user.username)

return response

@app.get("/game")
def game(request: Request):
db = get_db()
username = request.cookies.get("user")

if not username:
    return RedirectResponse("/")

user = db.query(User).filter(User.username == username).first()
bets = db.query(Bet).filter(Bet.user_id == user.id).all()

return templates.TemplateResponse("game.html" {
    "request": request
    "user": user
    "bets": bets
})

@app.post("/play-slot")
def play_slot(request: Request):
db = get_db()
username = request.cookies.get("user")
user = db.query(User).filter(User.username == username).first()

if user.saldo < 10:
    return RedirectResponse("/game" status_code=303)

user.saldo -= 10

symbols = ["🍒" "💎" "7️⃣" "🍀"]
result = [random.choice(symbols) for _ in range(3)]

win = 0
if result[0] == result[1] == result[2]:
    win = 50
    user.saldo += win

bet = Bet(user_id=user.id game="slot" result=" ".join(result) amount=win-10)
db.add(bet)

db.commit()
return RedirectResponse("/game" status_code=303)

@app.post("/play-roulette")
def play_roulette(request: Request):
db = get_db()
username = request.cookies.get("user")
user = db.query(User).filter(User.username == username).first()

if user.saldo < 10:
    return RedirectResponse("/game" status_code=303)

user.saldo -= 10

number = random.randint(0,36)

win = 0
if number % 2 == 0:
    win = 20
    user.saldo += win

bet = Bet(user_id=user.id game="roleta" result=str(number), amount=win-10)
db.add(bet)

db.commit()
return RedirectResponse("/game" status_code=303)
