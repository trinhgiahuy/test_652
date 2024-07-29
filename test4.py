import math

class Task:
    def __init__(self, name, releasetime, period, executiontime, deadline):
        self.releasetime = releasetime
        self.period = period
        self.executiontime = executiontime
        self.deadline = deadline
        self.next_available = releasetime
        self.name = name
        self.completed = False          # Completed of task within each of its period
        self.addedtime = 0.0            # Already executed time in the current period
        self.preemptions = 0            # Track number of preemptions
        self.expected_continue = False

    def info(self):
        return (f"{self.name}, exectime {self.executiontime} next_avai:{self.next_available} executed:{self.completed} addedtime:{self.addedtime} expected_continue: {self.expected_continue} preemptions:{self.preemptions}")

class Timeline:
    def __init__(self, total_time):
        self.current_time = 0.0
        self.total_time = total_time
        self.tasks = []

    def add_task(self, task, duration):
        from_time = self.current_time
        end_time = from_time + duration
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
                finish_before_trans = (expected_executing_task.getAddedTime() == expected_executing_task.getExecutionTime())

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

def get_next_event_time(tasks, current_time):
    next_times = [task.next_available for task in tasks if task.next_available > current_time]
    next_times.extend([task.next_available + task.period for task in tasks if task.addedtime < task.executiontime])
    if next_times:
        return min(next_times)
    return current_time + 1  # In case there are no upcoming events

def schedule(tasks, total_time, expected_task_first_run):
    timeline = Timeline(total_time)
    current_task = None
    first_run = True

    while timeline.current_time < timeline.total_time:
        print()
        print(f"=================================[SCHEDULE] [{timeline.current_time}]")
        print(f"current_task {current_task}")
        if first_run:
            print("First run")
            task = preempted(tasks, timeline.current_time, expected_task_first_run, True)
            first_run = False
        else:
            print("Not first run, handle expected executing task")
            task = preempted(tasks, timeline.current_time, expected_task_first_run, False)

        print(f"task after preempt: {task}")

        # CASE WHEN ALL TASKS COMPLETE WITHIN THEIR PERIOD AND NOT YET AVAILABLE, IDLE TIME
        if task is None:
            next_event_time = get_next_event_time(tasks, timeline.current_time)
            timeline.tasks.append(["  ", timeline.current_time, next_event_time])
            print(f"{timeline.current_time} - Timeline.tasks after add task {timeline.tasks}")
            timeline.current_time = next_event_time
            continue

        remaining_time = task.executiontime - task.addedtime
        next_event_time = get_next_event_time(tasks, timeline.current_time)
        duration = min(remaining_time, next_event_time - timeline.current_time)
        
        timeline.add_task(task, duration)
        task.addedtime += duration  # keep adding till it equals task.executiontime

        if task.addedtime < task.executiontime:
            task.expected_continue = True
        else:  # task completed
            task.addedtime = 0.0
            task.completed = True
            task.expected_continue = False
            task.next_available += task.period

        if task is not None:
            current_task = task
            expected_task_first_run = task
        print(f"[UPDATE TASK]: {task.info()}")
        print(f"[UPDATE TIMELINE]: {timeline.info()}")

    return timeline, tasks

def format_gantt_chart(timeline):
    total_time_slots = int(math.ceil(timeline.total_time * 1000))
    formatted_chart = ["  "] * total_time_slots
    for task in timeline.tasks:
        name, start, end = task
        for t in range(int(start * 1000), int(end * 1000)):
            formatted_chart[t] = name
    return formatted_chart

def print_gantt_chart(formatted_chart):
    time_header = "Time | " + " | ".join(f"{t / 1000:.3f}" for t in range(len(formatted_chart)))
    task_header = "Task | " + " | ".join(f"{task:2}" for task in formatted_chart)
    print(time_header)
    print(task_header)

def print_preemptions(tasks):
    preemptions = [task.preemptions for task in tasks]
    print("Preemptions:", ",".join(map(str, preemptions)))

# Main Function
if __name__ == "__main__":
    # Workload 4 from the exam question
    tasks = [
        Task("T0", 0, 4, 2, 6),
        Task("T1", 0, 8, 1.5, 10),
        Task("T2", 0, 8, 1.5, 9),
        Task("T3", 0, 8, 1, 15)
    ]

    # Define the total time for the Gantt chart (hyperperiod in this case)
    total_time = 8  # This is just an example value; adjust as needed

    # Expected task to run first
    expected_task_first_run = get_first_task_run(tasks)

    timeline, tasks = schedule(tasks, total_time, expected_task_first_run)
    formatted_chart = format_gantt_chart(timeline)
    print_gantt_chart(formatted_chart)
    print_preemptions(tasks)
