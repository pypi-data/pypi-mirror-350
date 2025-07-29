import asyncio
import uuid
import subprocess
from typing import Dict, Optional, Callable, Any
from anmvc.storage import save_containers, load_containers, save_tasks, load_tasks, save_environments, load_environments
from loguru import logger
from anmvc.environment import Environment

class Container:
    def __init__(self, name: Optional[str] = None, cid: Optional[str] = None):
        self.id = cid or str(uuid.uuid4())
        self.name = name or f"container-{self.id[:8]}"
        self._task: Optional[asyncio.Task] = None
        self._running = False
        self._stop_event = asyncio.Event()

    async def _run(self):
        self._running = True
        self._stop_event.clear()
        logger.info(f"[{self.name}] Starting container...")
        try:
            while not self._stop_event.is_set():
                logger.debug(f"[{self.name}] Running...")
                await asyncio.sleep(2)
        except asyncio.CancelledError:
            logger.info(f"[{self.name}] Stopping container (cancelled).")
            raise
        finally:
            self._running = False
            logger.info(f"[{self.name}] Container stopped.")

    def start(self):
        if self._running:
            logger.warning(f"[{self.name}] Already running!")
            return
        self._running = True
        self._task = asyncio.create_task(self._run())

    async def stop(self):
        if not self._running or not self._task:
            logger.warning(f"[{self.name}] Not running.")
            return
        self._stop_event.set()
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        self._task = None
        self._running = False
        logger.info(f"[{self.name}] Stopped.")

    @property
    def is_running(self):
        return self._running


class Task:
    def __init__(
            self,
            name: str,
            container_id: str,
            task_type: str = "repeat",
            command: Optional[str] = None,
            interval: float = 2.0,
            module_func: Optional[Callable] = None,
            tid: Optional[str] = None,
    ):
        self.id = tid or str(uuid.uuid4())
        self.name = name
        self.container_id = container_id
        self.task_type = task_type
        self.command = command
        self.interval = interval
        self.module_func = module_func
        self._task: Optional[asyncio.Task] = None
        self._stop_event = asyncio.Event()

    async def _run_repeat(self):
        logger.info(f"[Task {self.name}] Running repeat task...")
        try:
            while not self._stop_event.is_set():
                if self.command:
                    subprocess.run(self.command, shell=True)
                else:
                    logger.warning(f"[Task {self.name}] No shell command provided.")
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logger.info(f"[Task {self.name}] Repeat task cancelled.")
            raise

    async def _run_repeat_on_interval(self):
        logger.info(f"[Task {self.name}] Running repeat_on_interval task every {self.interval} seconds...")
        try:
            while not self._stop_event.is_set():
                if self.command:
                    subprocess.run(self.command, shell=True)
                else:
                    logger.warning(f"[Task {self.name}] No shell command provided.")
                await asyncio.sleep(self.interval)
        except asyncio.CancelledError:
            logger.info(f"[Task {self.name}] Repeat_on_interval task cancelled.")
            raise

    async def _run_shell_once(self):
        logger.info(f"[Task {self.name}] Running shell task once...")
        try:
            if self.command:
                subprocess.run(self.command, shell=True)
            else:
                logger.warning(f"[Task {self.name}] No shell command provided.")
        except Exception as e:
            logger.error(f"[Task {self.name}] Shell task error: {e}")
        finally:
            logger.info(f"[Task {self.name}] Shell task done.")

    async def _run_module_type(self):
        logger.info(f"[Task {self.name}] Running module_type task...")
        try:
            if self.module_func:
                if asyncio.iscoroutinefunction(self.module_func):
                    await self.module_func()
                else:
                    self.module_func()
            else:
                logger.warning(f"[Task {self.name}] No module function provided.")
        except Exception as e:
            logger.error(f"[Task {self.name}] Module task error: {e}")
        finally:
            logger.info(f"[Task {self.name}] Module task done.")

    async def _task_runner(self):
        if self.task_type == "repeat":
            await self._run_repeat()
        elif self.task_type == "repeat_on_interval":
            await self._run_repeat_on_interval()
        elif self.task_type == "shell":
            await self._run_shell_once()
        elif self.task_type == "module_type":
            await self._run_module_type()
        else:
            logger.warning(f"[Task {self.name}] Unknown task_type '{self.task_type}'")

    def start(self):
        if self._task and not self._task.done():
            logger.warning(f"[Task {self.name}] Already running!")
            return
        self._stop_event.clear()
        self._task = asyncio.create_task(self._task_runner())

    async def stop(self):
        if not self._task:
            logger.warning(f"[Task {self.name}] Not running.")
            return
        self._stop_event.set()
        self._task.cancel()
        try:
            await self._task
        except asyncio.CancelledError:
            pass
        self._task = None
        logger.info(f"[Task {self.name}] Stopped.")

    @property
    def is_running(self):
        return self._task is not None and not self._task.done()


