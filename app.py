import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(owner_id=1, name="Jordan")

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+. This version connects the Streamlit UI to your backend classes so you can
manage pets and tasks directly in the app.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** helps a pet owner plan care tasks for their pet(s) using simple scheduling logic.
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
if st.button("Save owner"):
    owner.name = owner_name
    st.success(f"Owner updated to {owner.name}")

st.divider()

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="Mochi", key="pet_name")
species = st.selectbox("Species", ["dog", "cat", "other"], key="pet_species")

if st.button("Add pet"):
    pet = Pet(pet_id=len(owner.pets) + 1, name=pet_name, species=species)
    owner.add_pet(pet)
    st.success(f"Added {pet.name} to your account")

st.subheader("Current Pets")
if owner.pets:
    for pet in owner.pets:
        st.write(f"- {pet.name} ({pet.species})")
else:
    st.info("No pets yet. Add one above.")

st.divider()

st.subheader("Schedule a Task")
if owner.pets:
    pet_names = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Select pet", pet_names, key="selected_pet")
    selected_pet = next(pet for pet in owner.pets if pet.name == selected_pet_name)
else:
    st.info("Add a pet before scheduling a task.")
    selected_pet = None

col1, col2 = st.columns(2)
with col1:
    task_description = st.text_input("Task description", value="Morning walk", key="task_description")
with col2:
    task_time = st.text_input("Time", value="08:00", key="task_time")

if st.button("Add task"):
    if selected_pet is None:
        st.warning("Please add a pet first.")
    else:
        task = Task(task_id=len(owner.get_all_tasks()) + 1, description=task_description, time=task_time)
        selected_pet.add_task(task)
        st.success(f"Added {task_description} for {selected_pet.name}")

st.divider()

st.subheader("Today's Schedule")
if owner.get_all_tasks():
    scheduler = Scheduler(owner=owner)
    for task in owner.get_all_tasks():
        scheduler.add_task(task)

    conflict_message = scheduler.check_conflicts()
    if conflict_message != "No conflicts detected.":
        st.warning(
            f"{conflict_message} Please update one of the task times so your pets are not double-booked."
        )

    schedule_rows = [
        {
            "Time": task.time,
            "Task": task.description,
            "Pet": task.pet.name if task.pet else "Unassigned",
            "Status": task.status,
        }
        for task in scheduler.view_schedule()
    ]

    st.table(schedule_rows)
else:
    st.info("No tasks yet. Add one above.")
