
import streamlit as st
import time
from graph import app_graph, initial_state_from_user_story

st.set_page_config(page_title="Auto Dev-Synapse", layout="wide")

st.title("🤖 Auto Dev-Synapse Platform")
st.markdown("**Team:** Techno Squad &nbsp;&nbsp;|&nbsp;&nbsp; **ID:** Auto-250329")
st.markdown("_Automating the Full‑Stack Lifecycle via Collaborative Multi‑Agent Orchestration_")

with st.sidebar:
    st.header("Azure DevOps Input")
    default_story = "As an examiner, I want a web-based exam form so that students can submit their details and preferred exam slot. The backend should expose FastAPI endpoints and store data in a PostgreSQL table."
    user_story = st.text_area("User Story", value=default_story, height=160)
    use_sample = st.checkbox("Use sample ADO payload (mock)", value=True)
    start_btn = st.button("🚀 Start Synapse Engine")

col_main, col_graph = st.columns([2.3, 1.2])

if start_btn and user_story.strip():
    with st.spinner("Starting multi‑agent orchestration..."):
        state = initial_state_from_user_story(user_story, use_sample_payload=use_sample)
        logs_placeholder = col_main.empty()
        timeline = []

        for step in app_graph.stream(state, config={"recursion_limit": 20}):
            for node_name, node_state in step.items():
                snapshot = {
                    "node": node_name,
                    "status": node_state.get("current_status", ""),
                    "plan": node_state.get("plan", ""),
                    "refined_story": node_state.get("refined_story", ""),
                    "backend_code": node_state.get("backend_code", ""),
                    "frontend_code": node_state.get("frontend_code", ""),
                    "db_schema": node_state.get("db_schema", ""),
                    "legacy_analysis": node_state.get("legacy_analysis", ""),
                    "test_results": node_state.get("test_results", ""),
                    "deployment_status": node_state.get("deployment_status", ""),
                    "logs": node_state.get("logs", [])[-4:],
                }
                timeline.append(snapshot)

            with logs_placeholder.container():
                st.subheader("📡 Agent Activity Feed")
                for i, snap in enumerate(timeline):
                    with st.expander(f"{i+1}. {snap['node']} – {snap['status']}", expanded=(i == len(timeline) - 1)):
                        for line in snap["logs"]:
                            st.markdown(f"- {line}")
                        if snap["plan"]:
                            st.markdown("**Plan:**")
                            st.code(snap["plan"])
                        if snap["refined_story"]:
                            st.markdown("**Refined Story:**")
                            st.write(snap["refined_story"])
                        if snap["db_schema"]:
                            st.markdown("**Proposed DB Schema:**")
                            st.code(snap["db_schema"], language="sql")
                        if snap["backend_code"]:
                            st.markdown("**Backend API (FastAPI):**")
                            st.code(snap["backend_code"], language="python")
                        if snap["frontend_code"]:
                            st.markdown("**Frontend UI (React + Fetch):**")
                            st.code(snap["frontend_code"], language="javascript")
                        if snap["legacy_analysis"]:
                            st.markdown("**Legacy Integration Notes:**")
                            st.code(snap["legacy_analysis"], language="python")
                        if snap["test_results"]:
                            if "FAIL" in snap["test_results"]:
                                st.error(snap["test_results"])
                            else:
                                st.success(snap["test_results"])
                        if snap["deployment_status"]:
                            st.info(snap["deployment_status"])

            time.sleep(0.4)

        final = timeline[-1] if timeline else {}
        if final.get("deployment_status", "").startswith("✅"):
            st.balloons()

    with col_graph:
        st.subheader("🧠 Live Orchestration Graph")
        st.graphviz_chart("""
        digraph AutoDev {
            rankdir=LR;
            node [shape=box, style=rounded];

            ADO          [label="Azure DevOps\nUser Story"];
            Orchestrator [label="Synapse Orchestrator"];
            Refiner      [label="Meta‑Refiner"];
            DB           [label="DB Architect"];
            Backend      [label="Backend Coder"];
            Frontend     [label="Frontend Coder"];
            Legacy       [label="Legacy Agent"];
            Sentinel     [label="The Sentinel\n(Tester)"];
            Deploy       [label="Deployment Engine"];

            ADO -> Orchestrator -> Refiner -> DB -> Backend -> Frontend -> Legacy -> Sentinel -> Deploy;

            Sentinel -> Backend [label="Fail / Retry", color="red", style="dashed"];
        }
        """)
else:
    with col_main:
        st.info("Provide a user story and press **Start Synapse Engine** to see the agents collaborate.")
    with col_graph:
        st.subheader("🧠 Live Orchestration Graph")
        st.graphviz_chart("""
        digraph AutoDev {
            rankdir=LR;
            node [shape=box, style=rounded];
            ADO          [label="Azure DevOps\nUser Story"];
            Orchestrator [label="Synapse Orchestrator"];
            Refiner      [label="Meta‑Refiner"];
            DB           [label="DB Architect"];
            Backend      [label="Backend Coder"];
            Frontend     [label="Frontend Coder"];
            Legacy       [label="Legacy Agent"];
            Sentinel     [label="The Sentinel\n(Tester)"];
            Deploy       [label="Deployment Engine"];

            ADO -> Orchestrator -> Refiner -> DB -> Backend -> Frontend -> Legacy -> Sentinel -> Deploy;
            Sentinel -> Backend [label="Fail / Retry", color="red", style="dashed"];
        }
        """)
