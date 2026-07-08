from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(owner_id=1, name="Jordan")

    pet1 = Pet(pet_id=1, name="Mochi", species="dog")
    pet2 = Pet(pet_id=2, name="Luna", species="cat")

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(task_id=1, description="Morning walk", time="08:00")
    task2 = Task(task_id=2, description="Feed breakfast", time="07:00")
    task3 = Task(task_id=3, description="Vet visit", time="10:00")
    task4 = Task(task_id=4, description="Play session", time="18:00")

    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)
    pet2.add_task(task4)

    scheduler = Scheduler(owner=owner)
    for task in owner.get_all_tasks():
        scheduler.add_task(task)

    print("Today's Schedule")
    print("----------------")
    for task in scheduler.view_schedule():
        pet_name = task.pet.name if task.pet else "Unassigned"
        print(f"{task.time} - {task.description} ({pet_name})")


if __name__ == "__main__":
    main()
