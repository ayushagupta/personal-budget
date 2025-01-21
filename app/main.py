from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def sample_function():
    return {"message": "Hello world"}