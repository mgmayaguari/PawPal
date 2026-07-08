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


def test_scheduler_sort_by_time_uses_time_attribute():
    scheduler = Scheduler()
    first = Task(task_id=6, description="Lunch", time="12:00")
    second = Task(task_id=7, description="Morning walk", time="08:00")

    assert scheduler.sort_by_time([first, second]) == [second, first]


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


def test_owner_can_filter_tasks_by_completion_and_pet_name():
    owner = Owner(owner_id=1, name="Jordan")
    pet_one = Pet(pet_id=1, name="Mochi")
    pet_two = Pet(pet_id=2, name="Luna")
    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    completed_task = Task(task_id=9, description="Vet visit", time="10:00")
    pending_task = Task(task_id=10, description="Walk", time="18:00")
    completed_task.mark_complete()

    pet_one.add_task(completed_task)
    pet_two.add_task(pending_task)

    filtered_by_status = owner.filter_tasks(completed=True)
    filtered_by_pet = owner.filter_tasks(pet_name="mochi")

    assert filtered_by_status == [completed_task]
    assert filtered_by_pet == [completed_task]


def test_recurring_task_creates_next_occurrence_when_completed():
    pet = Pet(pet_id=4, name="Biscuit")
    task = Task(task_id=11, description="Morning walk", time="08:00", frequency="daily")
    pet.add_task(task)

    next_task = task.mark_complete()

    assert task.completed is True
    assert task.status == "completed"
    assert next_task is not None
    assert next_task is not task
    assert next_task.completed is False
    assert next_task.status == "pending"
    assert next_task.frequency == "daily"
    assert next_task.pet is pet
    assert next_task in pet.tasks


def test_scheduler_detects_conflicting_tasks_at_same_time():
    owner = Owner(owner_id=1, name="Jordan")
    pet_one = Pet(pet_id=1, name="Mochi")
    pet_two = Pet(pet_id=2, name="Luna")
    owner.add_pet(pet_one)
    owner.add_pet(pet_two)

    first = Task(task_id=12, description="Walk", time="08:00")
    second = Task(task_id=13, description="Feed", time="08:00")

    pet_one.add_task(first)
    pet_two.add_task(second)

    scheduler = Scheduler(owner=owner)
    conflict_message = scheduler.check_conflicts()

    assert "Warning" in conflict_message
    assert "08:00" in conflict_message
