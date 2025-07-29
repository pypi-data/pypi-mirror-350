import numpy as np
from sklearn.base import BaseEstimator, MetaEstimatorMixin
from sklearn.model_selection import cross_val_score, KFold
from hyperopt import fmin, tpe, space_eval, Trials


# From typing
import pandas as pd
from typing import Self


from typing import TypeAlias
from scipy.sparse import spmatrix
import numpy.typing


from typing import Protocol


from collections.abc import Callable
from hyperopt.pyll.base import SymbolTable

from dataclasses import dataclass, field

PARAM = int | float | str | bool
MatrixLike: TypeAlias = np.ndarray | pd.DataFrame | spmatrix
ArrayLike: TypeAlias = numpy.typing.ArrayLike


class _Fitable(Protocol):
    def fit(self, X: MatrixLike, y: ArrayLike) -> Self: ...
    def predict(self, X: MatrixLike) -> ArrayLike: ...
    # def set_params(self, **params: dict[str, PARAM]) -> Self:
    # def set_params(self, **params: Unpack[dict[str, PARAM]]) -> Self:
    # def set_params(self, **params: Unpack[PARAM]) -> Self:
    # def set_params(self, **params: **dict) -> Self:
    def set_params(self, **params: PARAM) -> Self: ...
    def score(self, X: MatrixLike, y: ArrayLike) -> float: ...


class _FitableWithArgs(Protocol):
    def fit(self, X: MatrixLike, y: ArrayLike, *args, **kwargs) -> Self: ...
    def predict(self, X: MatrixLike) -> ArrayLike: ...
    def set_params(self, **params: PARAM) -> Self: ...
    def score(self, X: MatrixLike, y: ArrayLike) -> float: ...


def _cross_val_score_with_fit_params(
    estimator: _FitableWithArgs,
    X: MatrixLike,
    y: ArrayLike,
    cv: int = 5,
    scoring: str | Callable[[ArrayLike, ArrayLike], float] = "neg_mean_squared_error",
    *fit_args,
    **fit_kwargs,
) -> np.ndarray:
    """
    Local implementation of cross_val_score that supports passing fit_params
    to the estimator's fit method.
    """

    kf = KFold(n_splits=cv, shuffle=True, random_state=42)
    scores = []

    for train_index, test_index in kf.split(X):
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]

        estimator.fit(X_train, y_train, *fit_args, **fit_kwargs)
        score = estimator.score(X_test, y_test)
        scores.append(score)

    return np.array(scores)


@dataclass
class StepwiseHyperoptOptimizer(BaseEstimator, MetaEstimatorMixin):
    model: _FitableWithArgs
    param_space_sequence: list[dict[str, PARAM | SymbolTable]]
    max_evals_per_step: int = 100
    cv: int = 5
    scoring: str | Callable[[ArrayLike, ArrayLike], float] = "neg_mean_squared_error"
    random_state: int = 42
    best_params_: dict[str, PARAM] = field(default_factory=dict)
    best_score_: float = None

    def clean_int_params(self, params: dict[str, PARAM]) -> dict[str, PARAM]:
        int_vals = ["max_depth", "reg_alpha"]
        return {k: int(v) if k in int_vals else v for k, v in params.items()}

    def objective(self, params: dict[str, PARAM], *fit_args, **fit_kwargs) -> float:
        # I added this
        params = self.clean_int_params(params)
        # END
        current_params = {**self.best_params_, **params}
        self.model.set_params(**current_params)
        score = _cross_val_score_with_fit_params(
            self.model, self.X, self.y, cv=self.cv, scoring=self.scoring, *fit_args, **fit_kwargs
        )
        return -np.mean(score)

    def fit(self, X: pd.DataFrame, y: pd.Series, *fit_args, **fit_kwargs) -> Self:
        self.X = X
        self.y = y

        for step, param_space in enumerate(self.param_space_sequence):
            print(f"Optimizing step {step + 1}/{len(self.param_space_sequence)}")

            trials = Trials()
            best = fmin(
                fn=lambda p: self.objective(p, *fit_args, **fit_kwargs),
                space=param_space,
                algo=tpe.suggest,
                max_evals=self.max_evals_per_step,
                trials=trials,
                # rstate=np.random.RandomState(self.random_state)
            )

            step_best_params = space_eval(param_space, best)
            # I added this
            step_best_params = self.clean_int_params(step_best_params)
            # END
            self.best_params_.update(step_best_params)
            self.best_score_ = -min(trials.losses())

            print(f"Best parameters after step {step + 1}: {self.best_params_}")
            print(f"Best score after step {step + 1}: {self.best_score_}")

        # Fit the model with the best parameters
        self.model.set_params(**self.best_params_)
        self.model.fit(X, y, *fit_args, **fit_kwargs)

        return self

    def predict(self, X: pd.DataFrame) -> ArrayLike:
        return self.model.predict(X)

    def score(self, X: pd.DataFrame, y: pd.Series) -> float:
        return self.model.score(X, y)

