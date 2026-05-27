from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
import uuid
from anthropic import Anthropic

from models import SessionLocal, User, Memory, Interaction, Task, DashboardState, init_db

app = FastAPI()

# Initialize database
init_db()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://lily.netlify.app", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Claude client
client = Anthropic()

# Request models
class ContextRequest(BaseModel):
    user_id: str
    topic: str = None

class TaskRequest(BaseModel):
    user_id: str
    title: str
    description: str
    due_date: str = None

class EmailRequest(BaseModel):
    user_id: str
    recipient: str
    subject: str
    topic: str
    tone: str = "professional"

class MemoryRequest(BaseModel):
    user_id: str
    topic: str
    summary: str
    expires_days: int = 30

class AnalysisRequest(BaseModel):
    user_id: str
    data: dict

# Helper: Get or create user
def get_or_create_user(user_id: str, email: str = None):
    db = SessionLocal()
    user = db.query(User).filter(User.user_id == user_id).first()
    if not user:
        user = User(user_id=user_id, email=email or f"{user_id}@lily.ai", name=user_id)
        db.add(user)
        db.commit()
    db.close()
    return user

# Helper: Log interaction
def log_interaction(user_id: str, interaction_type: str, input_text: str, claude_response: str, tools: list = []):
    db = SessionLocal()
    interaction = Interaction(
        interaction_id=str(uuid.uuid4()),
        user_id=user_id,
        interaction_type=interaction_type,
        input_text=input_text,
        claude_response=claude_response,
        tools_called=tools
    )
    db.add(interaction)
    db.commit()
    db.close()

# Health check
@app.get("/health")
def health():
    return {"status": "ok"}

