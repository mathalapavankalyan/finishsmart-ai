import os
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from fastapi.concurrency import run_in_threadpool

# -----------------------------
# DATABASE CONNECTION
# -----------------------------
DB_HOST = os.getenv("DB_HOST", "10.10.0.2")
DB_PORT = int(os.getenv("DB_PORT", 5432))
DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root@123")  # Use secret in production

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print("Error connecting to DB:", e)
        raise

# -----------------------------
# TOOLS
# -----------------------------
def create_task(title: str) -> str:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tasks (title) VALUES (%s) RETURNING id;", (title,))
            task_id = cur.fetchone()[0]
            conn.commit()
        return f"Task created with ID {task_id} and title '{title}'."
    finally:
        conn.close()

def schedule_event(title: str) -> str:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO events (title) VALUES (%s) RETURNING id;", (title,))
            event_id = cur.fetchone()[0]
            conn.commit()
        return f"Event scheduled with ID {event_id} and title '{title}'."
    finally:
        conn.close()

def save_note(content: str) -> str:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO notes (content) VALUES (%s) RETURNING id;", (content,))
            note_id = cur.fetchone()[0]
            conn.commit()
        return f"Note saved with ID {note_id}."
    finally:
        conn.close()

# Create FunctionTools
task_tool = FunctionTool(func=create_task)
calendar_tool = FunctionTool(func=schedule_event)
notes_tool = FunctionTool(func=save_note)

# -----------------------------
# SUB-AGENTS
# -----------------------------
task_agent = Agent(
    name="task_agent",
    model="gemini-2.5-flash",
    tools=[task_tool],
)

calendar_agent = Agent(
    name="calendar_agent",
    model="gemini-2.5-flash",
    tools=[calendar_tool],
)

notes_agent = Agent(
    name="notes_agent",
    model="gemini-2.5-flash",
    tools=[notes_tool],
)

# -----------------------------
# PRIMARY AGENT
# -----------------------------
root_agent = Agent(
    name="finishsmart_primary",
    model="gemini-2.5-flash",
    sub_agents=[task_agent, calendar_agent, notes_agent],
)

# -----------------------------
# FASTAPI SERVER
# -----------------------------
app = FastAPI()

class UserInput(BaseModel):
    message: str

@app.post("/chat")
async def chat(user_input: UserInput):
    try:
        result = await run_in_threadpool(root_agent.run, user_input.message)
        return {"response": result.text}
    except AttributeError as e:
        raise HTTPException(status_code=500, detail=f"Method not found. Error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))