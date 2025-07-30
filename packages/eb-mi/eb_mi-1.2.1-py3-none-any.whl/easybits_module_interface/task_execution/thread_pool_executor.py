from concurrent.futures import ThreadPoolExecutor
from uuid import uuid4


class ManagedThreadPoolExecutor:
    """
    Implementation of a managed ThreadPoolExecutor.

    Allows seamless scheduling of unstable function calls.
    This implementation will spin up new instances of ThreadPoolExecutor
    if threads are supposed to be cancelled.

    See usage inside `./thread_executor.py`
    """
    def __init__(self, max_workers=None, logger=None):
        self.max_workers = max_workers
        self.current_executor = None
        self.current_executor_id = None
        self.frozen_executors = {}
        self.task_map = {}
        self.frozen_tasks = {}
        self.logger = logger
        self.requires_restart = False

    def _get_executor(self):
        """
        Factory function for new ThreadPoolExecutor instances

        :returns: Tuple of ThreadPoolExecutor instance and it's UID
        """
        return ThreadPoolExecutor(max_workers=self.max_workers), str(uuid4())

    def submit(self, func, process_id, *args, **kwargs):
        """
        Method to submit async Callable with its ID to the current thread pool executor.

        :param func: An async Callable to execute
        :param process_id: UID of the process
        :returns: A Future for the callable
        """
        if self.current_executor is None:
            self.logger.debug('Creating new executor')
            self.current_executor, self.current_executor_id = self._get_executor()
        if self.current_executor_id not in self.task_map:
            self.task_map[self.current_executor_id] = []

        self.task_map[self.current_executor_id].append(process_id)

        return self.current_executor.submit(func, *args, **kwargs)

    def shutdown(self) -> None:
        """
        Method to shut down all executors in the running ManagedThreadPoolExecutor instance.

        :returns: Nothing
        """
        if self.current_executor is not None:
            self.current_executor.shutdown()
        for executor in self.frozen_executors:
            executor.shutdown(wait=False)

        self.frozen_executors.clear()
        self.current_executor = None
        self.current_executor_id = None

    def _remove_executor(self, executor_id) -> None:
        """
        Helper method to _gracefully_ remove an executor.

        :param executor_id: the ID of the executor
        :returns: Nothing
        """
        if executor_id in self.frozen_executors:
            self.frozen_executors[executor_id].shutdown(wait=False)
        self.frozen_executors = {k: v for k, v in self.frozen_executors.items() if k != executor_id}
        self.task_map = {k: v for k, v in self.task_map.items() if k != executor_id}
        self.frozen_tasks = {k: v for k, v in self.frozen_tasks.items() if k != executor_id}

    def _handle_task_list(self, task_list, is_cancelled=False):
        """
        Method to handle finished tasks.

        This method "freezes" thread pools and resets the current executor if it contains
        a stale task.

        :param task_list: List of finished tasks
        :param is_cancelled: Indicates that `task_list` is a list of cancelled tasks
        :returns: A list of executor IDs of executors that can be safely shut down.
        """
        executors_to_remove = []
        for idx in task_list:
            for executor_id, tasks in filter(lambda x: idx in x[1], self.task_map.items()):
                if is_cancelled:
                    if executor_id == self.current_executor_id:
                        self.frozen_executors[executor_id] = self.current_executor
                        self.current_executor = None
                        self.current_executor_id = None
                        self.requires_restart = True

                    if executor_id not in self.frozen_tasks:
                        self.frozen_tasks[executor_id] = []
                    self.frozen_tasks[executor_id].append(idx)

                self.task_map[executor_id] = [i for i in self.task_map[executor_id] if i != idx]
                # if no more unfrozen tasks for frozen executor, remove it
                if len(self.task_map[executor_id]) == 0 and executor_id != self.current_executor_id:
                    executors_to_remove.append(executor_id)
        return executors_to_remove

    def garbage_collect(self, finished_tasks, cancelled_tasks) ->None:
        """
        Method to garbage collect inside of running thread pools.

        :param finished_tasks: List of tasks that are finished
        :param cancelled_tasks: List of tasks that are cancelled
        :returns: Nothing
        """
        # remove finished tasks from task_map
        executors_to_remove = (
            self._handle_task_list(finished_tasks)
            + self._handle_task_list(cancelled_tasks, is_cancelled=True)
        )

        for executor_id, executors in self.frozen_executors.items():
            if self.task_map.get(executor_id, None) in [None, []]:
                executors_to_remove.append(executor_id)

        for executor_id in set(executors_to_remove):
            self.logger.debug(f'Removing executor {executor_id}')
            self._remove_executor(executor_id)


