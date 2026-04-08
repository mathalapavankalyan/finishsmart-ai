# FinishSmart AI

## Project Overview

FinishSmart AI is a task and calendar management assistant powered by AI. It helps users create tasks, schedule meetings, and take notes. The system uses multiple specialized agents that work together under a primary coordinator agent to handle user requests efficiently.

The project is built using **FastAPI** for the web server and **Google ADK (AI Developer Kit)** for agent orchestration. Data is stored in a **Google AlloyDB** database, providing reliable and secure storage for tasks, events, and notes.

---

## Features

- **Task Management**: Create, view, and manage tasks.
- **Calendar Scheduling**: Schedule events and meetings.
- **Notes Management**: Save important notes for reference.
- **Agent Coordination**: Multiple specialized agents handle tasks, calendar events, and notes under a single primary agent.
- **Database Integration**: Stores tasks, events, and notes in AlloyDB for persistence.

---

## Architecture

The solution consists of the following layers:

1. **FastAPI Web Server**: Receives user requests via a REST API (`/chat` endpoint).
2. **Primary Agent (`finishsmart_primary`)**: Routes requests to sub-agents.
3. **Sub-Agents**:
    - `task_agent` – handles task creation.
    - `calendar_agent` – handles scheduling meetings/events.
    - `notes_agent` – handles note-taking.
4. **Database Layer**: Google AlloyDB stores all tasks, events, and notes securely.
5. **Cloud Deployment**: The project is deployed on **Google Cloud Run**, making it accessible via a public URL.

---

## Setup Instructions

### Prerequisites
- Python 3.12
- Google Cloud project with **AlloyDB** and **Cloud Run** enabled
- Google ADK installed (`google-adk` package)
- Virtual environment recommended

### Local Setup

1. Clone the repository:
    ```bash
    git clone <your-repo-url>
    cd finishsmart
    ```

2. Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. Install dependencies:
    ```bash
    pip install --upgrade pip
    pip install -r requirements.txt
    pip install uvicorn[standard] fastapi psycopg2-binary google-adk
    ```

4. Update the `agent.py` file with your AlloyDB credentials:
    ```python
    DB_HOST = "<alloydb-ip>"
    DB_USER = "postgres"
    DB_PASSWORD = "<your-db-password>"
    DB_NAME = "<database-name>"
    ```

5. Run the FastAPI server locally:
    ```bash
    uvicorn agent:app --reload --host 0.0.0.0 --port 8080
    ```

6. Test the `/chat` endpoint:
    ```bash
    curl -X POST http://127.0.0.1:8080/chat \
        -H "Content-Type: application/json" \
        -d '{"message":"Create a task to finish report and schedule meeting tomorrow"}'
    ```

---

## Cloud Deployment

1. Make sure your Google Cloud project is configured and the ADK CLI (`uvx`) is installed.
2. Deploy to Cloud Run:
    ```bash
    uvx --from google-adk==1.14.0 adk deploy cloud_run \
        --project=<PROJECT_ID> \
        --region=<REGION> \
        --service_name=finishsmart-api \
        --with_ui \
        . \
        -- \
        --labels=dev-tutorial=codelab-adk \
        --service-account=<SERVICE_ACCOUNT>
    ```
3. After deployment, the CLI will provide a **Cloud Run URL** to access your agent online.

---

## Database Verification

- **Check tables**:
    ```sql
    \dt
    ```
- Tables include:
    - `tasks`
    - `events`
    - `notes`
- Make sure your agents are storing data correctly by inserting a task or note and verifying it appears in the database.

---

## Project Structure


                finishsmart/
├── agent.py # Main agent orchestration and FastAPI server

├── requirements.txt # Python dependencies

├── init.py

├── diagrams/ # Architecture, wireframes, and process diagrams

├── test_db.py # Script to test database connection

└── README.md


---

## Conclusion

FinishSmart AI integrates AI-powered agents, a FastAPI server, and Google AlloyDB to provide a smart task and calendar assistant. The solution is modular, scalable, and can be extended with more sub-agents for additional functionality. Deployment on Cloud Run ensures secure, accessible, and serverless operation.
