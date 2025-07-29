import aiofiles
import json
import os

CONTAINERS_FILE = "containers.json"
TASKS_FILE = "tasks.json"
ENV_FILE = "environments.json"

async def save_containers(data: dict):
    async with aiofiles.open(CONTAINERS_FILE, "w") as f:
        await f.write(json.dumps(data, indent=2))

async def load_containers() -> dict:
    if not os.path.exists(CONTAINERS_FILE):
        return {}
    async with aiofiles.open(CONTAINERS_FILE, "r") as f:
        content = await f.read()
        return json.loads(content)

async def save_tasks(data: dict):
    async with aiofiles.open(TASKS_FILE, "w") as f:
        await f.write(json.dumps(data, indent=2))

async def load_tasks() -> dict:
    if not os.path.exists(TASKS_FILE):
        return {}
    async with aiofiles.open(TASKS_FILE, "r") as f:
        content = await f.read()
        return json.loads(content)

async def save_environments(data: dict):
    async with aiofiles.open(ENV_FILE, "w") as f:
        await f.write(json.dumps(data, indent=2))

async def load_environments() -> dict:
    if not os.path.exists(ENV_FILE):
        return {}
    async with aiofiles.open(ENV_FILE, "r") as f:
        content = await f.read()
        return json.loads(content)