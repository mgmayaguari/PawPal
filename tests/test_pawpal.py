from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pawpal_system import Owner, Pet, Scheduler, Task


def test_task_can_be_edited_and_marked_complete():
    task = Task(task_id=1, description="Morning walk", time="08:00")

    task.edit_task(description="Evening walk", time="19:00")
    task.mark_complete()

    assert task.description == "Evening walk"
    assert task.time == "19:00"
    assert task.completed is True
    assert task.status == "completed"


def test_pet_tracks_added_tasks():
    pet = Pet(pet_id=1, name="Mochi")
    task = Task(task_id=2, description="Feed breakfast", time="07:00")

    pet.add_task(task)

    assert task.pet is pet
    assert pet.tasks == [task]


def test_owner_manages_pets_and_collects_all_tasks():
    owner = Owner(owner_id=1, name="Jordan")
    pet = Pet(pet_id=1, name="Mochi")
    task = Task(task_id=3, description="Vet visit", time="10:00")

    owner.add_pet(pet)
    pet.add_task(task)

    assert pet.owner is owner
    assert owner.pets == [pet]
    assert owner.get_all_tasks() == [task]


def test_scheduler_orders_tasks_by_time():
    owner = Owner(owner_id=1, name="Jordan")
    pet = Pet(pet_id=1, name="Mochi")
    owner.add_pet(pet)

    first = Task(task_id=4, description="Lunch", time="12:00")
    second = Task(task_id=5, description="Morning walk", time="08:00")

    scheduler = Scheduler(owner=owner, pet=pet)
    scheduler.add_task(first)
    scheduler.add_task(second)

    assert scheduler.view_schedule() == [second, first]


def test_scheduler_preserves_existing_pet_assignment():
    owner = Owner(owner_id=1, name="Jordan")
    pet1 = Pet(pet_id=1, name="Mochi")
    pet2 = Pet(pet_id=2, name="Luna")
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task = Task(task_id=6, description="Vet visit", time="10:00")
    pet2.add_task(task)

    scheduler = Scheduler(owner=owner)
    scheduler.add_task(task)

    assert task.pet is pet2
    assert pet2.tasks == [task]


def test_task_completion_updates_status():
    task = Task(task_id=7, description="Brush teeth", time="09:00")

    task.mark_complete()

    assert task.completed is True
    assert task.status == "completed"


def test_adding_task_increases_pet_task_count():
    pet = Pet(pet_id=3, name="Biscuit")
    task = Task(task_id=8, description="Dinner", time="18:30")

    pet.add_task(task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is task
