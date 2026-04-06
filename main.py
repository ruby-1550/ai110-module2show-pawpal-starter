from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def format_schedule(tasks):
    lines = ["Today's Schedule:"]
    for task in tasks:
        pet_label = f" ({task.pet_name})" if task.pet_name else ""
        lines.append(f"- {task.time_str} | {task.title}{pet_label} | {task.duration_minutes} min")
    return "\n".join(lines)


def main() -> None:
    owner = Owner(name="Jordan", available_time_minutes=120)

    mochi = Pet(name="Mochi", species="dog", age=3)
    luna = Pet(name="Luna", species="cat", age=5)

    owner.add_pet(mochi)
    owner.add_pet(luna)

    mochi.add_task(Task(title="Morning walk", duration_minutes=20, priority="high", time_str="08:00"))
    mochi.add_task(Task(title="Breakfast", duration_minutes=10, priority="medium", time_str="07:30"))
    luna.add_task(Task(title="Medication", duration_minutes=5, priority="high", time_str="08:00", frequency="daily"))

    scheduler = Scheduler(owner)
    tasks, warnings = scheduler.build_daily_plan(date.today())

    print(format_schedule(tasks))
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    main()
