import asyncio
from threading import Thread, Lock, Event
import queue

from ...Application.TaskManager.job_task import JobTask

class TaskQueueItem():
    
    def __init__(self):
        self.__main_queue:queue.Queue = queue.Queue()
        self.__setEvent:Event = Event()
        self.__is_stop:bool = False

        self.__lock:Lock = Lock()
        self.__main_thread:Thread = None
        
    def IsStarted(self):
        return True if not self.__main_thread is None else False
    
    def stop(self):
        self.__is_stop = True
        self.__setEvent.set()

    def start(self):
        try:
            if self.__main_thread is None:
                self.__main_thread = Thread(target=self.__execute, daemon=True)
                self.__main_thread.start()

        except Exception as ex:
            print(ex)
    
    def add(self, task: JobTask)->JobTask | None:
        self.__lock.acquire()
        try:
            self.__main_queue.put(task)
            
            if not self.__setEvent.is_set():
                self.__setEvent.set()

            return task
        except Exception as ex:
            print(ex)
            return None
        finally:
            if self.__lock.locked():
                self.__lock.release()

    def __execute(self):
        while self.__setEvent.wait():
            if self.__is_stop:
                break
            while not self.__main_queue.empty():
                try:
                    task:JobTask = self.__main_queue.get()
                    result = asyncio.run(task.aexecute())

                    if task.is_callback():
                        task.callback_result(result)
                    else:
                        task.set_result(result)

                    self.__main_queue.task_done()
                except Exception as ex:
                    print(ex)
            
            self.__setEvent.clear()

        self.__main_thread = None