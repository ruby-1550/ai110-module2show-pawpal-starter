# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Three core actions the user should be able to perform: add a pet profile with basic details, add or edit care tasks (like walks, feeding, or meds) with duration and priority, and generate a daily schedule to see today’s planned tasks in order with brief reasoning.
- Building blocks (objects with attributes and methods):
- Owner: attributes = name, available_time_minutes, preferences; methods = add_pet(pet), add_task(task), set_preferences(preferences).
- Pet: attributes = name, species, age, notes; methods = add_task(task), list_tasks().
- Task: attributes = title, duration_minutes, priority, frequency, notes; methods = update_details(...), estimate_time(), describe().
- Schedule: attributes = date, total_available_minutes, selected_tasks, rationale; methods = build(tasks, constraints), prioritize(tasks), explain_plan().
- Briefly describe your initial UML design.
- I chose four core classes: `Owner` manages the user’s preferences, available time, and their collection of pets and tasks; `Pet` represents a specific animal and tracks its task list; `Task` encapsulates a care activity with duration, priority, and optional frequency/notes; `Schedule` takes tasks plus constraints and produces an ordered plan with a rationale. These classes separate data (who/what) from behavior (how tasks are prioritized and scheduled).

**b. Design changes**

- Yes. After reviewing the skeleton, I added a dedicated `Scheduler` class (instead of a passive Schedule-only object) to centralize sorting, filtering, conflict detection, and daily plan building. I also expanded `Task` to include `time_str`, `completed`, and `due_date` so the scheduler could sort by time and handle recurring tasks. These changes made the scheduling logic clearer and kept behavior out of the UI layer.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- The scheduler considers available time, task time of day, and priority as the main constraints. Available time limits the total duration, and priority acts as a tiebreaker when tasks share the same time. I chose these because they map directly to the app goals and keep the logic simple enough for a first implementation.

**b. Tradeoffs**

- The scheduler only flags exact time conflicts (same HH:MM) instead of overlapping durations. That’s a reasonable tradeoff for this scenario because the app is meant to be lightweight and easy to understand, and exact matches are the easiest conflicts for a user to fix quickly.

---

## 3. AI Collaboration

**a. How you used AI**

- I used AI to brainstorm the class structure, generate a UML diagram draft, and get feedback on whether my skeleton needed more relationships or task fields. Prompts that asked for missing relationships or edge cases were the most helpful because they highlighted gaps like time-of-day and recurrence.

**b. Judgment and verification**

- One suggestion was to add complex overlap detection for task durations. I chose a simpler conflict strategy (exact time matches only) after considering the scope and testing needs. I verified the simpler approach by writing a conflict-detection test and confirming it passed.

---

## 4. Testing and Verification

**a. What you tested**

- I tested task completion state changes, adding tasks to pets, sorting by time, recurrence creation for daily tasks, and conflict detection. These tests are important because they cover the core scheduling behaviors the UI depends on.

**b. Confidence**

- I’m fairly confident (about 4/5) because the core logic is covered by tests and a CLI demo. Next, I would test pets with no tasks, tasks with invalid time strings, and overlapping durations instead of exact matches.

---

## 5. Reflection

**a. What went well**

- I’m most satisfied with the clean separation between the logic layer and the Streamlit UI, which made the system easier to reason about and test.

**b. What you would improve**

- I would improve the scheduler to handle overlapping durations and introduce per-pet time windows or preferences.

**c. Key takeaway**

- The key takeaway is that AI is most useful when I ask it to critique my design rather than write everything; the human still has to make scope and simplicity tradeoffs.
