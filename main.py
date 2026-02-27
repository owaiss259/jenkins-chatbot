from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from service import trigger_pipeline

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/chat")
def chat(request: ChatRequest):
    try:
        if request.message.lower() == "food":
            success = trigger_pipeline()

            if success:
                return {"reply": "Pipeline triggered successfully."}
            else:
                return {"reply": "Pipeline trigger failed. Check terminal logs."}

        return {"reply": "Invalid command"}

    except Exception as e:
        return {"reply": f"Server error: {str(e)}"}