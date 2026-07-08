# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design focused on four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. The core actions I wanted to support were adding a pet, scheduling a task for that pet, and viewing the schedule. I designed the system around a simple workflow where an owner manages pets and organizes their care tasks.

***Classes and responsibilities***

- `Owner`: stores basic information about the pet owner, such as name and join date. The owner manages one or more pets and can create tasks for them.
- `Pet`: stores information about the pet, such as name, age, birth date, breed, and species. A pet belongs to an owner and can have multiple tasks.
- `Task`: stores details such as description, time, frequency, completed status, and pet assignment. A task is assigned to a pet.
- `Scheduler`: sorts and presents tasks, detects conflicts, and integrates with the owner or pet context.

***Relationships***

- `Owner` to `Pet`: one-to-many
- `Pet` to `Task`: one-to-many
- `Task` to `Pet`: optional back reference
- `Scheduler` to `Owner` / `Pet`: dependency relationships

***Missing cases to consider***

- Editing or deleting a pet
- Editing or deleting a task through the UI
- More advanced recurrence patterns beyond `daily` and `weekly`
- Real date handling and multi-day calendars
- Duration, priority, and owner preference constraints
- Notifications, reminders, or time window enforcement

**b. Design changes**

- During implementation, I updated `Scheduler` so it can reference an `Owner` or a specific `Pet`, not just an internal task list. That made the schedule display more accurate for the current app flow.
- I kept `Task` lightweight and used `Task.mark_complete()` to handle recurrence, because it was cleaner than moving that logic into the scheduler.
- I also chose to keep time as an `HH:MM` string and parse it for sorting, which was simpler for the current requirements.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The current scheduler primarily considers task time ordering and task recurrence.
- It also detects conflicts when multiple tasks are scheduled for the same time slot.
- Priority and owner preference are not implemented yet, because the focus was on establishing a correct baseline of sorting, conflict detection, and recurrence.

**b. Tradeoffs**

- One tradeoff is simplicity over full scheduling optimization. I used string-based time sorting instead of a complete date/time model.
- This tradeoff is reasonable for the current app scope because the UI is focused on same-day task order and conflict awareness, not complex calendar planning.
- Another tradeoff is allowing conflict detection instead of automatically resolving overlaps. That keeps the model transparent and lets the owner decide which task to move.

---

## 3. AI Collaboration

**a. How you used AI**

- I used the AI assistant for design validation, code suggestions, and refactoring guidance.
- The most effective features were help with class structure, test coverage recommendations, and identifying places where the UI should use scheduler methods directly.
- Prompts that asked for specific improvements, such as "use scheduler methods in app.py" or "add conflict warning display," were especially useful.

**b. Judgment and verification**

- I rejected one AI suggestion to give `Scheduler` full ownership of task persistence and instead kept task ownership with `Pet` and `Owner`. That preserved a clearer domain model and avoided unnecessary duplication.
- I verified AI suggestions by checking the current code structure, running the test suite, and ensuring the resulting design matched the intended relationships between owner, pet, and task.
- I also used separate chat sessions to isolate design discussion from implementation details, which made it easier to stay organized and avoid mixing design changes with UI updates.

---

## 4. Testing and Verification

**a. What you tested**

- I tested that the scheduler returns tasks in chronological order.
- I tested that marking a daily task complete creates a new task occurrence.
- I tested conflict detection when two tasks share the same time.
- I also tested basic owner and pet relationships, task editing, and status updates.

**b. Confidence**

- I am fairly confident that the implemented scheduler works correctly for the current app behavior.
- If I had more time, I would add edge case tests for invalid time formats, duplicate task objects, recurring tasks with different frequencies, and task deletion.

---

## 5. Reflection

**a. What went well**

- I am most satisfied with the way the scheduler logic was connected to the UI through `Scheduler.view_schedule()` and `Scheduler.check_conflicts()`.
- The test suite provides good coverage for the core behaviors that matter most for this stage of the app.

**b. What you would improve**

- In a future iteration, I would improve the schedule model by using real date/time values and by adding priority or duration support.
- I would also refine the UI to allow task editing and conflict resolution directly from the schedule.

**c. Key takeaway**

- The key lesson was that being the lead architect means making deliberate design choices and using AI suggestions selectively. AI can propose many good patterns, but the final system needs to stay coherent and aligned with the project goals.
