class Task:
    def __init__(self, name, releasetime, period, executiontime, deadline):
        self.releasetime = releasetime
        self.period = period
        self.executiontime = executiontime
        self.deadline = deadline
        self.next_available = releasetime
        self.name = name
        self.executed = False
        self.addedtime = 0  # Already executed time in the current period
        self.preemptions = 0  # Track number of preemptions

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

def available_tasks(tasks, current_time):
    return [task for task in tasks if current_time >= task.next_available]

def order_by_deadline(tasks):
    tasks.sort(key=lambda x: x.deadline)
    return tasks

def preempted(tasks, current_time, last_task):
    available = available_tasks(tasks, current_time)
    if available:
        ordered_by_priority = order_by_deadline(available)
        highest_priority_task = ordered_by_priority[0]
        if last_task and highest_priority_task.name != last_task.name:
            last_task.preemptions += 1
        return highest_priority_task
    else:
        return None

def schedule(tasks, total_time):
    timeline = Timeline(total_time)
    last_task = None
    while timeline.current_time < timeline.total_time:
        task = preempted(tasks, timeline.current_time, last_task)
        if task is None:
            timeline.tasks.append(["  ", timeline.current_time, timeline.current_time + 1])
            timeline.current_time += 1
            continue

        if task.addedtime < task.executiontime:
            timeline.add_task(task)
            task.addedtime += 1  # keep adding till it equals task.executiontime
        elif task.addedtime == task.executiontime:  # task completed
            task.addedtime = 0
            task.executed = True
            task.next_available += task.period

        last_task = task

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
    
    # Define the total time for the Gantt chart (hyperperiod in this case)
    total_time = 12  # This is just an example value; adjust as needed

    timeline, tasks = schedule(tasks, total_time)
    formatted_chart = format_gantt_chart(timeline)
    print_gantt_chart(formatted_chart)
    print_preemptions(tasks)
