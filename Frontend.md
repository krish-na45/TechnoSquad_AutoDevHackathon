 1. Frontend (React)

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


Key Files

frontend/
├── src/
│   ├── App.jsx              → Main application container
│   ├── components/
│   │   ├── InputPanel.jsx   → User requirement input
│   │   ├── AgentFeed.jsx    → Agent activity feed UI
│   │   ├── Orchestration.jsx → Live orchestration graph
│   │   └── CodeViewer.jsx   → Generated code preview
│   └── api.js               → Backend API calls

Important Design Choice

 No hardcoded logic
Frontend is event-driven — it reacts only to backend orchestration events.
