"""
https://discourse.prefect.io/t/set-name-for-flow-run-and-mapped-task-runs/1866/3

Not working.
We are waiting on feature request:

https://github.com/PrefectHQ/prefect/issues/7463
"""
from pprint import pprint

from prefect import flow, task, context
from prefect.orion.schemas.actions import FlowRunUpdate
from prefect.orion.api.flow_runs import update_flow_run


@task
def get_names():
    return ["Amber", "Barbara", "Charlie"]


@task(tags=['max_two_tasks'])
def say_hello(name):
    print(f"Hello {name}!")


@task
def dump_ctx():
    ctx = context.get_run_context()
    pprint(ctx)


from prefect.orion.database.dependencies import provide_database_interface


@task
async def set_flowrun_name():
    ctx = context.get_run_context()
    await update_flow_run(FlowRunUpdate(name='whatever'), ctx.task_run.flow_run_id, provide_database_interface())


@flow(name="hello_name")
def hello_flow():
    flow_run_name = set_flowrun_name()
    names = get_names()
    hellos = [say_hello.with_options(name=f'hello-{name}')(name) for name in names]
    dump_ctx()


if __name__ == '__main__':
    hello_flow()
