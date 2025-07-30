"""A calibrator class that routes to other calibrators."""

import json
import os
from typing import Self

import optuna
import pandas as pd

from ..model.model import Model
from ..model_type import ModelType, determine_model_type
from .calibrator import Calibrator
from .mapie_calibrator import MAPIECalibrator
from .vennabers_calibrator import VennabersCalibrator

_CALIBRATOR_ROUTER_FILE = "calibrator_router.json"
_CALIBRATOR_KEY = "calibrator"
_CALIBRATORS = {
    VennabersCalibrator.name(): VennabersCalibrator,
    MAPIECalibrator.name(): MAPIECalibrator,
}


class CalibratorRouter(Calibrator):
    """A router that routes to a different calibrator class."""

    # pylint: disable=too-many-positional-arguments,too-many-arguments

    _calibrator: Calibrator | None

    def __init__(self, model: Model):
        super().__init__(model)
        self._calibrator = None

    @classmethod
    def name(cls) -> str:
        return "router"

    def predictions_as_x(self, y: pd.Series | pd.DataFrame | None = None) -> bool:
        calibrator = self._calibrator
        if calibrator is not None:
            return calibrator.predictions_as_x(None)
        if y is None:
            raise ValueError("y is null")
        if determine_model_type(y) == ModelType.REGRESSION:
            return False
        return True

    def set_options(
        self, trial: optuna.Trial | optuna.trial.FrozenTrial, df: pd.DataFrame
    ) -> None:
        calibrator = self._calibrator
        if calibrator is None:
            return
        calibrator.set_options(trial, df)

    def load(self, folder: str) -> None:
        with open(
            os.path.join(folder, _CALIBRATOR_ROUTER_FILE), encoding="utf8"
        ) as handle:
            params = json.load(handle)
            calibrator = _CALIBRATORS[params[_CALIBRATOR_KEY]](self._model)
        calibrator.load(folder)
        self._calibrator = calibrator

    def save(self, folder: str, trial: optuna.Trial | optuna.trial.FrozenTrial) -> None:
        calibrator = self._calibrator
        if calibrator is None:
            raise ValueError("calibrator is null.")
        calibrator.save(folder, trial)
        with open(
            os.path.join(folder, _CALIBRATOR_ROUTER_FILE), "w", encoding="utf8"
        ) as handle:
            json.dump(
                {
                    _CALIBRATOR_KEY: calibrator.name(),
                },
                handle,
            )

    def fit(
        self,
        df: pd.DataFrame,
        y: pd.Series | pd.DataFrame | None = None,
        w: pd.Series | None = None,
        eval_x: pd.DataFrame | None = None,
        eval_y: pd.Series | pd.DataFrame | None = None,
    ) -> Self:
        # pylint: disable=no-else-return
        calibrator: Calibrator | None = None
        if y is None:
            raise ValueError("y is null")
        if determine_model_type(y) == ModelType.REGRESSION:
            calibrator = MAPIECalibrator(self._model)
        else:
            calibrator = VennabersCalibrator(self._model)
        calibrator.fit(df, y=y, w=w)
        self._calibrator = calibrator
        return self

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        calibrator = self._calibrator
        if calibrator is None:
            raise ValueError("calibrator is null.")
        return calibrator.transform(df)
