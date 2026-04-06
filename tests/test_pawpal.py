from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_mark_complete_updates_status():
    task = Task(title="Feed", duration_minutes=10, priority="high", time_str="08:00")
    task.mark_complete()
    assert task.completed is True


def test_pet_add_task_increases_count():
    pet = Pet(name="Mochi", species="dog")
    pet.add_task(Task(title="Walk", duration_minutes=20, priority="medium", time_str="07:30"))
    assert len(pet.tasks) == 1


def test_sorting_by_time():
    owner = Owner(name="Jordan", available_time_minutes=120)
    scheduler = Scheduler(owner)
    tasks = [
        Task(title="Late", duration_minutes=10, priority="low", time_str="09:00"),
        Task(title="Early", duration_minutes=10, priority="high", time_str="07:00"),
        Task(title="Mid", duration_minutes=10, priority="medium", time_str="08:00"),
    ]
    sorted_tasks = scheduler.sort_by_time(tasks)
    assert [task.title for task in sorted_tasks] == ["Early", "Mid", "Late"]


def test_recurrence_creates_next_task():
    today = date.today()
    task = Task(
        title="Medication",
        duration_minutes=5,
        priority="high",
        time_str="08:00",
        frequency="daily",
        due_date=today,
    )
    new_task = task.mark_complete()
    assert new_task is not None
    assert new_task.due_date == today + timedelta(days=1)
    assert new_task.completed is False


def test_conflict_detection_flags_duplicate_times():
    owner = Owner(name="Jordan", available_time_minutes=120)
    scheduler = Scheduler(owner)
    tasks = [
        Task(title="Walk", duration_minutes=20, priority="high", time_str="08:00"),
        Task(title="Feed", duration_minutes=10, priority="medium", time_str="08:00"),
    ]
    warnings = scheduler.detect_conflicts(tasks)
    assert len(warnings) == 1
