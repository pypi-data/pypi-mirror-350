import functools
import asyncio
import click
from anmvc.core import ContainerManager

mgr = ContainerManager()

@click.group()
def cli():
    """Container & Task Manager CLI"""
    pass

def async_command(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))
    return wrapper

# --- Container commands ---

@cli.command()
@click.option('--name', type=str, help='Name of the container')
async def container_create(name):
    await mgr.load()
    c = await mgr.create_container(name)
    print(f"Created container {c.name} with ID {c.id}")


@cli.command()
@async_command
async def container_list():
    await mgr.load()
    containers = mgr.list_containers()
    if not containers:
        print("No containers found.")
    for c in containers:
        print(f"{c.id} | {c.name} | Running: {c.is_running}")


@cli.command()
@async_command
@click.argument('container_id')
async def container_start(container_id):
    await mgr.load()
    await mgr.start_container(container_id)
    print(f"Started container {container_id}")


@cli.command()
@async_command
@click.argument('container_id')
async def container_stop(container_id):
    await mgr.load()
    await mgr.stop_container(container_id)
    print(f"Stopped container {container_id}")


@cli.command()
@async_command
@click.argument('container_id')
async def container_delete(container_id):
    await mgr.load()
    await mgr.delete_container(container_id)
    print(f"Deleted container {container_id}")


# --- Task commands ---

@cli.command()
@async_command
@click.option('--name', required=True, type=str, help='Task name')
@click.option('--container_id', required=True, type=str, help='Container ID to assign task')
@click.option('--task_type', type=click.Choice(['repeat', 'repeat_on_interval', 'shell', 'module_type']), default='repeat', help='Type of task')
@click.option('--cmd', 'task_command', multiple=True, help='Shell command to run (if applicable)')
@click.option('--interval', type=float, default=2.0, help='Interval for repeat_on_interval tasks')
async def task_create(name, container_id, task_type, task_command, interval):
    await mgr.load()
    command_str = " ".join(task_command) if task_command else None
    t = await mgr.create_task(
        name=name,
        container_id=container_id,
        task_type=task_type,
        command=command_str,
        interval=interval,
    )
    if t:
        print(f"Created task {t.name} with ID {t.id} in container {t.container_id}")
    else:
        print("Failed to create task.")


@cli.command()
@async_command
@click.option('--container_id', type=str, help='Filter tasks by container ID')
async def task_list(container_id):
    await mgr.load()
    tasks = mgr.list_tasks(container_id)
    if not tasks:
        print("No tasks found.")
    for t in tasks:
        print(f"{t.id} | {t.name} | Container: {t.container_id} | Type: {t.task_type} | Running: {t.is_running}")


@cli.command()
@async_command
@click.argument('task_id')
async def task_start(task_id):
    await mgr.load()
    await mgr.start_task(task_id)
    print(f"Started task {task_id}")


@cli.command()
@async_command
@click.argument('task_id')
async def task_stop(task_id):
    await mgr.load()
    await mgr.stop_task(task_id)
    print(f"Stopped task {task_id}")


@cli.command()
@async_command
@click.argument('task_id')
async def task_delete(task_id):
    await mgr.load()
    await mgr.delete_task(task_id)
    print(f"Deleted task {task_id}")


# --- Environment commands ---

@cli.command()
@async_command
@click.option('--name', required=True, type=str, help='Environment name')
@click.option('--container_id', required=True, type=str, help='Container ID')
@click.option('--type', 'shell_type', required=True, type=str, help='Shell type (e.g. /bin/bash, pwsh.exe)')
async def create_env(name, container_id, shell_type):
    await mgr.load()
    env = await mgr.create_environment(container_id, name, shell_type)
    if env:
        print(f"Created environment '{env.name}' with ID {env.id} in container {env.container_id}")
    else:
        print("Failed to create environment.")


@cli.command()
@async_command
@click.option('--container_id', type=str, help='Filter by container')
async def list_envs(container_id):
    await mgr.load()
    envs = mgr.list_environments(container_id)
    if not envs:
        print("No environments found.")
    for e in envs:
        print(f"{e.id} | {e.name} | Container: {e.container_id} | Shell: {e.shell_type} | Running: {e.is_running}")


@cli.command()
@async_command
@click.argument('env_id')
async def start_env(env_id):
    await mgr.load()
    await mgr.start_environment(env_id)
    print(f"Started environment {env_id}")


@cli.command()
@async_command
@click.argument('env_id')
async def stop_env(env_id):
    await mgr.load()
    await mgr.stop_environment(env_id)
    print(f"Stopped environment {env_id}")


@cli.command()
@async_command
@click.argument('env_id')
@click.option('--command', required=True, multiple=True, help='Command to run')
async def run_in_env(env_id, command):
    await mgr.load()
    command_str = " ".join(command)
    output = await mgr.run_command_in_environment(env_id, command_str)
    print(output)


@cli.command()
@async_command
@click.option('--env_id', required=True, help='Environment ID to enter')
async def enter_env(env_id):
    await mgr.load()
    try:
        await mgr.enter_environment(env_id)
    except Exception as e:
        print(f"Error: {e}")


@cli.command()
@async_command
@click.option('--env_id', type=str, help='Environment ID')
async def delete_env(env_id):
    await mgr.load()
    try:
        await mgr.delete_environment(env_id)
    except Exception as e:
        print(f"Error: {e}")


def main_sync():
    asyncio.run(cli())

if __name__ == "__main__":
    main_sync()
