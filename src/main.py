from fastapi import FastAPI

app = FastAPI(title="CannaTracker")


@app.get("/login")
async def login():
    return {"message": "Hello World"}

@app.post("/register")
async def register():
    return {"message": "Hello World"}

@app.post("/plants")
async def create_plant():
    return {"message": "Hello World"}

@app.get("/plants/{plant}")
async def get_plant(plant):
    return {"message": "Hello World"}