# 1. Get context (recent interactions, memory, open tasks)
@app.post("/api/context")
def get_context(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)
        db = SessionLocal()

        interactions = db.query(Interaction).filter(Interaction.user_id == req.user_id).order_by(Interaction.created_at.desc()).limit(5).all()
        memory = db.query(Memory).filter(Memory.user_id == req.user_id).all()
        open_tasks = db.query(Task).filter(Task.user_id == req.user_id, Task.status != "completed").all()

        db.close()

        return {
            "status": "success",
            "interactions": [{"type": i.interaction_type, "input": i.input_text} for i in interactions],
            "memory": [{"topic": m.topic, "summary": m.summary} for m in memory],
            "open_tasks": [{"title": t.title, "status": t.status} for t in open_tasks]
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 2. List calendar events
@app.post("/api/calendar")
def list_calendar(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)

        # Simulated calendar data (replace with Google Calendar API)
        events = [
            {"time": "9:00 AM", "title": "Deal Review", "description": "Casa Del Sol underwriting"},
            {"time": "11:30 AM", "title": "Broker Call", "description": "DFW market update"},
            {"time": "2:00 PM", "title": "Site Walkthrough", "description": "Main St Renovation"},
            {"time": "4:00 PM", "title": "Offer Deadline", "description": "Submit LOI — Weatherford"}
        ]

        log_interaction(req.user_id, "calendar_fetch", "Fetched calendar events", str(events))

        return {"status": "success", "events": events}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 3. Create task
@app.post("/api/tasks")
def create_task(req: TaskRequest):
    try:
        get_or_create_user(req.user_id)
        db = SessionLocal()

        task = Task(
            task_id=str(uuid.uuid4()),
            user_id=req.user_id,
            title=req.title,
            description=req.description,
            due_date=datetime.fromisoformat(req.due_date) if req.due_date else None,
            status="open"
        )
        db.add(task)
        db.commit()
        db.close()

        log_interaction(req.user_id, "task_created", req.title, f"Task created: {req.title}")

        return {"status": "success", "task_id": task.task_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 4. Draft email
@app.post("/api/email-draft")
def draft_email(req: EmailRequest):
    try:
        get_or_create_user(req.user_id)

        # Use Claude to draft email
        prompt = f"""Draft a {req.tone} email to {req.recipient} about {req.topic} with subject: {req.subject}.
        Return ONLY the email body (no subject line)."""

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )

        email_body = message.content[0].text

        log_interaction(req.user_id, "email_drafted", req.topic, email_body, ["claude_email_draft"])

        return {
            "status": "success",
            "subject": req.subject,
            "body": email_body,
            "recipient": req.recipient
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 5. Get weather
@app.post("/api/weather")
def get_weather(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)

        # Simulated weather data (replace with real API)
        weather = {
            "location": "Dallas, TX",
            "temp": 75,
            "condition": "Overcast",
            "wind": 5,
            "humidity": 87,
            "forecast": [
                {"day": "Thu", "high": 83, "low": 68},
                {"day": "Fri", "high": 92, "low": 72},
                {"day": "Sat", "high": 94, "low": 76}
            ]
        }

        log_interaction(req.user_id, "weather_fetch", "Fetched weather", str(weather))

        return {"status": "success", "weather": weather}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 6. Search CRM (HubSpot)
@app.post("/api/crm-search")
def search_crm(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)

        # Simulated CRM data (replace with HubSpot API)
        deals = [
            {"id": "d1", "name": "Casa Del Sol", "stage": "underwriting", "value": 450000},
            {"id": "d2", "name": "Main St Renovation", "stage": "negotiation", "value": 280000},
            {"id": "d3", "name": "Weatherford LOI", "stage": "proposal", "value": 195000}
        ]

        log_interaction(req.user_id, "crm_search", "Searched CRM", str(deals))

        return {"status": "success", "deals": deals}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 7. Save to memory
@app.post("/api/memory")
def save_to_memory(req: MemoryRequest):
    try:
        get_or_create_user(req.user_id)
        db = SessionLocal()

        memory = Memory(
            memory_id=str(uuid.uuid4()),
            user_id=req.user_id,
            topic=req.topic,
            summary=req.summary,
            expires_at=datetime.utcnow() + timedelta(days=req.expires_days)
        )
        db.add(memory)
        db.commit()
        db.close()

        log_interaction(req.user_id, "memory_saved", req.topic, req.summary)

        return {"status": "success", "memory_id": memory.memory_id}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 8. Generate briefing
@app.post("/api/briefing")
def generate_briefing(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)
        db = SessionLocal()

        interactions = db.query(Interaction).filter(Interaction.user_id == req.user_id).count()
        tasks = db.query(Task).filter(Task.user_id == req.user_id, Task.status == "open").count()

        db.close()

        briefing = {
            "deals_analyzed": interactions // 3,
            "rfis_generated": tasks,
            "emails_drafted": interactions // 2,
            "notifications": 2
        }

        log_interaction(req.user_id, "briefing_generated", "Generated morning briefing", str(briefing))

        return {"status": "success", "briefing": briefing}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 9. Search emails (simulated)
@app.post("/api/emails-search")
def search_emails(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)

        emails = [
            {"from": "broker@dfw.com", "subject": "New listings in buy box", "date": "Today"},
            {"from": "title@company.com", "subject": "Closing docs ready", "date": "Yesterday"},
            {"from": "contractor@build.com", "subject": "Project estimate", "date": "2 days ago"}
        ]

        log_interaction(req.user_id, "emails_search", "Searched emails", str(emails))

        return {"status": "success", "emails": emails}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 10. Analyze data
@app.post("/api/analyze")
def analyze_data(req: AnalysisRequest):
    try:
        get_or_create_user(req.user_id)

        # Use Claude to analyze data
        prompt = f"Analyze this data and provide 3 key insights: {req.data}"

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        analysis = message.content[0].text

        log_interaction(req.user_id, "data_analyzed", str(req.data), analysis, ["claude_analysis"])

        return {"status": "success", "analysis": analysis}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 11. Send message (SMS/Slack)
@app.post("/api/message-send")
def send_message(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)

        # Simulated message send
        log_interaction(req.user_id, "message_sent", "Sent notification", "Message delivered")

        return {"status": "success", "message": "Sent"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 12. Get document
@app.post("/api/document")
def get_document(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)

        doc = {
            "id": "doc123",
            "title": "Casa Del Sol - Underwriting",
            "content": "Document preview...",
            "url": "https://docs.google.com/document/..."
        }

        log_interaction(req.user_id, "document_fetched", "Retrieved document", str(doc))

        return {"status": "success", "document": doc}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 13. Transcribe audio
@app.post("/api/transcribe")
def transcribe_audio(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)

        transcript = {
            "text": "Transcribed meeting notes...",
            "duration": 1200,
            "key_points": ["Action item 1", "Action item 2"]
        }

        log_interaction(req.user_id, "audio_transcribed", "Transcribed audio", transcript["text"])

        return {"status": "success", "transcript": transcript}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 14. Create calendar event
@app.post("/api/calendar-create")
def create_calendar_event(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)

        event = {
            "id": str(uuid.uuid4()),
            "created": True,
            "time": "Tomorrow at 2:00 PM"
        }

        log_interaction(req.user_id, "event_created", "Created calendar event", str(event))

        return {"status": "success", "event": event}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# 15. Execute workflow
@app.post("/api/workflow-execute")
def execute_workflow(req: ContextRequest):
    try:
        get_or_create_user(req.user_id)

        result = {
            "workflow": "executed",
            "status": "completed",
            "actions_taken": 3
        }

        log_interaction(req.user_id, "workflow_executed", "Executed automation", str(result))

        return {"status": "success", "result": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
