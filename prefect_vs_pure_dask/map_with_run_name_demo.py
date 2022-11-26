"""
https://discourse.prefect.io/t/set-name-for-flow-run-and-mapped-task-runs/1866/3

Not working.
We are waiting on feature request:

https://github.com/PrefectHQ/prefect/issues/7463
"""
import prefect
from prefect import get_run_logger, flow, task
from prefect.orion.api.flow_runs import update_flow_run
from prefect.orion.database.dependencies import provide_database_interface
from prefect.orion.schemas.actions import FlowRunUpdate


@task
async def set_flowrun_name():
    ctx = prefect.context.get_run_context()
    await update_flow_run(FlowRunUpdate(name='runtime_task_run_name'), ctx.task_run.flow_run_id, provide_database_interface())


@flow
def the_flow():
    get_run_logger().info(f"the_flow(): Starting ...")
    set_flowrun_name()
    get_run_logger().info(f"the_flow(): Done.")


if __name__ == '__main__':
    the_flow()
