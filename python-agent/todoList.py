from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# if "count" not in st.session_state:
#     st.session_state.count = 0
if "tasks" not in st.session_state:
    st.session_state.tasks = [{
        "id": 1,
        "task": "Task 1",
        "done": False
    }]

def main():
    st.title("Todo List")
    st.write("Here are your tasks:")

    for task in st.session_state.tasks:
        if task["done"]:
            st.write(f"✅ {task['task']}")
            st.button("Toggle", key=task["id"], on_click=toggle_task, args=(task["id"]))
        else:
            st.write(f"❌ {task['task']}")
            st.button("Toggle", key=task["id"], on_click=toggle_task, args=(task["id"]))

    st.text_input("Add a task", key="input")
    st.button("Add", on_click=add_task, args=(st.session_state.input,))

def add_task(value):
    st.session_state.tasks.append({
        "id": len(st.session_state.tasks) + 1,
        "task": value,
        "done": False
    })

def toggle_task(id):
    for task in st.session_state.tasks:
        if task["id"] == id:
            task["done"] = not task["done"]

if __name__ == "__main__":
    main()