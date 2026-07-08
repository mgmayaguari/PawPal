# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to help implement and refine the scheduler system for PawPal+, including task sorting, conflict detection, recurring task logic, and connecting the scheduler methods to the Streamlit UI.

**What did the agent do?**

The agent reviewed existing source files, suggested improvements to `app.py`, `README.md`, and the UML diagram, and helped ensure the scheduler methods were used consistently. It also proposed tests and UI updates that aligned the app with the final scheduler behavior.

**What did you have to verify or fix manually?**

I verified that the suggested code changes preserved the ownership relationships between `Owner`, `Pet`, and `Task`. I also checked the UI updates for correctness, ensured the conflict warning logic was user-friendly, and confirmed the final design through pytest.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | GitHub Copilot | GitHub Copilot |
| **Prompt** | "Use scheduler methods in app.py and show conflict warnings." | "Update README with demo walkthrough and sample output." |
| **Response summary** | Suggested UI changes to use `Scheduler.view_schedule()` and `Scheduler.check_conflicts()` | Replaced the demo section with a detailed walkthrough and sample CLI output. |
| **What was useful** | The agent consistently mapped code behavior to UI display requirements. | The agent provided a structured README section that matched the implementation. |
| **Problems noticed** | Needed manual review to keep task ownership and avoid duplicate persistence. | None significant; the generated walkthrough was aligned with the project. |
| **Decision** | Accepted the changes after verifying domain relationships. | Accepted the documentation update as-is. |

**Which approach did you use in your final implementation and why?**

I used the AI assistant as a collaborative editor for iterative implementation, focusing on incremental requests that matched distinct phases of the project. This kept the design clean and allowed me to validate each change with tests and manual review before moving on.
