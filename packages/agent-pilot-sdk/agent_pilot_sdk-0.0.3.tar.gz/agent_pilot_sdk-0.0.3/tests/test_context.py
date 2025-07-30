from agent_pilot.context import (
    RunManager,
)


class TestRunManager:
    def test_run_manager_initialization(self):
        """Test the initialization of RunManager."""
        manager = RunManager()

        # Verify initial state
        assert manager.current_run is None
        assert manager.current_run_id is None
        assert manager.runs == {}

    def test_run_manager_start_run(self):
        """Test starting a run with RunManager."""
        manager = RunManager()

        # Start a run
        run_id = 'test-run-id'
        task_id = 'test-task'
        version = 'v1'

        run = manager.start_run(run_id, task_id, version)

        # Verify run state
        assert manager.current_run is not None
        assert manager.current_run_id == run.id
        assert run.task_id == task_id
        assert run.version == version

    def test_run_manager_end_run(self):
        """Test ending a run with RunManager."""
        manager = RunManager()

        # Start and end a run
        run = manager.start_run('test-run-id', 'test-task', 'v1')
        manager.end_run(run.id)

        # Verify run was ended
        assert manager.current_run is None
        assert manager.current_run_id is None
        assert run.id not in manager.runs

    def test_run_manager_nested_runs(self):
        """Test nested runs with RunManager."""
        manager = RunManager()

        # Start parent run
        parent_run_id = 'parent-run-id'
        parent_task_id = 'parent-task'
        parent_version = 'v1'

        parent_run = manager.start_run(parent_run_id, parent_task_id, parent_version)

        # Store parent ID
        parent_id = parent_run.id

        # Start child run
        child_run_id = 'child-run-id'
        child_task_id = 'child-task'
        child_version = 'v2'

        child_run = manager.start_run(child_run_id, child_task_id, child_version)

        # Verify child run
        assert manager.current_run_id == child_run.id
        assert manager.current_run_id != parent_id
        assert child_run.task_id == child_task_id
        assert child_run.parent_run_id == parent_id

        # End child run
        manager.end_run(child_run.id)

        # Verify returned to parent run
        assert manager.current_run_id == parent_id
        assert manager.current_run.task_id == parent_task_id
