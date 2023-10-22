---
layout: post
title: General notes on Multiprocessing in Python
permalink: code_musings/multiprocessing_using_queues
---
Say you have *m* tasks, and *n* workers. How would you write a class such that the *m* tasks get processed  **sequentially** in the order they were added to some iterable? 

An example of such a setup could be that you have 
1. A list of paths to images, and 
2. You want to do some kind of processing on them, and
3. You have a method that processes each image file path. 

You could do something like this to start off with: 

```python
class Worker:


    def work(self, worker_id: int, queue: Queue):
        print(f"Entered work! worker_id: {worker_id}")
        while (task := queue.get()):
            print(f"worker_id: {worker_id}, task: {task}")
            time.sleep(2)
        

    def run(self, tasks: list[dict], num_workers: int, **kwargs):
        queue_in = Queue()
        print(f"num tasks: {len(tasks)}")
        processes = []
        for worker_id in range(num_workers):
            proc = Process(
                target=self.work, kwargs={"worker_id": worker_id, "queue": queue_in}
            )
            proc.start()
            processes.append(proc)
            
        for task in tasks:
            queue_in.put(task)

            
        for proc in processes:
            proc.join()


def run_worker():
    worker = Worker()
    tasks = [f"path_{idx}" for idx in range(10)]
    worker.run(tasks=tasks, num_workers=3)

```

But then you'll get stuck on something like this: 

```bash
num tasks: 10
Entered work! worker_id: 0
worker_id: 0, task: path_0
Entered work! worker_id: 2
Entered work! worker_id: 1
worker_id: 2, task: path_1
worker_id: 1, task: path_2
worker_id: 1, task: path_3
worker_id: 2, task: path_4
worker_id: 0, task: path_5
worker_id: 1, task: path_6
worker_id: 2, task: path_7
worker_id: 0, task: path_8
worker_id: 1, task: path_9
<GETS STUCK>

```

Why? Because `queue.get()` and `queue.put()` are blocking operations! If you try and `get` from an empty queue, or `put` to a full queue, you'll be stuck forever. 
i.e. 
```python
queue = Queue()
print("trying to get something from empty queue")
res = queue.get()
print(f"Got {res} from empty queue")

```
in output, you'll only ever get:
```bash
trying to get something from empty queue
<GET STUCK!>
```
and then get stuck.

So in the `Worker` class, we must always make sure the queue has something for the `work` method to `get`. To make sure this happens, you can add a `DONE` tag to the `Worker`. In its `run` method, you can then add this `DONE` flag to the in-queue to signal to the `work` method that there is nothing more to be done.

```python
class Worker:
    DONE = "DONE"

    def work(self, worker_id: int, queue: Queue):
        print(f"Entered work! worker_id: {worker_id}")
        while (task := queue.get()) != self.DONE:
            print(f"worker_id: {worker_id}, task: {task}")
            time.sleep(2)
        else:
            print(f"task: {task}, or encountered DONE tag")
        print(f"Exiting work! worker_id: {worker_id}")

    def run(self, tasks: list[dict], num_workers: int, **kwargs):
        queue_in = Queue()
        print(f"num tasks: {len(tasks)}")
        processes = []
        for worker_id in range(num_workers):
            proc = Process(
                target=self.work, kwargs={"worker_id": worker_id, "queue": queue_in}
            )
            proc.start()
            processes.append(proc)

        for task in tasks:
            queue_in.put(task)

        for worker_id in tasks:
            queue_in.put(self.DONE)

        # block until all processes are completed
        for proc in processes:
            proc.join()

```

Then the output of
```python
def run_worker():
    worker = Worker()
    num_paths = 10
    tasks = [f"path_{idx}" for idx in range(num_paths)]
    worker.run(tasks=tasks, num_workers=3)
```
would be 

```bash
num tasks: 10
Entered work! worker_id: 0
worker_id: 0, task: path_0
Entered work! worker_id: 1
worker_id: 1, task: path_1
Entered work! worker_id: 2
worker_id: 2, task: path_2
worker_id: 0, task: path_3
worker_id: 1, task: path_4
worker_id: 2, task: path_5
worker_id: 0, task: path_6
worker_id: 1, task: path_7
worker_id: 2, task: path_8
worker_id: 1, task: path_9
task: DONE, or encountered DONE tag
Exiting work! worker_id: 0
task: DONE, or encountered DONE tag
Exiting work! worker_id: 2
task: DONE, or encountered DONE tag
Exiting work! worker_id: 1
```

Ok, so now we have a `Worker` class that works on *m* tasks sequentially with *n* workers.
But what we don't have is a way of manipulating the results of `run` yet, since the `work` method doesn't return anything. Let's change that by introducing a `queue_out`.

We can put in the results in this `queue_out`, and retrieve it after all the child processes are done.

```python
class Worker:
    DONE = "DONE"

    def work(self, worker_id: int, queue_in: Queue, queue_out: Queue):
        print(f"Entered work! worker_id: {worker_id}")
        while (task := queue_in.get()) != self.DONE:
            res = f"worker_id: {worker_id}, task: {task}"
            time.sleep(2)
            queue_out.put(res)
        else:
            print(f"task: {task}, or encountered DONE tag")
            queue_out.put(self.DONE)
        print(f"Exiting work! worker_id: {worker_id}")

    def run(self, tasks: list[dict], num_workers: int, **kwargs) -> Iterable:
        queue_in = Queue()
        queue_out = Queue()
        print(f"num tasks: {len(tasks)}")
        processes = []
        out = []
        for worker_id in range(num_workers):
            proc = Process(
                target=self.work,
                kwargs={
                    "worker_id": worker_id,
                    "queue_in": queue_in,
                    "queue_out": queue_out,
                },
            )
            proc.start()
            processes.append(proc)

        for task in tasks:
            queue_in.put(task)

        for worker_id in tasks:
            queue_in.put(self.DONE)

        for proc in processes:
            proc.join()
            
        while (res := queue_out.get()) != self.DONE:
            out.append(res)
        return out
```

and then the usage would be something like this: 

```python
def run_worker():
    worker = Worker()
    num_paths = 10
    tasks = [f"path_{idx}" for idx in range(num_paths)]
    out = worker.run(tasks=tasks, num_workers=3)
    for elem in out:
        print(elem)

```
and the output will be 

```bash
num tasks: 10
Entered work! worker_id: 1
Entered work! worker_id: 2
Entered work! worker_id: 0
task: DONE, or encountered DONE tag
Exiting work! worker_id: 1
task: DONE, or encountered DONE tag
Exiting work! worker_id: 0
task: DONE, or encountered DONE tag
Exiting work! worker_id: 2
worker_id: 1, task: path_0
worker_id: 2, task: path_1
worker_id: 0, task: path_2
worker_id: 1, task: path_4
worker_id: 2, task: path_3
worker_id: 0, task: path_5
worker_id: 2, task: path_6
worker_id: 1, task: path_7
worker_id: 0, task: path_8
```

You can see that the tasks were completed in the order they were in inside the input `tasks` list.
