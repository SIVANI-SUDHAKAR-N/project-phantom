from fastapi import FastAPI
from parser.project_analyzer import analyze_project

app = FastAPI(title="Project Phantom")


@app.get("/")
def home():
    return {
        "message": "👻 Phantom is alive!"
    }


@app.get("/analyze")
def analyze():
    return analyze_project("parser")