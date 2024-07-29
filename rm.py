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

class Timeline:
    def __init__(self, total_time):
        self.current_time = 0
        self.total_time = total_time
        self.schedule = ["Idle"] * total_time

    def add_task(self, task):
        self.schedule[self.current_time] = task.name
        self.current_time += 1

def available_tasks(tasks, current_time):
    return [task for task in tasks if current_time >= task.next_available]

def order_by_deadline(tasks):
    tasks.sort(key=lambda x: x.deadline)
    return tasks

def preempted(tasks, current_time):
    available = available_tasks(tasks, current_time)
    if available:
        ordered_by_priority = order_by_deadline(available)
        return ordered_by_priority[0]
    else:
        return None

def schedule(tasks, total_time):
    timeline = Timeline(total_time)
    while timeline.current_time < timeline.total_time:
        task = preempted(tasks, timeline.current_time)
        if task is None:
            timeline.current_time += 1
            continue

        if task.addedtime < task.executiontime:
            timeline.add_task(task)
            task.addedtime += 1  # keep adding till it equals task.executiontime
        elif task.addedtime == task.executiontime:  # task completed
            task.addedtime = 0
            task.executed = True
            task.next_available += task.period

    return timeline

def print_gantt_chart(timeline):
    print("Gantt Chart:")
    print(" | ".join(timeline.schedule))

# Main Function
if __name__ == "__main__":
    # Example workload from the exam question
    tasks = [
        Task("T0", 0, 3, 1, 3),
        Task("T1", 0, 4, 2, 5)
    ]
    
    # Define the total time for the Gantt chart (hyperperiod in this case)
    total_time = 12  # This is just an example value; adjust as needed

    timeline = schedule(tasks, total_time)
    print_gantt_chart(timeline)
