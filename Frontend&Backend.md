# 1. Frontend (React)

Role

Acts as the human interaction layer for:

Submitting DevOps / software requirements

Visualizing agent execution

Observing orchestration progress in real time


Key Responsibilities

Capture user story / input

Trigger orchestration pipeline

Render agent activity feed

Display generated code snippets and plans


Important Design Choice

 No hardcoded logic
Frontend is event-driven — it reacts only to backend orchestration events.


# 2. Backend (FastAPI)

Role

The backend is the execution brain.

It:

Receives user requirements

Breaks them into structured tasks

Coordinates agents

Validates outputs

Returns final artifacts

