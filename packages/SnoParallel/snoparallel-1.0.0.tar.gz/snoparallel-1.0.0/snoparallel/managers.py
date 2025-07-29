"""
This module contains the manager class and worker function to control parallelized work cycles.
"""

import sys
from multiprocessing import Process
from multiprocessing.managers import SharedMemoryManager, SyncManager
from multiprocessing.shared_memory import SharedMemory
from os import devnull
from queue import Empty, Queue
from threading import Event, Lock
from traceback import format_exc
from typing import Any, Callable, Optional

from snoparallel.variables import Variable, VariableType, get_variable_size

_WorkType = tuple[Callable[..., Any], dict[str, Any]]


def _worker(queue: Queue[_WorkType], event: Event) -> None:
    """
    This function is called by each worker process defined in the Manager class. It performs work added to the given
    queue. When working, the flag of the given event is set to false. When finished, the event flag is set to true.

    Args:
        queue: SyncManager.Queue instance to get work from.
        event: SyncManager.Event instance which is coupled to the worker.
    """
    event.clear()
    sys.stderr = open(file=devnull, encoding="utf-8", mode="w")

    while True:
        try:
            function, kwargs = queue.get(block=False)

            try:
                function(**kwargs)
            except Exception as error:
                print(f"TARGET: {function.__name__} - ARGS: {kwargs} - ERROR: \n{format_exc()}")
                raise error

            if event.is_set():
                event.clear()

        except Empty:
            if not event.is_set():
                event.set()


class Manager:
    """
    Class to control parallelized work cycles.
    """

    def __init__(self, workers: int) -> None:
        """
        Starts the queue and worker processes.

        Args:
            workers: Number of workers to start.
        """
        self._manager_sync = SyncManager()
        self._manager_sync.start()
        self._manager_sync.Lock()

        self._manager_mem = SharedMemoryManager()
        self._manager_mem.start()

        self._queue = self._manager_sync.Queue()
        self._locks: list[Lock] = []
        self._variables: list[Variable] = []
        self._memory: list[SharedMemory] = []
        self._events = [self._manager_sync.Event() for _ in range(workers)]
        self._workers = [Process(target=_worker, args=(self._queue, self._events[i])) for i in range(workers)]

        for worker in self._workers:
            worker.start()

        for event in self._events:
            event.wait(timeout=2)

    def __del__(self) -> None:
        """
        Terminates the queue and worker processes.
        """
        for worker in self._workers:
            worker.terminate()

        self._manager_sync.shutdown()
        self._manager_mem.shutdown()

    @property
    def variables(self) -> list[Variable]:
        """
        List with the requested Variable instances.
        """
        return self._variables

    def add_work(self, target: Callable[..., Any], **kwargs: Any) -> None:
        """
        Add work items to the queue for the workers to process.

        Args:
            target: Function to call.
            kwargs: Keyword arguments to call this function with.
        """
        self._queue.put(item=(target, kwargs))

    def wait(self, timeout: Optional[int | float]) -> None:
        """
        Wait for the workers to finish.

        Args:
            timeout: Seconds to wait for workers to finish. No time limit when value is None.

        Raises:
            ChildProcessError: Worker(s) failed while processing work.
            TimeoutError: Worker(s) did not finish before timeout.
        """
        for event in self._events:
            event.clear()

        for event in self._events:
            if not event.wait(timeout=timeout):
                if any(worker.exitcode for worker in self._workers):
                    raise ChildProcessError("Worker(s) failed while processing work.")

                raise TimeoutError("Worker(s) did not finish before timeout.")

    def request_variable(self, name: str, value: VariableType) -> Variable:
        """
        Request a variable which can be shared between workers.

        Args:
            name: Name of the variable.
            value: Initial value of the variable.

        Returns:
            Variable instance with the given name and value.

        Raises:
            TypeError: Type of the value not supported.
        """
        size = get_variable_size(value=value)
        memory = self._manager_mem.SharedMemory(size=size)
        lock = self._manager_sync.Lock()
        variable = Variable(name=name, value=value, memory=memory.name, lock=lock)

        self._memory.append(memory)
        self._locks.append(lock)
        self._variables.append(variable)

        return variable
