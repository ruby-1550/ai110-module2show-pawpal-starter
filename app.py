from datetime import date, datetime

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value="Jordan")
available_time = st.number_input(
    "Available time (minutes)", min_value=15, max_value=480, value=120, step=15
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time_minutes=available_time)
else:
    st.session_state.owner.name = owner_name
    st.session_state.owner.available_time_minutes = available_time

owner = st.session_state.owner

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age (years)", min_value=0, max_value=30, value=3, step=1)
    submitted = st.form_submit_button("Add pet")
    if submitted and pet_name:
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added {pet_name}!")

if owner.pets:
    st.write("Current pets:")
    st.table([{"name": pet.name, "species": pet.species, "age": pet.age} for pet in owner.pets])
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Add a Task")
if owner.pets:
    with st.form("add_task_form"):
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        time_value = st.time_input("Time", value=datetime.strptime("08:00", "%H:%M").time())
        frequency = st.selectbox("Frequency", ["none", "daily", "weekly"], index=0)
        pet_for_task = st.selectbox("Assign to pet", [pet.name for pet in owner.pets])
        submitted_task = st.form_submit_button("Add task")
        if submitted_task:
            time_str = time_value.strftime("%H:%M") if time_value else "08:00"
            task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority,
                time_str=time_str,
                frequency=None if frequency == "none" else frequency,
            )
            for pet in owner.pets:
                if pet.name == pet_for_task:
                    pet.add_task(task)
                    break
            st.success(f"Added {task_title} for {pet_for_task} at {time_str}.")
else:
    st.info("Add a pet before creating tasks.")

all_tasks = owner.get_all_tasks()
if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "title": task.title,
                "pet": task.pet_name,
                "time": task.time_str,
                "duration": task.duration_minutes,
                "priority": task.priority,
                "frequency": task.frequency or "none",
                "completed": task.completed,
            }
            for task in all_tasks
        ]
    )

st.divider()

st.subheader("Build Schedule")
if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    tasks, warnings = scheduler.build_daily_plan(date.today())
    explanations = scheduler.explain_plan(tasks)

    if tasks:
        st.success("Schedule generated!")
        st.table(
            [
                {
                    "time": task.time_str,
                    "task": task.title,
                    "pet": task.pet_name,
                    "duration": task.duration_minutes,
                    "priority": task.priority,
                }
                for task in tasks
            ]
        )
        st.markdown("**Why these tasks?**")
        for explanation in explanations:
            st.write(f"- {explanation}")
    else:
        st.warning("No tasks fit within the available time.")

    if warnings:
        st.markdown("**Warnings**")
        for warning in warnings:
            st.warning(warning)
