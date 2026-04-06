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

## Features

- Create owners, pets, and care tasks with duration, priority, and time.
- Build a daily schedule that fits within available time.
- Sort tasks by time and surface basic conflicts.
- Support recurring daily/weekly tasks that re-create after completion.

## Smarter Scheduling

This version includes:

- Sorting tasks by time (with priority as a tiebreaker)
- Filtering by pet or completion status
- Recurring task creation for daily/weekly tasks
- Conflict warnings when tasks share the same time

## 📸 Demo

<a href="/course_images/ai110/pawpal_demo.png" target="_blank"><img src='/course_images/ai110/pawpal_demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Testing PawPal+

Run tests with:

```bash
python -m pytest
```

Tests cover task completion, task addition, sorting by time, recurrence creation, and conflict detection.

Confidence level: ★★★★☆

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
