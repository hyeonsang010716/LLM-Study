from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_root():
    return {"messages": "Hello world"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)