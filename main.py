from fastapi import FastAPI

from routes.upload import router as upload_router
from routes.schedule_upload import router as schedule_upload_router
from routes.swap import router as swap_router
from routes.confirm import router as confirm_router

app = FastAPI()# This is your server instance
app.include_router(upload_router)# This connects /upload to your app
app.include_router(schedule_upload_router)
app.include_router(swap_router)# takes all endpoints inside swap_router and attach them to the main app
app.include_router(confirm_router)


@app.get("/")
def root():
    return {"message": "Backend"}
