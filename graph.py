from typing import TypedDict, List
from langgraph.graph import StateGraph, END


class AgentState(TypedDict, total=False):
    user_story: str
    ado_payload: str
    refined_story: str
    plan: str
    backend_code: str
    frontend_code: str
    db_schema: str
    legacy_analysis: str
    test_results: str
    deployment_status: str
    retry_count: int
    current_status: str
    logs: List[str]


def _append_log(state: AgentState, message: str) -> AgentState:
    logs = list(state.get("logs", []))
    logs.append(message)
    state["logs"] = logs
    return state


def initial_state_from_user_story(
    user_story: str, use_sample_payload: bool = True
) -> AgentState:
    state: AgentState = {
        "user_story": user_story.strip(),
        "retry_count": 0,
        "logs": [],
        "current_status": "Waiting for orchestration",
    }
    if use_sample_payload:
        sample = {
            "id": 101,
            "title": "Exam Form UI with FastAPI backend",
            "description": user_story.strip(),
            "areaPath": "AutoDev/Frontend-Backend",
            "iterationPath": "Sprint 3",
        }
        state["ado_payload"] = str(sample)
    return state


def ado_connector(state: AgentState) -> AgentState:
    state["current_status"] = "Parsing ADO user story"
    if not state.get("user_story"):
        return _append_log(state, "No user story provided – nothing to do.")
    _append_log(
        state,
        "ADO Connector: Ingested user story and created a normalized payload.",
    )
    if "Exam" in state["user_story"] or "exam" in state["user_story"]:
        _append_log(state, "ADO tags: [exam-form, fastapi, postgres, ui].")
    return state


def synapse_orchestrator(state: AgentState) -> AgentState:
    state["current_status"] = "Deriving high‑level build plan"
    story = state.get("user_story", "")
    plan_lines = [
        "1. Clarify functional scope and inputs from the user story.",
        "2. Design DB schema for submissions table.",
        "3. Generate FastAPI backend with CRUD endpoints.",
        "4. Generate React UI bound to backend API.",
        "5. Run automated tests on generated backend stub.",
        "6. Patch legacy exam module without breaking old flows.",
        "7. Prepare deployable artefacts.",
    ]
    state["plan"] = "\n".join(plan_lines)
    _append_log(
        state,
        "Synapse Orchestrator: Generated build plan and routed work to Meta‑Refiner.",
    )
    return state


def meta_refiner(state: AgentState) -> AgentState:
    state["current_status"] = "Refining requirements"
    story = state.get("user_story", "")
    refined = (
        "Normalized requirement: Build a small full‑stack exam registration module with "
        "a FastAPI backend, PostgreSQL persistence and a React/HTML frontend. "
        "The system must expose a POST endpoint to create exam registrations and "
        "a GET endpoint to list all registrations."
    )
    if "slot" in story.lower():
        refined += " The UI should allow the student to choose a preferred exam slot (morning/afternoon)."
    state["refined_story"] = refined
    _append_log(
        state,
        "Meta‑Refiner: Eliminated ambiguity and produced a concise engineering-ready requirement.",
    )
    return state


def db_architect(state: AgentState) -> AgentState:
    state["current_status"] = "Designing DB schema"
    schema = """
CREATE TABLE exam_registrations (
    id SERIAL PRIMARY KEY,
    student_name VARCHAR(120) NOT NULL,
    email VARCHAR(200) NOT NULL,
    exam_code VARCHAR(40) NOT NULL,
    preferred_slot VARCHAR(40),
    created_at TIMESTAMPTZ DEFAULT NOW()
);
""".strip()
    state["db_schema"] = schema
    _append_log(
        state, "DB Architect: Proposed PostgreSQL schema for exam_registrations table."
    )
    return state


def backend_coder(state: AgentState) -> AgentState:
    state["current_status"] = "Authoring FastAPI backend"
    backend_code = """
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI(title="Exam Registration API")


class ExamRegistration(BaseModel):
    student_name: str
    email: str
    exam_code: str
    preferred_slot: str | None = None


_fake_db: List[ExamRegistration] = []


@app.post("/registrations")
def create_registration(payload: ExamRegistration) -> dict:
    _fake_db.append(payload)
    return {"status": "ok", "total": len(_fake_db)}


@app.get("/registrations")
def list_registrations() -> List[ExamRegistration]:
    return _fake_db


@app.get("/")
def health() -> dict:
    return {"service": "exam-reg-api", "status": "healthy"}
""".strip()
    state["backend_code"] = backend_code
    _append_log(
        state,
        "Backend Coder: Generated FastAPI service with health, create and list endpoints.",
    )
    return state


