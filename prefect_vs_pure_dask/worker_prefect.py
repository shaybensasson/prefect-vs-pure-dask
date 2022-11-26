"""
The dask worker implementation. Electrode subset features training, evaluation and saving of the performance metrics is done here.
"""
from pprint import pprint
import random
import time
from timeit import default_timer as timer
from typing import Optional, cast

import lightgbm
import pandas as pd
from prefect import flow, get_run_logger, task
from prefect.context import TaskRunContext
import sklearn.datasets
import prefect.states


def _train_and_evaluate_model(X_train: pd.DataFrame, y_train: pd.DataFrame,  # noqa: N803
                              X_validation: pd.DataFrame, y_validation: pd.DataFrame,
                              *,
                              n_jobs: Optional[int] = None) -> dict:
    """Trains a LightGBM model and evaluates its performance on the validation set."""

    _logger = get_run_logger()

    lgbm_hyperparameters = {
        'n_estimators': 1000,
        'objective': 'binary',
        'n_jobs': n_jobs}

    # train a lightgbm model
    clf = lightgbm.LGBMClassifier(**lgbm_hyperparameters)

    _logger.info(f"Training LightGBM model on {X_train.shape=}, {y_train.shape=} ...")
    timer_start = timer()
    clf.fit(X=X_train, y=y_train)
    training_duration_in_sec = timer() - timer_start

    # inference on internal validation-set
    _logger.info(f"Performing inference on {X_validation.shape=} ...")
    timer_start = timer()
    y_proba = clf.predict_proba(X_validation)[:, 1]

    inference_duration_in_sec = timer() - timer_start

    _logger.info(f"Evaluating performance using {y_validation.shape=} ...")
    # calc performance metrics
    return {
        'some_metric': sklearn.metrics.roc_auc_score(y_validation, y_proba),

        "training_duration_in_sec": training_duration_in_sec,
        "inference_duration_in_sec": inference_duration_in_sec,
    }


@task
def train_and_evaluate_model(i_job: int) -> dict:
    # data, target = sklearn.datasets.load_breast_cancer(return_X_y=True, as_frame=True)

    # NOTE: This is a workaround - we can't change the task run name in Perfect v2.0 yet :(
    ctx = cast(TaskRunContext, prefect.context.get_run_context())
    ctx.task_run.name = f"train_and_evaluate_model_{i_job}"
    get_run_logger(ctx).info(f"train_and_evaluate_model({i_job=}): 😴 ...")

    time.sleep(5 * random.random())

    the_result = {
        'some_metric': None,

        "training_duration_in_sec": None,
        "inference_duration_in_sec": None,
    }
    # return prefect.states.Completed(message=f"Job {i_job} processed successfully ✅", result=the_result)
    return the_result


@flow
def the_demo_flow():
    """A demo flow."""
    pprint(train_and_evaluate_model(0))


if __name__ == '__main__':
    with prefect.tags("dev"):
        the_demo_flow()
