"""
Orchestration of using prefect and dask
"""
from pprint import pprint

import prefect
from prefect import flow, get_run_logger
from prefect.futures import PrefectFuture
from prefect_dask import DaskTaskRunner

from prefect_vs_pure_dask.worker_prefect import train_and_evaluate_model

FLOW_NAME = "prefect-vs-pure-dask__prefect"


@flow(name=FLOW_NAME)
def the_flow() -> None:
    _logger = get_run_logger()

    N_JOBS = 10
    # N_JOBS = 1_000
    # increase N_JOBS to 1000 to reproduce the spurious error:
    # raise RuntimeError(
    #   RuntimeError: The connection pool was closed while 2 HTTP requests/responses were still in-flight.

    # Sometimes I also get this:
    # distributed.client - ERROR -
    # Traceback (most recent call last):
    #   File "/home/shay/prefect-vs-pure-dask/.venv/lib/python3.8/site-packages/distributed/client.py", line 1644, in _close
    #     await self.scheduler_comm.close()
    # asyncio.exceptions.CancelledError

    futures = train_and_evaluate_model.map(list(range(N_JOBS)))
    f: PrefectFuture
    results = [f.result() for f in futures]
    pprint(results)

    # for future, result in distributed.as_completed(futures, with_results=True, raise_errors=True):

    # futures = []
    # for i in range(N_JOBS):
    # key = f"job{i}"

    #
    #
    # future = train_and_evaluate_model \
    #     .with_options(name=key,
    #                   # retries=3
    #                   ) \
    #     .submit(i,
    #             # return_state=True
    #             )

    # IMPORTANT: currently, return_state=True, runs the tasks sequentially :(
    # I wish we could get the state but still run the tasks in parallel.
    # FUTURE: shayb | Check this out: https://discourse.prefect.io/t/how-to-add-retries-when-processing-files-and-know-which-files-failed-to-get-processed/1201.

    # futures.append(future)


if __name__ == '__main__':
    # task_runner = SequentialTaskRunner()
    # task_runner = DaskTaskRunner(address="tcp://0.0.0.0:8786")
    task_runner = DaskTaskRunner()

    with prefect.tags(
            "dev"
    ):
        the_flow.with_options(task_runner=task_runner)(
        )

        # input('Dont let the dask cluster go down on me ...')
