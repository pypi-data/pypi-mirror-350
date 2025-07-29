import yaml
import pandas as pd
import numpy as np
from typing import List, Dict, Union
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score


class ModelMakerHelper:
    """
    Train & tune a RandomForestClassifier, then produce
    multiple KPI flags from predicted probabilities.
    """

    def __init__(self, random_state: int = 42, base_params: Dict = None):
        self.random_state = random_state
        self.base_params = base_params or {
            "n_estimators": 100,
            "random_state": random_state,
            "oob_score": True
        }
        self.model = RandomForestClassifier(**self.base_params)
        self.fitted = False

        # to be loaded
        self.feature_cols: List[str] = []
        self.target_col: str = ""
        self.test_size: float = 0.2
        self.tune_params: Dict = {}
        self.kpis: List[Dict[str, Union[str, float]]] = []

    def load_config(self, path: str):
        """Load features, target, split, tune grid, and KPI list from YAML."""
        with open(path, "r") as f:
            cfg = yaml.safe_load(f)

        self.feature_cols = cfg["feature_cols"]
        self.target_col   = cfg["target_col"]
        self.test_size    = cfg.get("test_size", 0.2)
        self.tune_params  = cfg.get("tune_params", {})
        self.kpis         = cfg.get("kpis", [])

    def train(
        self,
        df: pd.DataFrame,
        cv: int = 3,
        **fit_kwargs
    ) -> Dict:
        """Train (and optionally tune) the classifier, return metrics."""
        X = df[self.feature_cols].values
        y = df[self.target_col].values

        X_tr, X_te, y_tr, y_te = train_test_split(
            X, y,
            test_size=self.test_size,
            random_state=self.random_state
        )

        # hyperparam tuning if provided
        best_params = {}
        if self.tune_params:
            grid = GridSearchCV(
                estimator=self.model,
                param_grid=self.tune_params,
                cv=cv,
                scoring="accuracy",
                n_jobs=-1
            )
            grid.fit(X_tr, y_tr)
            self.model = grid.best_estimator_
            best_params = grid.best_params_
        else:
            self.model.fit(X_tr, y_tr, **fit_kwargs)

        # evaluate
        y_pred = self.model.predict(X_te)
        acc    = accuracy_score(y_te, y_pred)
        oob    = getattr(self.model, "oob_score_", None)

        self.fitted = True
        return {"accuracy": acc, "oob_score": oob, "best_params": best_params}

    def predict_with_kpis(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Predict class probabilities and generate multiple KPI flags
        as defined in config.
        """
        if not self.fitted:
            raise RuntimeError("Call train() before predict_with_kpis()")

        X_new = df[self.feature_cols].values
        probs = self.model.predict_proba(X_new)[:, 1]  # probability of class '1'

        out = df.copy().reset_index(drop=True)
        out[f"prob_{self.target_col}"] = probs

        # for each KPI definition, add a boolean column
        for kpi in self.kpis:
            name      = kpi["name"]
            threshold = kpi["threshold"]
            out[name] = probs >= threshold

        return out
