"""Classification Pipeline Module for TV Program Success Predictor.

Trains multiple classification models to predict categorical TV show success tiers (Low, Moderate, High), evaluates classification metrics,
and saves the best model artifact.
"""

from pathlib import Path
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report


def build_preprocessor() -> ColumnTransformer:
    """Creates a ColumnTransformer for feature scaling and encoding."""
    num_features = ['release_year', 'runtime_mins']
    cat_features = ['primary_genre', 'certificate']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_features),
            ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), cat_features)
        ]
    )
    return preprocessor


def train_and_evaluate_classification(dataset_path: str = "dataset/cleaned_tv_shows.csv"):
    """Loads cleaned dataset, trains candidate classifiers, compares macro metrics, and exports the top-performing model artifact."""
    # 1. Load Cleaned Dataset
    df = pd.read_csv(dataset_path)

    # 2. Separate Features and Target (Zero-Leakage Enforcement)
    feature_cols = ['release_year', 'runtime_mins', 'certificate', 'primary_genre']
    X = df[feature_cols]
    y = df['success_category']

    # 3. Train/Test Split (80/20)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    # 4. Define Candidate Classifiers
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
        'Gradient Boosting': GradientBoostingClassifier(random_state=42)
    }

    best_model = None
    best_name = ""
    best_f1 = -1.0
    results = {}

    print("--- Phase 3: Classification Model Evaluation ---")

    # 5. Pipeline Execution and Evaluation Loop
    for name, model in models.items():
        pipeline = Pipeline(steps=[
            ('preprocessor', build_preprocessor()),
            ('classifier', model)
        ])

        pipeline.fit(X_train, y_train)
        preds = pipeline.predict(X_test)

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, average='weighted', zero_division=0)
        rec = recall_score(y_test, preds, average='weighted', zero_division=0)
        f1 = f1_score(y_test, preds, average='weighted', zero_division=0)

        results[name] = {'Accuracy': acc, 'Precision': prec, 'Recall': rec, 'F1-Score': f1}
        print(f"[{name}] Accuracy: {acc:.4f} | Precision: {prec:.4f} | Recall: {rec:.4f} | F1-Score: {f1:.4f}")

        if f1 > best_f1:
            best_f1 = f1
            best_model = pipeline
            best_name = name

    print(f"\nBest Performing Classifier: {best_name} (Weighted F1-Score: {best_f1:.4f})")

    # 6. Save Best Classification Model Artifact
    models_dir = Path("models")
    models_dir.mkdir(parents=True, exist_ok=True)
    model_path = models_dir / "classification_model.pkl"

    joblib.dump(best_model, model_path)
    print(f"Successfully saved best classification pipeline to {model_path}")

    return results


if __name__ == "__main__":
    train_and_evaluate_classification()