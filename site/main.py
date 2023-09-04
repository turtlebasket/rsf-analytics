from fastapi import FastAPI, HTTPException, Request, status
from fastapi.staticfiles import StaticFiles
from apscheduler.schedulers.background import BackgroundScheduler
from get_data_graph import get_data_graphs
import config

scheduler = BackgroundScheduler()
scheduler.add_job(get_data_graphs, 'cron', day_of_week='sun', hour=1)
scheduler.start()

app = FastAPI()
ADMIN_KEY = config.get("ADMIN_KEY")

def verify_admin_key(req: Request):
    if req.headers.get("Admin-Key") != ADMIN_KEY:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Unauthorized")

@app.post("/admin/run")
async def force_run(req: Request):
    verify_admin_key(req)
    get_data_graphs()
    return {"info": "Done"}

app.mount("/", StaticFiles(directory="static", html=True), name="static")
