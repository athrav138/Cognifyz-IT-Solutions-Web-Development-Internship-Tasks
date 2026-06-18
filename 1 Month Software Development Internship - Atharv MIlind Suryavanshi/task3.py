# Defining task with necessary attributes with CRUD
class Task:
  tasks_list = []

  @staticmethod
  def create(name):
    Task.tasks_list.append(name)

  @staticmethod
  def delete(name):
    if name in Task.tasks_list:
      Task.tasks_list.remove(name)
    else:
      print("The task is not exist.")

  @staticmethod
  def read():
    if not Task.tasks_list:
      print("No Tasks in list. Please Create!")
      return
    print("List of tasks:")
    for i in range(0,len(Task.tasks_list)):
      print(f"{i+1}. {Task.tasks_list[i]}")

  @staticmethod
  def update(old_task_id, update_task_name):
    if old_task_id >= 1 and old_task_id <= len(Task.tasks_list):
        Task.tasks_list[old_task_id - 1] = update_task_name
    else:
        print("The task does not exist.")

  @staticmethod
  def delete_all():
    Task.tasks_list.clear()


# Using the Tasks Class
while True:
  print("---Task Manager---")
  print("1. Create New Task") 
  print("2. Update Existing Task")
  print("3. Deleting Existing Task")   
  print("4. Deleting All tasks")
  print("5. Display All tasks")
  print("6. Exit")

  choice = int(input("Enter choice(1-6): "))

  if choice==1:
    task = input("Enter your Task to create: ")
    Task.create(task)
    print("Task is successfully added to list.")
  elif choice==2:
    id = int(input("Enter old task id: "))
    task = input("Enter your Updated Task: ")
    Task.update(id,task)
    print("Task is successfully updated to list.")
  elif choice==3:
    task = input("Enter your Task to delete : ")
    Task.delete(task)
    print("Task is successfully deleted from list.")
  elif choice==4:
    Task.delete_all()
    print("All Tasks is successfully deleted from list.")
  elif choice==5:
    Task.read()
  elif choice==6:
    print("Exiting....!")
    break
  else:
    print("Invalid Input.Please Enter valid Input(1,6)")

  