class ContainerManager:
    def __init__(self):
        self.containers: Dict[str, Container] = {}
        self.tasks: Dict[str, Task] = {}
        self._load_lock = asyncio.Lock()
        self.environments = {}

    async def load(self):
        async with self._load_lock:
            containers_data = await load_containers()
            tasks_data = await load_tasks()
            environment_data = await load_environments()
            self.environments = {}

            self.containers = {}
            for cid, info in containers_data.items():
                c = Container(name=info.get("name"), cid=cid)
                self.containers[cid] = c
            self.tasks = {}
            for tid, info in tasks_data.items():
                t = Task(
                    name=info.get("name"),
                    container_id=info.get("container_id"),
                    task_type=info.get("task_type", "repeat"),
                    command=info.get("command"),
                    interval=info.get("interval", 2.0),
                    tid=tid,
                )
                self.tasks[tid] = t
            for env_id, info in environment_data.items():
                env = Environment(
                    container_id=info.get("container_id"),
                    name=info.get("name"),
                    shell_type=info.get("shell_type"),
                    eid=env_id,
                )
                self.environments[env_id] = env

            logger.info(f"Loaded {len(self.containers)} containers and {len(self.tasks)} tasks from storage.")

    async def save(self):
        containers_data = {
            cid: {"name": c.name, "running": c.is_running}
            for cid, c in self.containers.items()
        }
        tasks_data = {
            tid: {
                "name": t.name,
                "container_id": t.container_id,
                "task_type": t.task_type,
                "command": t.command,
                "interval": t.interval,
            }
            for tid, t in self.tasks.items()
        }
        environments_data = {
            env_id: {
                "container_id": env.container_id,
                "name": env.name,
                "shell_type": env.shell_type,
            }
            for env_id, env in self.environments.items()
        }
        await save_containers(containers_data)
        await save_tasks(tasks_data)
        await save_environments(environments_data)
        logger.debug("Saved containers and tasks to storage.")

    async def create_container(self, name: Optional[str] = None) -> Container:
        container = Container(name)
        self.containers[container.id] = container
        logger.info(f"Created container {container.name} with ID {container.id}")
        await self.save()
        return container

    async def create_task(
            self,
            name: str,
            container_id: str,
            task_type: str = "repeat",
            command: Optional[str] = None,
            interval: float = 2.0,
    ) -> Optional[Task]:
        if container_id not in self.containers:
            logger.error(f"Cannot create task; container ID {container_id} not found.")
            return None
        task = Task(name, container_id, task_type, command, interval)
        self.tasks[task.id] = task
        logger.info(f"Created task {task.name} ({task.id}) in container {container_id}")
        await self.save()
        return task

    def list_containers(self):
        return list(self.containers.values())

    def list_tasks(self, container_id: Optional[str] = None):
        if container_id:
            return [t for t in self.tasks.values() if t.container_id == container_id]
        return list(self.tasks.values())

    def get_container(self, container_id: str) -> Optional[Container]:
        return self.containers.get(container_id)

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    async def start_container(self, container_id: str):
        container = self.get_container(container_id)
        if container:
            container.start()
            logger.info(f"Started container {container.name}")
            # Start all tasks for this container automatically
            tasks_for_container = [t for t in self.tasks.values() if t.container_id == container_id]
            for t in tasks_for_container:
                t.start()
                logger.info(f"Started task {t.name} ({t.id}) for container {container.name}")
            await self.save()
        else:
            logger.error(f"No container with ID {container_id}")

    async def stop_container(self, container_id: str):
        container = self.get_container(container_id)
        if container:
            # Stop all tasks first
            tasks_for_container = [t for t in self.tasks.values() if t.container_id == container_id]
            await asyncio.gather(*(t.stop() for t in tasks_for_container if t.is_running))
            await container.stop()
            logger.info(f"Stopped container {container.name}")
            await self.save()
        else:
            logger.error(f"No container with ID {container_id}")

    async def start_task(self, task_id: str):
        task = self.get_task(task_id)
        if task:
            container = self.get_container(task.container_id)
            if container and not container.is_running:
                container.start()
                logger.info(f"Started container {container.name} for task {task.name}")
            task.start()
            logger.info(f"Started task {task.name} ({task_id})")
        else:
            logger.error(f"Task {task_id} not found")

    async def stop_task(self, task_id: str):
        task = self.get_task(task_id)
        if task and task.is_running:
            await task.stop()
            logger.info(f"Stopped task {task.name} ({task_id})")
        else:
            logger.warning(f"Task {task_id} not running or not found")

    async def delete_container(self, container_id: str):
        if container_id in self.containers:
            # Stop container and tasks first
            await self.stop_container(container_id)
            # Remove all tasks of container
            tasks_to_delete = [tid for tid, t in self.tasks.items() if t.container_id == container_id]
            for tid in tasks_to_delete:
                del self.tasks[tid]
            del self.containers[container_id]
            logger.info(f"Deleted container {container_id} and its tasks")
            await self.save()
        else:
            logger.error(f"Container {container_id} not found")

    async def delete_task(self, task_id: str):
        if task_id in self.tasks:
            await self.stop_task(task_id)
            del self.tasks[task_id]
            logger.info(f"Deleted task {task_id}")
            await self.save()
        else:
            logger.error(f"Task {task_id} not found")

    # Environment methods
    async def create_environment(self, container_id: str, name: str, shell_type: str) -> Environment:
        if container_id not in self.containers:
            return None
        env = Environment(container_id=container_id, name=name, shell_type=shell_type)
        self.environments[env.id] = env
        await self.save()
        return env

    def list_environments(self, container_id: str = None):
        if container_id:
            return [env for env in self.environments.values() if env.container_id == container_id]
        return list(self.environments.values())

    async def start_environment(self, env_id: str):
        env = self.environments.get(env_id)
        if not env:
            raise ValueError("Environment not found")
        await env.start()

    async def stop_environment(self, env_id: str):
        env = self.environments.get(env_id)
        if not env:
            raise ValueError("Environment not found")
        await env.stop()

    async def run_command_in_environment(self, env_id: str, command: str) -> str:
        env = self.environments.get(env_id)
        if not env:
            raise ValueError("Environment not found")
        return await env.run_command(command)

    async def enter_environment(self, env_id: str):
        env = self.environments.get(env_id)
        if not env:
            raise ValueError("Environment not found")
        await env.interact()

    async def delete_environment(self, env_id: str):
        if env_id in self.environments:
            await self.stop_environment(env_id)
            del self.environments[env_id]
            await self.save()
        else:
            logger.error(f"Environment {env_id} not found")