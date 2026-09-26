# 📺 TV Program Success Predictor

> A dual-stage machine learning system that predicts a TV show's audience reception **before it airs**, using only pre-production metadata from open IMDb data.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Scikit-Learn](https://img.shields.io/badge/scikit--learn-ML-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Phase%204%20In%20Progress-yellow)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📖 Overview

Networks and streaming platforms greenlight shows with little objective feedback on how audiences will receive them. Earlier research relied on proprietary broadcast telemetry, which only works *after* a show airs and often leaks post-release signals into the model.

This project uses **only information available before production** (genre, release year, runtime, certificate, cast) to deliver two predictions:

| Stage | Task | Output |
| :--- | :--- | :--- |
| **1. Regression** | Predict a continuous IMDb rating | e.g. `7.4 / 10` |
| **2. Classification** | Predict a success tier | `Low` · `Moderate` · `High` |

Results are served through an interactive **Streamlit** dashboard.

---

## 🚦 Project Status

| Phase | Description | Status |
| :--- | :--- | :--- |
| **Phase 1** | Dataset Preprocessing & EDA | ✅ Completed |
| **Phase 2** | Regression Pipeline | ✅ Completed |
| **Phase 3** | Classification Pipeline | ✅ Completed |
| **Phase 4** | Streamlit WebApp (`app/main.py`) | 🟡 In Progress |
| **Phase 5** | Integration, Testing & Documentation | ⏳ Pending |

---

## ✨ Features

- 🎯 **Single-Show Predictor** — enter a show concept and get a predicted rating and success tier badge. *(Phase 4)*
- 📊 **Model Benchmarking** — compare regressors on MAE, RMSE, and $R^2$, and classifiers on Accuracy, Precision, Recall, and F1. *(Phase 4)*
- 🔍 **Exploratory Analytics** — interactive Plotly charts for rating distributions, genre performance, and correlations. *(Phase 4)*
- 🛡️ **Zero Data Leakage** — post-release signals such as vote counts are strictly excluded from model inputs.
- 🔁 **Reproducible** — every stochastic step uses `RANDOM_STATE = 42`.
- 🧩 **End-to-end Pipelines** — preprocessing (`StandardScaler` + `OneHotEncoder` via `ColumnTransformer`) is bundled inside each saved Scikit-Learn pipeline, so raw inputs go straight into the model.

---

## 🧠 How It Works

```text
Raw Kaggle CSV ──► Preprocessing ──► Feature Matrix (X, y)
(3,000 shows)          │
                       ├──► Train/Test Split (80/20)
                       ├──► Regression Pipeline ───────► models/regression_model.pkl
                       ├──► Rating Binning + Classifier ► models/classification_model.pkl
                       └──► Streamlit Dashboard (app/main.py)
```

### Input Features vs. Targets

| Role | Columns |
| :--- | :--- |
| ✅ **Input Features ($X$)** | `release_year`, `runtime_mins`, `certificate`, `primary_genre`, `key_cast` |
| 🎯 **Regression Target** | `imdb_rating` |
| 🎯 **Classification Target** | `success_category` |
| ❌ **Excluded (leakage)** | `no_of_votes`, popularity rank, user reviews |

### Success Tiers

| Tier | Rating Range |
| :--- | :--- |
| 🔴 **Low** | $< 7.0$ |
| 🟠 **Moderate** | $7.0 \le x < 8.0$ |
| 🟢 **High** | $\ge 8.0$ |

### Models Evaluated

| Regression | Classification |
| :--- | :--- |
| **Linear Regression** ⭐ (selected) | Logistic Regression |
| Random Forest Regressor | Random Forest Classifier |
| Gradient Boosting Regressor | **Gradient Boosting Classifier** ⭐ (selected) |

---

## 📈 Results

**Dataset:** 3,000 TV shows · **Split:** 80% train / 20% test · **Seed:** 42

### Regression

| Model | MAE ↓ | RMSE ↓ | $R^2$ ↑ |
| :--- | :---: | :---: | :---: |
| **Linear Regression** ⭐ | **0.7097** | **0.9216** | **0.0804** |
| Gradient Boosting | 0.7133 | 0.9226 | 0.0784 |
| Random Forest | 0.8396 | 1.1025 | -0.3161 |

### Classification

| Model | Accuracy ↑ | Weighted F1 ↑ |
| :--- | :---: | :---: |
| **Gradient Boosting** ⭐ | **45.67%** | **0.3956** |
| Logistic Regression | 45.67% | 0.3692 |
| Random Forest | 38.17% | 0.3784 |

> Logistic Regression and Gradient Boosting tie on accuracy; Gradient Boosting was selected for its higher weighted F1.

### Against the Original Targets

| Metric | Target | Achieved | Met? |
| :--- | :---: | :---: | :---: |
| Regression MAE | $\le 0.65$ | 0.7097 | ❌ |
| Regression $R^2$ | $\ge 0.35$ | 0.0804 | ❌ |
| Classification Accuracy | $\ge 70\%$ | 45.67% | ❌ |
| Classification F1 | $\ge 0.68$ | 0.3956 | ❌ |

### 🔎 Key Findings & Limitations

- **Pre-production metadata alone is a weak predictor.** An $R^2$ of about 0.08 means genre, year, runtime, certificate, and cast explain only a small share of rating variance. This is an honest result of the strict no-leakage design: the strongest correlates of rating (votes, popularity) are deliberately excluded.
- **Random Forest overfits.** Its negative $R^2$ on the test set means it performs worse than predicting the mean rating, which points to overfitting on the small, high-cardinality feature space (especially `key_cast`).
- **Simpler models generalize best.** Linear Regression slightly edged out Gradient Boosting, which suggests the available signal is mostly linear and limited.