def frontend_coder(state: AgentState) -> AgentState:
    state["current_status"] = "Authoring frontend UI"
    frontend_code = """
import React, { useState, useEffect } from "react";


export default function ExamForm() {
  const [form, setForm] = useState({
    student_name: "",
    email: "",
    exam_code: "",
    preferred_slot: "",
  });


  const [status, setStatus] = useState("");
  const [items, setItems] = useState([]);


  const handleChange = (ev) => {
    setForm({ ...form, [ev.target.name]: ev.target.value });
  };


  const submit = async (ev) => {
    ev.preventDefault();
    setStatus("Submitting...");
    const res = await fetch("http://localhost:8000/registrations", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    setStatus("Saved. Total registrations: " + data.total);
    await loadItems();
  };


  const loadItems = async () => {
    const res = await fetch("http://localhost:8000/registrations");
    const data = await res.json();
    setItems(data);
  };


  useEffect(() => {
    loadItems();
  }, []);


  return (
    <div className="p-6 max-w-xl mx-auto space-y-4">
      <h1 className="text-2xl font-semibold">Exam Registration</h1>
      <form onSubmit={submit} className="space-y-2">
        <input
          name="student_name"
          placeholder="Student name"
          onChange={handleChange}
          className="border px-2 py-1 w-full"
        />
        <input
          name="email"
          placeholder="Email"
          onChange={handleChange}
          className="border px-2 py-1 w-full"
        />
        <input
          name="exam_code"
          placeholder="Exam code"
          onChange={handleChange}
          className="border px-2 py-1 w-full"
        />
        <select
          name="preferred_slot"
          onChange={handleChange}
          className="border px-2 py-1 w-full"
        >
          <option value="">Select slot</option>
          <option value="morning">Morning</option>
          <option value="afternoon">Afternoon</option>
        </select>
        <button type="submit" className="px-3 py-1 rounded bg-black text-white">
          Submit
        </button>
      </form>
      <p>{status}</p>
      <ul className="text-sm list-disc pl-5">
        {items.map((row, idx) => (
          <li key={idx}>
            {row.student_name} – {row.exam_code} ({row.preferred_slot || "no slot"})
          </li>
        ))}
      </ul>
    </div>
  );
}
""".strip()
    state["frontend_code"] = frontend_code
    _append_log(
        state,
        "Frontend Coder: Generated React component wired to FastAPI endpoints.",
    )
    return state


def legacy_agent(state: AgentState) -> AgentState:
    state["current_status"] = "Analysing legacy code"
    template = """
# legacy_exam_module.py (excerpt)


def render_dashboard(user):
    # Existing implementation ...
    pass


# AUTO-DEV-INJECT-HERE: safe extension point for new registration link
""".strip()
    # Use single quotes for the inner docstring to avoid ending the outer triple double-quoted string
    patch_notes = (
        "# Suggested patch for legacy_exam_module.py\n\n"
        f"{template}\n\n"
        "def add_exam_registration_entrypoint():\n"
        "    '''Hook to open the new exam registration micro‑frontend.'''\n"
        "    return '/exam/registration'\n"
    )
    state["legacy_analysis"] = patch_notes
    _append_log(
        state,
        "Legacy Agent: Located safe injection point in legacy_exam_module.py and suggested patch.",
    )
    return state


def sentinel_tester(state: AgentState) -> AgentState:
    state["current_status"] = "Running automated checks"
    code = state.get("backend_code", "")
    errors: List[str] = []

    if "FastAPI" not in code:
        errors.append("Backend does not import FastAPI.")
    if '@app.post("/registrations")' not in code:
        errors.append("Missing POST /registrations endpoint.")
    if "health" not in code:
        errors.append("Missing health check endpoint.")

    retry_count = int(state.get("retry_count", 0))

    if errors:
        retry_count += 1
        state["retry_count"] = retry_count
        msg = f"❌ TESTS FAIL on attempt {retry_count}: " + "; ".join(errors)
        state["test_results"] = msg
        _append_log(state, msg)
    else:
        msg = "✅ TESTS PASS: Backend structure and key endpoints validated."
        state["test_results"] = msg
        _append_log(state, msg)

    return state


def test_router(state: AgentState) -> str:
    if "FAIL" in state.get("test_results", ""):
        if int(state.get("retry_count", 0)) >= 2:
            return "max_retries"
        return "retry"
    return "success"


def deployment_engine(state: AgentState) -> AgentState:
    state["current_status"] = "Preparing deployment artefacts"
    if "FAIL" in state.get("test_results", ""):
        msg = (
            "⚠️ Deployment skipped: tests still failing after max retries. "
            "Hand‑off to human reviewer."
        )
    else:
        msg = (
            "✅ Deployment package ready: Dockerfile + FastAPI app + "
            "generated React component."
        )
    state["deployment_status"] = msg
    _append_log(state, msg)
    return state


workflow = StateGraph(AgentState)

workflow.add_node("ADO Connector", ado_connector)
workflow.add_node("Synapse Orchestrator", synapse_orchestrator)
workflow.add_node("Meta‑Refiner", meta_refiner)
workflow.add_node("DB Architect", db_architect)
workflow.add_node("Backend Coder", backend_coder)
workflow.add_node("Frontend Coder", frontend_coder)
workflow.add_node("Legacy Agent", legacy_agent)
workflow.add_node("The Sentinel", sentinel_tester)
workflow.add_node("Deployment Engine", deployment_engine)

workflow.set_entry_point("ADO Connector")

workflow.add_edge("ADO Connector", "Synapse Orchestrator")
workflow.add_edge("Synapse Orchestrator", "Meta‑Refiner")
workflow.add_edge("Meta‑Refiner", "DB Architect")
workflow.add_edge("DB Architect", "Backend Coder")
workflow.add_edge("Backend Coder", "Frontend Coder")
workflow.add_edge("Frontend Coder", "Legacy Agent")
workflow.add_edge("Legacy Agent", "The Sentinel")

workflow.add_conditional_edges(
    "The Sentinel",
    test_router,
    {
        "retry": "Backend Coder",
        "success": "Deployment Engine",
        "max_retries": "Deployment Engine",
    },
)

workflow.add_edge("Deployment Engine", END)

app_graph = workflow.compile()
