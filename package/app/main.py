from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def root():
    return {"message": "FastAPI running on Lambda!"}

# 👇 Add this at the end
handler = Mangum(app)
