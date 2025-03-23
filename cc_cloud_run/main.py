from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from google.cloud import firestore
from typing import Annotated
import datetime

app = FastAPI()

# mount static files
app.mount("/static", StaticFiles(directory="/app/static"), name="static")
templates = Jinja2Templates(directory="/app/template")

# init firestore client
db = firestore.Client()
votes_collection = db.collection("votes")


@app.get("/")
async def read_root(request: Request):
    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================
    tabs_count = 0
    spaces_count = 0

    # stream all votes; count tabs / spaces votes, and get recent votes
    # get all votes from firestore collection
    votes = votes_collection.stream()
    # @note: we are storing the votes in `vote_data` list because the firestore stream closes after certain period of time
    vote_data = []
    for v in votes:
        vote_data.append(v.to_dict())
        vote_dict = v.to_dict()
        if vote_dict["team"] == "TABS":
            tabs_count += 1
        elif vote_dict["team"] == "SPACES":
            spaces_count += 1

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
    return templates.TemplateResponse("index.html", {
        "request": request,
        "tabs_count": tabs_count,
        "spaces_count": spaces_count,
        "recent_votes": []
    })


@app.post("/")
async def create_vote(team: Annotated[str, Form()]):
    if team not in ["TABS", "SPACES"]:
        raise HTTPException(status_code=400, detail="Invalid vote")

    # ====================================
    # ++++ START CODE HERE ++++
    # ====================================
    vote_data = {
        "team": team,
        "time_cast": datetime.datetime.utcnow().isoformat()
    }
    votes_collection.add(vote_data)

    return {"message": "Vote successfully recorded"}

    # ====================================
    # ++++ STOP CODE ++++
    # ====================================
