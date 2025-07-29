import pytest
from unittest.mock import AsyncMock, patch
from anmvc.core import ContainerManager, Container, Task

@pytest.fixture
def manager():
    mgr = ContainerManager()

    with patch("anmvc.storage.load_containers", new_callable=AsyncMock) as load_containers, \
            patch("anmvc.storage.load_tasks", new_callable=AsyncMock) as load_tasks, \
            patch("anmvc.storage.load_environments", new_callable=AsyncMock) as load_envs, \
            patch("anmvc.storage.save_containers", new_callable=AsyncMock) as save_containers, \
            patch("anmvc.storage.save_tasks", new_callable=AsyncMock) as save_tasks, \
            patch("anmvc.storage.save_environments", new_callable=AsyncMock) as save_envs:

        load_containers.return_value = {}
        load_tasks.return_value = {}
        load_envs.return_value = {}
        save_containers.return_value = None
        save_tasks.return_value = None
        save_envs.return_value = None

        yield mgr


@pytest.mark.asyncio
async def test_create_and_start_container(manager: ContainerManager):
    container = await manager.create_container("test-container")
    assert container.name == "test-container"
    assert container.id in manager.containers

    await manager.start_container(container.id)
    assert container.is_running

    await manager.stop_container(container.id)
    assert not container.is_running


@pytest.mark.asyncio
async def test_create_task_and_start_stop(manager: ContainerManager):
    container = await manager.create_container("test-container")
    task = await manager.create_task(
        name="test-task",
        container_id=container.id,
        task_type="repeat",
        command="echo hello"
    )
    assert task is not None
    assert task.id in manager.tasks

    await manager.start_container(container.id)
    assert task.is_running

    await manager.stop_task(task.id)
    assert not task.is_running

    await manager.start_task(task.id)
    assert task.is_running

    await manager.stop_container(container.id)
    assert not task.is_running
    assert not container.is_running


@pytest.mark.asyncio
async def test_delete_container_and_task(manager: ContainerManager):
    container = await manager.create_container("container-to-delete")
    task = await manager.create_task(
        "task-to-delete",
        container_id=container.id,
        command="echo bye"
    )
    await manager.start_container(container.id)
    assert container.is_running
    assert task.is_running

    await manager.delete_task(task.id)
    assert task.id not in manager.tasks

    await manager.delete_container(container.id)
    assert container.id not in manager.containers


@pytest.mark.asyncio
async def test_load_and_save(manager: ContainerManager):
    container = await manager.create_container("container-for-save")
    task = await manager.create_task(
        "task-for-save",
        container_id=container.id,
        command="echo save"
    )

    await manager.save()


@pytest.mark.asyncio
async def test_start_stop_task_without_container_running(manager: ContainerManager):
    container = await manager.create_container("container-no-auto-start")
    task = await manager.create_task("task1", container_id=container.id, command="echo test")

    await manager.start_task(task.id)
    assert task.is_running
    assert container.is_running

    await manager.stop_task(task.id)
    assert not task.is_running


@pytest.mark.asyncio
async def test_invalid_container_and_task(manager: ContainerManager):
    task = await manager.create_task("bad-task", container_id="invalid-id")
    assert task is None

    await manager.start_container("invalid-id")
    await manager.stop_container("invalid-id")
    await manager.start_task("invalid-task-id")
    await manager.stop_task("invalid-task-id")

    await manager.delete_container("invalid-id")
    await manager.delete_task("invalid-task-id")
