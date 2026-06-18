import os

class Task:
    FILE_NAME = "tasks.txt"

    @staticmethod
    def create(name):
        with open(Task.FILE_NAME, "a") as file:
            file.write(name + "\n")

    @staticmethod
    def read():
        try:
            with open(Task.FILE_NAME, "r") as file:
                tasks = file.readlines()

            if not tasks:
                print("No tasks in  the list.")
                return

            print("List of Tasks:")
            for i, task in enumerate(tasks, start=1):
                print(f"{i}. {task.strip()}")

        except FileNotFoundError:
            print("No  task file found. Create a task first.")

    @staticmethod
    def update(task_id, new_task):
        try:
            with open(Task.FILE_NAME, "r") as file:
                tasks = file.readlines()

            if 1 <= task_id <= len(tasks):
                tasks[task_id - 1] = new_task + "\n"

                with open(Task.FILE_NAME, "w") as file:
                    file.writelines(tasks)

                print("Task updated  successfully")

            else:
                print("Invalid task ID.")

        except FileNotFoundError:
            print("No task file found ")

    @staticmethod
    def delete(task_id):
        try:
            with open(Task.FILE_NAME, "r") as file:
                tasks = file.readlines()

            if 1 <= task_id <= len(tasks):
                removed = tasks.pop(task_id - 1)

                with open(Task.FILE_NAME, "w") as file:
                    file.writelines(tasks)

                print(f"Deleted task: {removed.strip()}")

            else:
                print("Invalid task ID ")

        except FileNotFoundError:
            print("No task file found.")

    @staticmethod
    def delete_all():
        try:
            open(Task.FILE_NAME, "w").close()
            print("All tasks deleted ")

        except Exception as e:
            print("Error:", e)


# Main Program
while True:
    print("\n--- TASK MANAGER ---")
    print("1. Create New Task")
    print("2. Update Existing Task")
    print("3. Delete Existing Task")
    print("4. Delete All Tasks")
    print("5. Display All Tasks")
    print("6. Exit")

    try:
        choice = int(input("Enter choice (1-6): "))

        if choice == 1:
            task = input("Enter task: ")
            Task.create(task)
            print("Task added successfully. ")

        elif choice == 2:
            Task.read()
            task_id = int(input("Enter task ID to update: "))
            new_task = input("Enter updated task:")
            Task.update(task_id, new_task)

        elif choice == 3:
            Task.read()
            task_id = int(input("Enter task ID to delete: "))
            Task.delete(task_id)

        elif choice == 4:
            Task.delete_all()

        elif choice == 5:
            Task.read()

        elif choice == 6:
            print("Exiting Task Manager...")
            break

        else:
            print("Please enter a number between 1 and 6.")

    except ValueError:
        print("Invalid input. Please enter a number.")