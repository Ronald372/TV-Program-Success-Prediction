# System Architecture Document

**Project:** TV Program Success Predictor
**Document Version:** 1.0

---

## 1. High-Level Architecture Overview

```text
                                 [ USER / BROWSER ]
                                         │
                                         ▼
                             ┌───────────────────────┐
                             │ Streamlit Web App UI  │
                             └───────────┬───────────┘
                                         │
                 ┌───────────────────────┼───────────────────────┐
                 ▼                       ▼                       ▼
      ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
      │  Single-Show View   │ │  Benchmark View     │ │   Analytics View    │
      └──────────┬──────────┘ └──────────┬──────────┘ └──────────┬──────────┘
                 │                       │                       │
                 ▼                       ▼                       ▼
      ┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
      │   Inference Engine  │ │  Metrics Cache      │ │  Plotly Visuals     │
      └──────────┬──────────┘ └──────────┬──────────┘ └──────────┬──────────┘
                 │                       │                       │
                 └───────────────────────┼───────────────────────┘
                                         │
                                         ▼
                             ┌───────────────────────┐
                             │ Pre-Trained Artifacts │
                             │ (.pkl models/scalers) │
                             └───────────────────────┘
```

---

## 2. End-to-End Data Flow

```text
Raw Kaggle CSV ---> Data Preprocessing ---> Feature Matrix (X, y)
                        │
                        ├───► Train/Test Split (80/20)
                        │
                        ├───► Regression Training ────► best_regressor.pkl
                        │
                        ├───► Class Target Binning ───► best_classifier.pkl
                        │
                        └───► Saved Metrics CSVs ─────► Streamlit App Render
```

---

## 3. Component Architecture

| Component | File Path | Responsibilities | Input Artifacts | Output Artifacts |
| :--- | :--- | :--- | :--- | :--- |
| **Data Cleaner** | `src/preprocessing.py` | Imputation, scaling, categorical encoding, and feature filtering. | `dataset/tv_shows_raw.csv` | `dataset/cleaned_tv_shows.csv`, `models/encoder_scaler.pkl` |
| **Regression Trainer** | `src/train_regression.py` | Fits 4 regression algorithms; computes MAE, RMSE, $R^2$. | `dataset/cleaned_tv_shows.csv` | `models/best_regressor.pkl`, `results/regression_metrics.csv` |
| **Classifier Trainer** | `src/train_classification.py` | Bins ratings into 3 classes; fits 4 classification algorithms. | `dataset/cleaned_tv_shows.csv` | `models/best_classifier.pkl`, `results/classification_metrics.csv` |
| **Web Application** | `app/app.py` | Interactive dashboard layout and real-time inference execution. | `.pkl` models, metrics CSVs | User Interface |

---

## 4. Dataset Relational Model

```text
+--------------------------------------------------------+
|                   CLEANED_TV_SHOWS                     |
+-------------------+--------------+---------------------+
| Column            | Type         | Constraint          |
+-------------------+--------------+---------------------+
| show_id (PK)      | String/UUID  | NOT NULL, UNIQUE    |
| title             | String       | NOT NULL            |
| release_year      | Integer      | 1950 <= x <= 2026   |
| runtime_mins      | Float        | > 0                 |
| certificate       | String       | Categorical         |
| primary_genre     | String       | Categorical         |
| key_cast          | String       | Nullable            |
| imdb_rating       | Float        | 1.0 <= x <= 10.0    |
| success_category  | String       | Low/Moderate/High   |
+-------------------+--------------+---------------------+
```

---

## 5. Dashboard Architecture (Streamlit + Plotly)

| Concern | Mechanism | Purpose |
| :--- | :--- | :--- |
| **State Management** | `st.session_state` | Stores user input parameters across tab switches. |
| **Resource Caching** | `@st.cache_resource` | Loads serialized ML models (`.pkl`) into memory once on startup. |
| **Data Caching** | `@st.cache_data` | Caches processed dataframes and metrics tables for fast UI rendering. |

---

## 6. Comprehensive Directory Structure

```text
TV-Program-Success-Prediction/
│
├── dataset/
│   ├── tv_shows_raw.csv                # Original raw Kaggle CSV
│   └── cleaned_tv_shows.csv            # Processed dataset
│
├── notebooks/
│   ├── 01_data_cleaning_eda.ipynb      # Member 1
│   ├── 02_regression_models.ipynb      # Member 2
│   └── 03_classification_models.ipynb  # Member 3
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py                # Scaling and encoding logic
│   ├── train_regression.py             # Regression model training pipeline
│   ├── train_classification.py         # Classification model training pipeline
│   └── utils.py                        # Plotting helpers and metrics calculators
│
├── models/
│   ├── best_regressor.pkl              # Saved best regressor (baseline: Random Forest)
│   ├── best_classifier.pkl             # Saved best classifier (baseline: Random Forest)
│   └── encoder_scaler.pkl              # Saved preprocessing transformers
│
├── results/
│   ├── regression_metrics.csv          # Benchmarking results for regressor models
│   └── classification_metrics.csv      # Benchmarking results for classifier models
│
├── app/
│   ├── app.py                          # Streamlit application entrypoint
│   ├── views/
│   │   ├── predictor.py                # Single-Show Predictor View
│   │   ├── benchmark.py                # Model Benchmark View
│   │   └── analytics.py                # Exploratory Data Analytics View
│   └── components/
│       └── ui_helpers.py               # Custom CSS cards and visual badges
│
├── .gitignore
├── PRD.md
├── Architecture.md
├── Rules.md
├── Phases.md
├── Design.md
├── Memory.md
├── requirements.txt
└── README.md
```

---

## 7. Technology Stack & Justification

| Technology | Role | Justification |
| :--- | :--- | :--- |
| **Python 3.10+** | Core language | Standard ML ecosystem compatibility. |
| **Pandas & NumPy** | Data processing | Data cleaning, manipulation, and vectorized array calculations. |
| **Scikit-Learn** | Machine learning | Pipelines, model training, and metrics calculation. |
| **Streamlit** | Web framework | Lightweight ML dashboard deployment without JavaScript overhead. |
| **Plotly Express** | Visualization | Interactive plotting natively integrated with Streamlit. |

---

## 8. Data Lifecycle Management

1. **Ingestion** — Raw CSV loaded into a Pandas DataFrame.
2. **Sanitization** — String normalization, null imputation, duplicate removal.
3. **Transformation** — One-Hot Encoding for categorical features; `StandardScaler` for continuous variables.
4. **Persistence** — Models exported as compressed `.pkl` files using `joblib`.

---

## 9. Error Handling & Data Quality Strategy

| Scenario | Strategy |
| :--- | :--- |
| **Null Value Fallbacks** | Numerical nulls imputed with median values; categorical nulls imputed with `"Unknown"`. |
| **User Input Bounds** | Streamlit forms enforce upper/lower bounds on numeric inputs (e.g., Runtime constrained to 5–300 minutes). |
| **Out-of-Vocabulary Encodings** | `OneHotEncoder(handle_unknown='ignore')` safely handles unseen categorical inputs. |

---

## 10. Scalability & Performance Optimization

- Model files optimized using Joblib compression:

  ```python
  joblib.dump(model, "models/best_regressor.pkl", compress=3)
  ```

- Heavy compute processes (EDA plots, model loading) are cached via Streamlit decorators to guarantee response latency under **200 ms**.
