"""Regression Pipeline Module for TV Program Success Predictor.

Trains multiple regression models to predict continuous IMDb ratings using pre-production features, evaluates performance metrics, and saves the best model.
"""

from pathlib import Path
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score


def build_preprocessor() -> ColumnTransformer:
    """Creates a ColumnTransformer to handle numerical scaling and categorical encoding."""
    num_features = ['release_year', 'runtime_mins']
    cat_features = ['primary_genre', 'certificate']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ]
    )
    return preprocessor


def train_and_evaluate_regression(dataset_path: str = "dataset/cleaned_tv_shows.csv"):
    """Loads cleaned data, trains regression algorithms, compares metrics, and exports the top-performing model artifact."""
    # 1. Load Cleaned Dataset
    df = pd.read_csv(dataset_path)

    # 2. Separate Features and Target (Zero-Leakage Enforcement)
    feature_cols = ['release_year', 'runtime_mins', 'certificate', 'primary_genre']
    X = df[feature_cols]
    y = df['imdb_rating']

    # 3. Train/Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # 4. Define Candidate Models
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingRegressor(random_state=42)
    }

    best_model = None
    best_name = ""
    best_rmse = float('inf')
    results = {}

    print("--- Phase 2: Regression Model Evaluation ---")

    # 5. Pipeline Execution and Evaluation Loop
    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', build_preprocessor()),
            ('regressor', model)
        ])

        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)

        mse = mean_squared_error(y_test, preds)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, preds)
        r2 = r2_score(y_test, preds)

        results[name] = {'RMSE': rmse, 'MAE': mae, 'R2': r2}
        print(f"[{name}] RMSE: {rmse:.4f} | MAE: {mae:.4f} | R2 Score: {r2:.4f}")

        if rmse < best_rmse:
            best_rmse = rmse
            best_model = pipeline
            best_name = name

    print(f"\nBest Performing Model: {best_name} (RMSE: {best_rmse:.4f})")

    # 6. Save Best Model Artifact
    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "regression_model.pkl"
    
    joblib.dump(best_model, model_path)
    print(f"Successfully saved best model pipeline to {model_path}")

    return results


if __name__ == "__main__":
    train_and_evaluate_regression()