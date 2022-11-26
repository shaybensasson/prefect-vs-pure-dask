"""
Just a sanity to fast test docker images.
"""
import logging
from pprint import pprint
from timeit import default_timer as timer
from typing import Optional

import lightgbm
import pandas as pd
import sklearn.datasets

_logger = logging.getLogger(__name__)


def train_lightgbm_and_evaluate_performance(X_train: pd.DataFrame, y_train: pd.DataFrame,  # noqa: N803
                                            X_validation: pd.DataFrame, y_validation: pd.DataFrame,
                                            *,
                                            n_jobs: Optional[int] = None) -> dict:
    """Trains a LightGBM model and evaluates its performance on the validation set."""

    lgbm_hyperparameters = {'learning_rate': 0.03,
                            'min_split_gain': 0.012,
                            'max_depth': 5,
                            'num_leaves': 15,
                            'n_estimators': 1000,
                            'objective': 'binary',
                            'min_child_samples': 30,
                            'reg_alpha': 0.007,
                            'reg_lambda': 0.033,
                            'is_unbalance': True,
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


if __name__ == '__main__':
    data, target = sklearn.datasets.load_breast_cancer(return_X_y=True, as_frame=True)
    pprint(train_lightgbm_and_evaluate_performance(data, target, data, target, n_jobs=None))
