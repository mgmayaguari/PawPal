# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
Today's Schedule
----------------
07:00 - Feed breakfast (Mochi)
08:00 - Morning walk (Mochi)
10:00 - Vet visit (Luna)
18:00 - Play session (Luna)
```

## 🧪 Testing PawPal+

Run the test suite from the project root:

```bash
python -m pytest
```

These tests cover:

- task sorting correctness via `Scheduler.view_schedule()` and `Scheduler.sort_by_time()`
- recurring task behavior when a daily task is marked complete
- conflict detection when two tasks share the same time slot

Sample successful output:

```bash
============================= test session starts ==============================
platform darwin -- Python 3.11.5, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/michaelmayaguari/Documents/code/CodePath/PawPal
plugins: anyio-4.14.1
collected 11 items

tests/test_pawpal.py ...........                                         [100%]

============================== 11 passed in 0.01s ==============================
```

**Confidence Level:** ⭐⭐⭐⭐⭐
## 📐 Smarter Scheduling

The scheduling logic in PawPal+ now supports a few lightweight automation features:

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Sorting behavior | `Scheduler.sort_by_time()` | Orders tasks by their `time` attribute using a lambda key that parses `HH:MM` values. |
| Filtering behavior | `Owner.filter_tasks()` | Filters tasks by completion status and/or pet name. |
| Conflict detection | `Scheduler.check_conflicts()` | Returns a warning message when multiple tasks share the same time slot. |
| Recurring tasks | `Task.mark_complete()` | Creates a new pending task for the next occurrence when a task is marked complete and its frequency is `daily` or `weekly`. |

## Demo Walkthrough

### Main UI features

- Update the owner name at the top of the page.
- Add a new pet by entering a name and selecting a species.
- Schedule a task by choosing a pet, typing a task description, and entering a time.
- View the full day’s schedule in a sorted table that lists time, task, pet, and status.
- Receive a visible warning when two or more tasks are scheduled at the same time.

### Example workflow

1. Open the app and verify the owner name is correct.
2. Add a pet such as `Mochi` with species `dog`.
3. Choose `Mochi` from the pet dropdown.
4. Schedule a task like `Morning walk` at `08:00`.
5. Add another task for the same or a different pet, for example `Feed breakfast` at `07:00`.
6. Check `Today's Schedule` to confirm tasks appear in chronological order.
7. If two tasks share the same time, review the warning and update one of the times.

### Key Scheduler behaviors shown

- **Sorting by time**: the scheduler uses `Scheduler.view_schedule()` to order tasks by their `HH:MM` time value.
- **Conflict warnings**: `Scheduler.check_conflicts()` detects duplicate times and surfaces a `st.warning(...)` message in the UI.
- **Recurrence support**: `Task.mark_complete()` can create a next occurrence when a task is marked complete and its frequency is `daily` or `weekly`.
- **Pet-task linkage**: tasks added through the UI are assigned to the selected pet and preserved across the schedule.

### Sample CLI output from `main.py`

```bash
$ python main.py
08:00 - Morning walk (Mochi)
12:00 - Lunch (Mochi)
18:00 - Evening play (Luna)
```