Ideas to improve these numbers are listed under [Future Scope](#-future-scope).

---

## 📁 Project Structure

```text
TV-Program-Success-Prediction/
│
├── dataset/
│   ├── tv_shows_raw.csv                # Original raw Kaggle CSV (3,000 rows)
│   └── cleaned_tv_shows.csv            # Processed dataset
│
├── notebooks/
│   ├── 01_data_cleaning_eda.ipynb
│   ├── 02_regression_models.ipynb
│   └── 03_classification_models.ipynb
│
├── src/
│   ├── __init__.py
│   ├── preprocessing.py                # Cleaning, genre extraction, rating binning
│   ├── train_regression.py             # Regression training pipeline
│   ├── train_classification.py         # Classification training pipeline
│   └── utils.py                        # Plotting and metric helpers
│
├── models/
│   ├── regression_model.pkl            # Linear Regression pipeline (incl. preprocessing)
│   └── classification_model.pkl        # Gradient Boosting pipeline (incl. preprocessing)
│
├── results/
│   ├── regression_metrics.csv
│   └── classification_metrics.csv
│
├── app/
│   ├── main.py                         # Streamlit entrypoint (Phase 4)
│   ├── views/
│   │   ├── predictor.py
│   │   ├── benchmark.py
│   │   └── analytics.py
│   └── components/
│       └── ui_helpers.py
│
├── PRD.md  ·  Architecture.md  ·  Design.md
├── Memory.md  ·  Phases.md  ·  Rules.md
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python **3.10+**
- `pip` and `git`

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/TV-Program-Success-Prediction.git
cd TV-Program-Success-Prediction
```

### 2. Create a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

<details>
<summary><b>requirements.txt</b></summary>

```text
pandas
numpy
scikit-learn
streamlit
plotly
seaborn
joblib
```

</details>

### 4. Add the dataset

Download the IMDb TV shows dataset from Kaggle and save it as:

```text
dataset/tv_shows_raw.csv
```

### 5. Run the pipeline

```bash
python -m src.preprocessing           # Clean data and bin ratings
python -m src.train_regression        # Train regressors -> models/regression_model.pkl
python -m src.train_classification    # Train classifiers -> models/classification_model.pkl
```

### 6. Launch the app *(Phase 4, in progress)*

```bash
streamlit run app/main.py
```

Then open **http://localhost:8501** in your browser.

---

## 🖥️ Using the Dashboard

In `app/main.py`, show details are entered in the **sidebar**, and results appear in two columns: the predicted rating on the left and the success tier badge on the right.

**Default inputs:** Drama · 45 mins · TV-MA · Release Year 2024

| View | What you can do |
| :--- | :--- |
| **Single-Show Predictor** | Pick a genre, runtime, certificate, and year, and enter cast names to get a predicted rating and success tier. |
| **Model Benchmarks** | Compare models side by side and inspect the confusion matrix. |
| **Exploratory Analytics** | Explore rating distributions, top genres, and feature correlations. |

Models are loaded once at startup:

```python
@st.cache_resource
def load_models():
    regressor = joblib.load("models/regression_model.pkl")
    classifier = joblib.load("models/classification_model.pkl")
    return regressor, classifier
```

---

## 🛠️ Tech Stack

| Layer | Tools |
| :--- | :--- |
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-Learn |
| Visualization | Plotly Express, Seaborn |
| Web App | Streamlit |
| Model Persistence | Joblib |

The stack is 100% free and open source, with no paid APIs.

---

## 👥 Team

| Member | Role | Responsibilities |
| :--- | :--- | :--- |
| **Member 1** | Data Lead | Data cleaning, feature engineering, EDA, analytics dashboard |
| **Member 2** | ML Lead | Regression and classification pipelines, model benchmarking |
| **Member 3** | WebApp Lead | Streamlit app (`app/main.py`), single-show predictor UI |

---

## 📚 Project Documentation

| Document | Contents |
| :--- | :--- |
| [PRD.md](PRD.md) | Requirements, scope, and success criteria |
| [Architecture.md](Architecture.md) | System design, data flow, and components |
| [Design.md](Design.md) | UI/UX tokens, layouts, and states |
| [Phases.md](Phases.md) | Roadmap and task progress |
| [Rules.md](Rules.md) | Coding standards and anti-leakage rules |
| [Memory.md](Memory.md) | Project state log, decisions, and metrics |

---

## 🔮 Future Scope

- **Richer cast and crew features** — replace raw cast text with target-encoded or historical average ratings per actor and director (computed on training data only, to avoid leakage).
- **Class imbalance handling** — use class weights or resampling to lift classifier F1.
- **Hyperparameter tuning** — apply `GridSearchCV` with 5-fold cross-validation, and regularize the Random Forest to curb overfitting.
- **More data** — expand beyond 3,000 shows toward the original 5,000+ target.
- **Batch prediction** via CSV upload.
- **Explainability** — SHAP-based feature drivers in the predictor view.
- **Deployment** to Streamlit Community Cloud.

---

## 📄 Citation

This project is inspired by the methodology of:

> El Fayq et al. (2024). *<Add full paper title, venue, and DOI>*

---

## 📜 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<p align="center">Made with ❤️ as an academic ML project</p>