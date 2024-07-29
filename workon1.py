class Task:
    def __init__(self, name, releasetime, period, executiontime, deadline):
        self.releasetime = releasetime
        self.period = period
        self.executiontime = executiontime
        self.deadline = deadline
        self.next_available = releasetime
        self.name = name
        self.completed = False          # Completed of task within each of its period
        self.addedtime = 0              # Already executed time in the current period
        self.preemptions = 0            # Track number of preemptions
        self.expected_continue = False

    def info(self):
        return (f"{self.name}, exectime {self.executiontime} next_avai:{self.next_available} executed:{self.completed} addedtime:{self.addedtime} expected_continue: {self.expected_continue} preemptions:{self.preemptions}")

    def getName(self):
        return f"{self.name}"

    def getExpectedContinue(self):
        return self.expected_continue

    def getAddedTime(self):
        return self.addedtime

    def getExecutionTime(self):
        return self.executiontime

class Timeline:
    def __init__(self, total_time):
        self.current_time = 0
        self.total_time = total_time
        self.tasks = []

    def add_task(self, task):
        from_time = self.current_time
        end_time = from_time + 1
        self.tasks.append([task.name, from_time, end_time])
        self.current_time = end_time

    def info(self):
        return (f"TIMELINE: current time: {self.current_time}     tasks: {self.tasks}")

def available_tasks(tasks, current_time):
    print("Call available:::::::::::::::::")
    for task in tasks:
        print(f"{current_time}: {task.info()}")
    print("::::::::::::::::::::")

    # This will update the available task list, with whenever task available, will update and return here
    return [task for task in tasks if current_time >= task.next_available]

def order_by_deadline(tasks):
    tasks.sort(key=lambda x: x.deadline)
    return tasks

def preempted(tasks, current_time, expected_executing_task, first_run):
    available = available_tasks(tasks, current_time)
    if available:
        print(f"Call preempted: available")
        ordered_by_priority = order_by_deadline(available)
        print(f"ordered_by_priority: {ordered_by_priority}")


        # HANDLE PRE_EMPT HERE? USUALLY NOT FIRST RUN
        if not first_run:
            print(f"[EVALUATE]: expected_executing_task {expected_executing_task.getName()} with expected_run: {expected_executing_task.getExpectedContinue()}")
            if expected_executing_task.getExpectedContinue() == True:
                print()
                print(expected_executing_task.getAddedTime())
                print(expected_executing_task.getExecutionTime())
                finish_before_trans = (expected_executing_task.getAddedTime() == expected_executing_task.getExecutionTime())
                print(finish_before_trans)

                if not finish_before_trans and (ordered_by_priority[0].getName() != expected_executing_task.getName()):
                    print("**************************PREEMPT HAPPENS!!")
                    print(f"expected_executing_task.getName() got preempted")
                    expected_executing_task.preemptions += 1
                elif finish_before_trans:
                    print("**************************** ALREADY ADDED TO TIMELINE. RESET AND PREPARE TO TRANS NEXT ITER")
                else:
                    print("**************************RUN NORMAL")
            else:
                print(f"******************TRANS TO OTHER TASK")

        return ordered_by_priority[0]
    else:
        return None

def get_first_task_run(tasks):
    tmp_list = order_by_deadline(tasks)
    print(f"FISRT RUN: {tmp_list[0].getName()}")
    return tmp_list[0]


def schedule(tasks, total_time, expected_task_first_run):
    timeline = Timeline(total_time)
    last_task = None
    current_task = None
    print(timeline.current_time)
    print(timeline.total_time)
    first_run = True

    while timeline.current_time < timeline.total_time:
        print()
        print(f"=================================[SCHEDULE] [{timeline.current_time}]")
        print(f"current_task {current_task}, last_task {last_task}")
        if first_run:
            print("First run")
            task = preempted(tasks, timeline.current_time, expected_task_first_run, True)
            # expected_executing_task = task
            first_run = False
        else:
            print("Not first run, handle expected executing task")
            task = preempted(tasks, timeline.current_time, expected_task_first_run, False)

        print(f"task after preempt: {task}")

        # CASE WHEN ALL TASKS COMPLETE WITHIN THEIR PERIOD AND NOT YET AVAILABLE, IDLE TIME
        if task is None:
            timeline.tasks.append(["  ", timeline.current_time, timeline.current_time + 1])
            print(f"{timeline.current_time} - Timeline.tasks after add task {timeline.tasks}")
            timeline.current_time += 1
            continue

        # if current_task and task.name != current_task.name:
        #    current_task.preemptions += 1

        if task.addedtime < task.executiontime:
            print(f"{task.addedtime} < {task.executiontime}.. Add to timeline")
            timeline.add_task(task)
            task.completed = False

            if task.addedtime + 1 <= task.executiontime:
                print("______________still able to continue")
                task.expected_continue = True

            task.addedtime += 1  # keep adding till it equals task.executiontime
        elif task.addedtime == task.executiontime:  # task completed
            print(f"{task.addedtime} == {task.executiontime}..Reset added time, start executing and increase next_available")
            task.addedtime = 0
            task.completed = True
            task.expected_continue = False
            task.next_available += task.period

        # Last task before transition
        # last_task = task
        if task is not None:
            current_task = task
            expected_task_first_run = task
        print(f"[UPDATE TASK]: {task.info()}")
        print(f"[UPDATE TIMELINE]: {timeline.info()}")

    return timeline, tasks

def format_gantt_chart(timeline):
    formatted_chart = ["  "] * timeline.total_time
    for task in timeline.tasks:
        name, start, end = task
        for t in range(start, end):
            formatted_chart[t] = name
    return formatted_chart

def print_gantt_chart(formatted_chart):
    time_header = "Time | " + " | ".join(f"{t:2}" for t in range(len(formatted_chart)))
    task_header = "Task | " + " | ".join(f"{task:2}" for task in formatted_chart)
    print(time_header)
    print(task_header)

def print_preemptions(tasks):
    preemptions = [task.preemptions for task in tasks]
    print("Preemptions:", ",".join(map(str, preemptions)))

# Main Function
if __name__ == "__main__":
    # Example workload from the exam question
    tasks = [
        Task("T0", 0, 3, 1, 3),
        Task("T1", 0, 4, 2, 5)
    ]
    #tasks = [
    #    Task("T0", 0, 4, 2, 6),
    #    Task("T1", 0, 8, 1.5, 10),
    #    Task("T2", 0, 8, 1.5, 9),
    #    Task("T3", 0,8, 1, 15)
    #]


    # Define the total time for the Gantt chart (hyperperiod in this case)
    total_time = 12  # This is just an example value; adjust as needed


    # expeced task to run first
    init_time = 0
    expected_task_first_run = get_first_task_run(tasks)

    timeline, tasks = schedule(tasks, total_time, expected_task_first_run)
    formatted_chart = format_gantt_chart(timeline)
    print_gantt_chart(formatted_chart)
    print_preemptions(tasks)
