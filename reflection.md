# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial UML design focused on four main classes: Owner, Pet, Task, and Scheduler. The core actions I wanted to support were adding a pet, scheduling a task for that pet, and viewing the schedule. I designed the system around a simple workflow where an owner manages pets and organizes their care tasks.

***Classes and responsibilities***

- Owner: stores basic information about the pet owner, such as name and join date. The owner manages one or more pets and can create tasks for them.
- Pet: stores information about the pet, such as name, age, birth date, breed, and type. A pet belongs to an owner and can have multiple tasks.
- Task: stores details such as task name, date, time, duration, recurrence, and status. A task is assigned to a pet.
- Scheduler: organizes tasks by date and time and helps display the pet’s schedule.

***Relationships***

- Owner to Pet: one-to-many
- Pet to Task: one-to-many
- Scheduler to Task: one scheduler can manage many tasks

***Missing cases to consider***

- Editing or deleting a pet
- Editing or deleting a task
- Marking a task as completed or skipped
- Handling recurring tasks
- Preventing schedule conflicts
- Viewing tasks by day, week, or month
- Sending reminders or notifications

**b. Design changes**

- Yes. During implementation, I adjusted the design of the Scheduler so it had a direct connection to an Owner or Pet instead of only managing a list of tasks.

- I added optional owner and pet references to the Scheduler class because it made the relationships clearer and helped the schedule feel more connected to a specific pet owner. This change also made it easier to think about how tasks would be grouped and viewed later, instead of treating the scheduler as a disconnected list of tasks.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
