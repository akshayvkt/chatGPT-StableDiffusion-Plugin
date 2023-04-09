import json
import os
import base64
from typing import Optional

import replicate
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse

app = FastAPI()

REPLICATE_API_TOKEN = os.environ['REPLICATE_API_TOKEN']


@app.get("/")
async def hello_world():
  return "Hello, welcome to the ChatGPT image generation plugin! Go to chat.openai.com and paste the URL."


@app.post("/generate-image")
async def generate_image(prompt: str):
  model_name = "stability-ai/stable-diffusion:db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf"

  api_token = os.environ.get("REPLICATE_API_TOKEN")
  if not api_token:
    raise HTTPException(
      status_code=500,
      detail="REPLICATE_API_TOKEN environment variable not set")

  output = replicate.run(model_name, input={"prompt": prompt})

  return JSONResponse(content=output, status_code=200)


@app.get("/logo.png")
async def plugin_logo():
  return FileResponse('logo.png')


@app.get("/.well-known/ai-plugin.json")
async def plugin_manifest(request: Request):
  host = request.headers['host']
  with open("ai-plugin.json") as f:
    text = f.read().replace("PLUGIN_HOSTNAME", f"https://{host}")
  return JSONResponse(content=json.loads(text))


@app.get("/openapi.json")
async def custom_openapi():
  return JSONResponse(content=get_openapi(
    title="Image Generation Plugin", version="1.0.0", routes=app.routes))


if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=5002)
