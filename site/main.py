from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from apscheduler.schedulers.background import BackgroundScheduler
from os import getenv
from get_data_graph import get_data_graphs, update_global_times
import config

scheduler = BackgroundScheduler()
templates = Jinja2Templates(directory="templates")
scheduler.add_job(get_data_graphs, "cron", day_of_week="sun", hour=1)
scheduler.start()

app = FastAPI()
ADMIN_KEY = config.get("ADMIN_KEY")
FATHOM_HOST = getenv("FATHOM_HOST")
FATHOM_SITE_ID = getenv("FATHOM_SITE_ID")


def verify_admin_key(req: Request):
    if req.headers.get("Admin-Key") != ADMIN_KEY:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")


@app.post("/admin/run")
async def force_run(req: Request):
    verify_admin_key(req)
    update_global_times()
    get_data_graphs()
    return {"info": "Done"}


@app.get("/")
async def home(req: Request):
    update_global_times()
    return templates.TemplateResponse(
        "index.html.j2",
        {"request": req, "fathom_host": FATHOM_HOST, "fathom_site_id": FATHOM_SITE_ID},
    )


app.mount("/", StaticFiles(directory="static", html=True), name="static")
