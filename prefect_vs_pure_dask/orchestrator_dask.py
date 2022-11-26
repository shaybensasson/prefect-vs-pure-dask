"""
Orchestration of using dask only
"""
import logging
from typing import Any, Dict

from distributed import Client, as_completed
from tqdm import tqdm

from prefect_vs_pure_dask.worker_dask import train_and_evaluate_model

FLOW_NAME = "prefect-vs-pure-dask__dask"

_logger = logging.getLogger(__name__)


def the_flow(cluster_client_kwargs: Dict[str, Any]) -> None:
    with Client(**cluster_client_kwargs) as client:
        futures = []

        for i in range(1000):
            key = f"job{i}"

            future = client.submit(
                train_and_evaluate_model,
                i,
                # submit() kwargs
                key=key,
            )

            futures.append(future)

        # upon each future completion collect results
        with tqdm(total=len(futures)) as t:
            for future in as_completed(futures, with_results=False, raise_errors=False):
                t.set_description(future.key)
                t.update()

                try:
                    future.result()
                except Exception as e:
                    _logger.error(f"Failed to complete future {future.key} with error {e}.", exc_info=e)
                    continue


if __name__ == '__main__':
    cluster_client_kwargs = dict(address="tcp://0.0.0.0:8786")

    the_flow(
        cluster_client_kwargs=cluster_client_kwargs,
    )
