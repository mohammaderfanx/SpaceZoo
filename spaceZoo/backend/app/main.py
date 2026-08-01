from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DB_PATH = os.path.join(PROJECT_ROOT, "game.db")

app = FastAPI(title="Game Framework")
app.mount("/static", StaticFiles(directory=os.path.join(PROJECT_ROOT, "static")), name="static")

templates = Jinja2Templates(directory=os.path.join(PROJECT_ROOT, "templates"))

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Score(Base):
    __tablename__ = "scores"
    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    db = SessionLocal()
    try:
        scores = db.query(Score).order_by(Score.score.desc()).limit(10).all()
    finally:
        db.close()
    return templates.TemplateResponse("index.html", {"request": request, "scores": scores})

@app.post("/submit")
async def submit_score(player_name: str = Form(...), score: int = Form(...)):
    db = SessionLocal()
    try:
        db.add(Score(player_name=player_name, score=score))
        db.commit()
    finally:
        db.close()
    return RedirectResponse(url="/", status_code=303)

@app.get("/health")
def health():
    return {"status": "ok"}
