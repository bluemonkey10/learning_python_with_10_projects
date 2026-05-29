# To-Do List App: Project 2
import json

def main():
    print("=== TO-DO LIST Ultra ===\n")
    menu()

    # the_tasks = ["Study", "Exercise", "Drive to church"]
    
    try:
        with open("tasks.json", "r") as file:
            tasks = json.load(file)
    except(json.JSONDecodeError, FileNotFoundError):
        tasks = {}
    
    keepGoing = True

    while keepGoing:
    # Checking if user input is a valid number
        valid = False
        while not valid:
            try:
                userChoice = input("Enter your choice (1-5): ")
                userChoice = int(userChoice)
                
                # Checking if user input is a valid option
                if not userAction(userChoice, tasks):
                    valid = False
                else:
                    valid = True
                
                if userChoice != 4:
                    shouldContinue = input("Would you like to continue? Enter yes or no: ")
                    if shouldContinue.lower() == "yes":
                        keepGoing = True
                        menu()
                    else:
                        keepGoing = False
                

                # If its option 4, quitting immediately is essential
                else:
                    keepGoing = False
                
            except ValueError:
                print("Please enter a valid number\n")
                valid = False
            
            
            
    
def userAction(userChoice, tasks):
    if userChoice == 1:
        view(tasks)
        return True
    elif userChoice == 2:
        add(tasks)
        return True
    elif userChoice == 3:
        remove(tasks)
        return True
    elif userChoice == 4:
        quit_program(tasks)
        return True
    elif userChoice == 5:
        completeTask(tasks)
        return True
    else:
        print("Must be a number that is 1-5\n")
        return False

def view(tasks):
    print("\n=== TASKS AT HAND ===\n")
    for i, task in enumerate(tasks.values()):
        status = "X" if task["completed"] else " "
        print(f"{list(tasks.keys())[i]}.[{status}] {task['description']}")
    print("\n")

    
def add(tasks):
    task_description = input("Enter task description: ")
    new_task = {
        "description": task_description,
        "completed": False
    }

    if not tasks:
        tasks["1"] = new_task
    else:
        tasks[str(int(list(tasks.keys())[-1]) + 1)] = new_task

    print("Task added successfully\n")

    print("After update: \n")
    view(tasks)

def remove(tasks):
    view(tasks)

    try:
        task_num = int(input("Enter task number to remove: "))
    except ValueError:
        print("Please enter a valid number\n")
        return

    if str(task_num) not in tasks:
        print("Task does not exist\n")
    else:
        del tasks[str(task_num)]
        print("Task removed successfully\n")
        print("After removal: \n")
        view(tasks)
    
    
def quit_program(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)

    print("Progress saved, enjoy your day, chump\n")

def completeTask(tasks):
    view(tasks)

    try:
        task_num = int(input("Enter completed task number: "))
    except ValueError:
        print("Please enter a valid number\n")
        return
    
    if str(task_num) not in tasks:
        print("Task does not exist\n")
        return
    
    else:
        # task_key = list(tasks.keys())[task_num - 1]
        tasks[str(task_num)]["completed"] = True
        print("Good job finishing that task!\n")

        print("After update: \n")
        view(tasks)

def menu():
    print("1. View Tasks")
    print("2. Add Task")
    print("3. Remove Task")
    print("4. Save & Quit")
    print("5. Complete Task\n")


if __name__ == "__main__":
    main()
