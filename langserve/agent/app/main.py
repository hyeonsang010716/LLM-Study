from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def hello():
    return {"messages": "Hello"}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)