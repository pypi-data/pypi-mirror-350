import asyncio
from dataclasses import dataclass, field, asdict
from functools import partial
from datetime import datetime
from itertools import count
from typing import Callable, Optional
from collections import defaultdict
from easybits_module_interface.models import Message, MessageTypes
from uuid import uuid4
from copy import deepcopy
from easybits_module_interface.task_execution.thread_pool_executor import ManagedThreadPoolExecutor
from easybits_module_interface.task_execution.models import GenerationRequest, RunningTask


def sync_wrapper(func: Callable) -> Callable:
    """
    Decorator style implementation wrapping any callable Future
    into a synchronous task.
    """
    def inner(*args, **kwargs):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(func(*args, **kwargs))
        loop.close()
        return result
    return inner


class TaskExecutor:
    """
    TaskExecutor class to manage the execution of tasks in a thread pool.

    The class is responsible for:
    - Scheduling tasks in a thread pool
    - Handling finished tasks
    - Notifying users about timeouts
    - Sending out results to users
    - Sending out verbose results to users
    - Publishing status messages
    - Handling rate limits
    - Handling task timeouts
    - Handling errors

    To add custom behavior for...
    - Notifying users about timeouts: Override the `notify_timeout` method
    - Sending out verbose results: Override the `notify_verbose_result` method
    - Notifying users about task timeouts: Override the `notify_execution_timeout` method

    """
    def __init__(self, error_responses, logger):
        # token based process map, to maintain pending tasks
        self.process_queue = {}
        # status messages used to sed out status messages from running/pending tasks
        self.status_messages = []
        # copy of/reference to error responses dictionary from module
        self.error_responses = error_responses
        # constant for token based rate limiting
        self.max_tasks_per_owner = 5
        # constant for number of parallel threads (keep it 64!)
        self.max_running_tasks = 64
        # map for detailed rate limits - currently everyone is treaded equally
        self.max_running_tasks_owner_map = defaultdict(lambda: self.max_tasks_per_owner)
        # list of currently running tasks
        self.running_tasks = []
        # map for rate limits
        self.running_tasks_map = defaultdict(int)
        # a reference to the module logger
        self.logger = logger

    async def publish(self, message: Message) -> None:
        """
        Method to publish a message to RMQ.
        Dynamically set this to inject outside functionality.

        See the module_implementation.py for more details.
        """
        raise NotImplementedError('Attach method after instantiation!')

    async def notify_timeout(self, process: GenerationRequest) -> None:
        """
        Method to notify a user about a timeout in their task.

        Override this method to implement custom behavior.
        """
        pass

    def _update_rate_limit(self, owner_id, change: int) -> None:
        self.running_tasks_map[owner_id] += change
        if self.running_tasks_map[owner_id] <= 0:
            del self.running_tasks_map[owner_id]

    async def notify(self, processes: list[GenerationRequest | RunningTask]) -> None:
        """
        Method to notify users about progress in processes.

        :param processes: List of running task objects
        :returns: Nothing
        """
        for p in processes:
            if isinstance(p, GenerationRequest):
                process = p
            elif isinstance(p, RunningTask):
                process = p.generation_request
            else:
                raise ValueError('Invalid type for process')

            # notify unnotified users about delays in their tasks
            if not process.notified and (datetime.now() - process.timestamp).seconds > process.timeout:
                await self.notify_timeout(process)
                process.notified = True

    async def schedule_task(self, free_workers: int, pool: ManagedThreadPoolExecutor) -> None:
        """
        Method to schedule a pending task in the thread pool.

        1. iterates over list of pending tasks
        2. checks for rate limit
        3. then schedules the first task that is allowed to be scheduled

        :param free_workers: number of free workers in the thread pool
        :param pool: the pool to schedule the task in
        :returns: Nothing
        """
        if min(free_workers, len(self.process_queue)) <= 0:
            return

        found = False
        p_id = None
        # search for task that is allowed to be scheduled
        for p_id, p in self.process_queue.items():
            running_for_owner = self.max_running_tasks_owner_map[p.owner_id]
            if (p.owner_id not in self.running_tasks_map
                or self.running_tasks_map[p.owner_id] < running_for_owner):
                found = True
                break

        if not found:
            return

        # schedule task
        generation_request = self.process_queue.pop(p_id)
        generation_request.execution_timestamp = datetime.now()
        thread = pool.submit(sync_wrapper(generation_request.method), p_id)
        task = RunningTask(generation_request, thread)
        self.running_tasks.append(task)

        # update rate limit map
        self._update_rate_limit(generation_request.owner_id, 1)

        self.logger.debug(
            f'Scheduled task {generation_request.task_id}. '
            f'{len(self.running_tasks)} tasks running. '
            f'{len(self.process_queue)} tasks pending. '
            f'{len(pool.task_map)} executors in pool running '
            f'{sum(len(v) for v in pool.task_map.values())} tasks ('
            f'{len(pool.frozen_executors)} frozen executors with '
            f'{sum(len(v) for v in pool.frozen_tasks.values())} tasks)'
        )

    async def notify_verbose_result(self, msg: Message) -> None:
        """
        Method to notify the user about a verbose result.

        Override this method to implement custom behavior.
        """
        pass

    async def sendout_result(self, msg: Message, is_success: bool) -> None:
        """
        Send out the result of a task to the user.

        :param msg: The original message to send out
        :param is_success: Whether the task was successfully executed
        :return: None
        """
        msg.meta.event = 'success_response' if is_success else 'error_response'
        await self.publish(msg)
        verbose = msg.config.get('verbose', 0)
        try:
            verbose = int(verbose)
        except ValueError:
            verbose = 0

        if not is_success or verbose < 2:
            return

        # sendout verbose message
        await self.notify_verbose_result(msg)

    async def handle_finished_task(self, running_task: GenerationRequest) -> None:
        """
        Method to handle a finished task

        :param running_task: The reference to the finished task
        :returns: Nothing
        """
        result = running_task.task.result()
        if result:
            message, is_success = result
            await self.sendout_result(message, is_success)

        self._update_rate_limit(running_task.generation_request.owner_id, -1)
        self.running_tasks_map[running_task.generation_request.owner_id] -= 1
        self.logger.debug(
            f'Task {running_task.generation_request.task_id} done. '
            f'{len(self.running_tasks) - 1} tasks running. '
            f'{len(self.process_queue)} tasks pending. '
        )

    async def notify_execution_timeout(self, running_task: GenerationRequest) -> None:
        """
        Method to notify a user about a timeout in their task.

        Override this method to implement custom behavior.

        :param running_task: The reference to the task that timed out
        """
        pass

    async def handle_execution_timeout(self, running_task: GenerationRequest) -> None:
        """
        Method to handle a task that timed out.

        :param running_task: The reference to the task that timed out
        :returns: Nothing
        """
        success = running_task.task.cancel()
        self._update_rate_limit(running_task.generation_request.owner_id, -1)

        if running_task.generation_request.verbose > 1:
            # send out verbose message for timeout
            await self.notify_execution_timeout(running_task)

        self.logger.debug(
            f'TIMEOUT: Task {running_task.generation_request.task_id} killed. '
            f'{len(self.running_tasks) - 1} tasks running. '
            f'{len(self.process_queue)} tasks pending. '
        )

    async def check_finished_tasks(self) -> tuple[list[int], list[int]]:
        """
        Check for finished (positive/negative) tasks and handle them appropriately

        :returns: Tuple of list of still pending tasks, successful tasks and list of cancelled tasks
        """
        pending_tasks = []
        cancelled_tasks = []
        successful_tasks = []
        for running_task in self.running_tasks:
            idx = running_task.generation_request.task_id
            if running_task.task.done():
                await self.handle_finished_task(running_task)
                successful_tasks.append(idx)
                continue
            elif ((datetime.now() - running_task.generation_request.execution_timestamp).seconds 
                > running_task.generation_request.execution_timeout * 60):
                await self.handle_execution_timeout(running_task)
                cancelled_tasks.append(idx)
                continue
            else:
                pending_tasks.append(idx)
        return pending_tasks, successful_tasks, cancelled_tasks

    async def publish_status_messages(self) -> None:
        """
        Helper method to publish scheduled status messages

        :returns: Nothing
        """
        if self.status_messages:
            for msg in self.status_messages:
                await self.publish(msg)
            self.status_messages = []

    async def run(self) -> None:
        """
        Consume scheduled tasks from the `process_queue` and execute them.

        The tasks are executed in a thread pool, so the main event loop is not blocked.
        While processing, the module will occasional publish status messages to the `outgoing_messages` exchange.

        If threads become stale due to issues on HF the thread pool will notify and terminate the current
        process.
        This will cause a call of this method again.
        """
        pool = ManagedThreadPoolExecutor(None, self.logger)
        while True:
            if not self.process_queue and not self.running_tasks and not self.status_messages:
                if pool.requires_restart:
                    self.logger.debug('Restarting task executor')
                    break
                await asyncio.sleep(.1)
                continue

            # schedule new task
            free_workers = self.max_running_tasks - len(self.running_tasks)
            await self.schedule_task(free_workers, pool)

            # notify user about timeouts in pending tasks
            await self.notify(list(self.process_queue.values()))

            # check for finished tasks
            pending_tasks, successful_tasks, cancelled_tasks = await self.check_finished_tasks()
            self.running_tasks = [t for t in filter(lambda x: x.generation_request.task_id in pending_tasks, self.running_tasks)]

            # notify user about timeouts in running tasks
            await self.notify(self.running_tasks)

            # publish status messages produced by tasks
            await self.publish_status_messages()
            pool.garbage_collect(successful_tasks, cancelled_tasks)
            await asyncio.sleep(1)
        pool.shutdown()

