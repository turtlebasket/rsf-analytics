from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.post("/admin/run")
async def force_run():
    return {"info": "Running"}

app.mount("/", StaticFiles(directory="static"), name="static")
