from fastapi import FastAPI, Request

app: FastAPI = FastAPI()

@app.get("/")
def hello_world():
	return {"hello": "world"}

	