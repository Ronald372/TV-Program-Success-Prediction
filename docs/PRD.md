# Product Requirements Document (PRD)

**Project:** TV Program Success Predictor
**Document Version:** 1.1
**Status:** Phases 1–3 Complete (Phase 4 Active)

---

## 1. Executive Summary & Overview

The **TV Program Success Predictor** is an interactive, dual-stage Machine Learning system designed to evaluate pre-production television show metadata (Genre, Release Year, Runtime, Certificate, Cast/Crew) to predict audience reception prior to broadcast scheduling.

Inspired by the foundational methodology of El Fayq et al. (2024)[^1], this project adapts proprietary broadcast telemetry modeling into an open, reproducible framework that serves:

- **Continuous rating predictions** (regression), and
- **Discrete greenlighting decision tiers** (classification)

via a Streamlit web application.

---

## 2. Problem Statement & Motivation

Television networks and streaming services commit massive capital to content development without early-stage, objective feedback on audience reception. Prior academic research relies heavily on real-time, proprietary broadcast telemetry (such as live audience measurement boxes)[^1]. These approaches present three core failures:

1. **Inability to Predict Pre-Production Success** — Telemetry models require the show to already be scheduled and aired[^1].
2. **Target Data Leakage** — Models often use post-airing engagement metrics as input features, resulting in artificially inflated evaluation scores[^1].
3. **Reproducibility Barriers** — Access to localized, closed-source measurement datasets limits practical academic and industrial usage[^1].

> **Our Solution:** Enforce strict pre-production feature isolation on open IMDb metadata to deliver non-leaky continuous score regressions and decision-tier classifications.

---

## 3. Target Users & Stakeholders

| User Role | Needs & Objectives | Interaction with System |
| :--- | :--- | :--- |
| **Network Executives & Content Producers** | Objective greenlighting indicators to evaluate scripts, cast lists, and runtimes before budgeting. | Inputs proposed metadata into the single-show predictor to analyze predicted score and risk level. |
| **Acquisitions & Program Schedulers** | Data-backed estimation of audience appeal for purchasing global distribution rights. | Filters top-performing genres and runtimes in the analytics dashboard to identify high-value traits. |
| **Academic Evaluators / Professors** | Rigorous ML pipeline proof, reproducible metrics, multi-model comparisons, and zero data leakage. | Reviews the benchmark dashboard to inspect model metrics ($R^2$, MAE, Confusion Matrix) and repository structure. |

---

## 4. Scope & Boundaries

### 4.1 In-Scope

- Dual-target prediction pipeline:
  - Continuous IMDb rating estimation ($1.0 - 10.0$)
  - 3-class categorical success prediction (Low, Moderate, High)
- Pre-production feature isolation (Genre, Release Year, Runtime, Content Certificate, Cast, Director).
- Interactive Streamlit web interface containing single-show predictions, model benchmarking, and exploratory data analytics.
- Comparative evaluation of **8 ML algorithms** (4 Regressors, 4 Classifiers).

### 4.2 Out-of-Scope

- Real-time social media sentiment tracking (Twitter/X, Reddit scraping).
- Live broadcast telemetry box integration (Moroccan CIAUMED / Médiamétrie hardware signals)[^1].
- Deep learning computer vision analysis on video trailers or poster art.

---

## 5. Functional Requirements (FR)

| Req. ID | Module | Priority | Description |
| :--- | :--- | :--- | :--- |
| **FR-01** | Data Pipeline | **COMPLETED** | Cleaned raw IMDb dataset (3,000 rows), extracted primary genres/years, and built zero-leakage `src/preprocessing.py`. |
| **FR-02** | Regression ML | **COMPLETED** | Trained and evaluated Linear Regression, Random Forest, and Gradient Boosting in `src/train_regression.py`. Best: Linear Regression ($\text{RMSE} = 0.9216$). |
| **FR-03** | Classification ML | **COMPLETED** | Categorized into Low, Moderate, High tiers and evaluated Logistic Regression, Random Forest, and Gradient Boosting in `src/train_classification.py`. Best: Gradient Boosting ($\text{F1} = 0.3956$). |
| **FR-04** | Inference Engine | **MUST-HAVE (M)** | Load pre-trained `.pkl` artifacts and execute dual-target inference in under 200 ms. |
| **FR-05** | Predictor UI | **MUST-HAVE (M)** | Interactive form with sliders, dropdowns, and text fields yielding real-time score badges and risk indicators. |
| **FR-06** | Benchmark UI | **MUST-HAVE (M)** | Dynamic performance tables ($R^2$, MAE, RMSE, Accuracy, F1) with toggleable plots and confusion matrices. |
| **FR-07** | Analytics UI | **MUST-HAVE (M)** | Interactive Plotly charts covering rating distributions, genre performance, and correlation heatmaps. |
| **FR-08** | Batch Prediction | **OPTIONAL (O)** | Allow users to upload a CSV file of multiple show concepts for bulk success score generation. |

---

## 6. Non-Functional Requirements (NFR)

| NFR ID | Attribute | Requirement |
| :--- | :--- | :--- |
| **NFR-01** | Latency | Single-show prediction runtime must be $< 200\ \text{ms}$. |
| **NFR-02** | Usability | UI must render cleanly at $1280 \times 720$ and higher, using a dark theme. |
| **NFR-03** | Reproducibility | Pipelines must execute deterministically using a fixed global seed (`RANDOM_STATE = 42`). |
| **NFR-04** | Memory Footprint | Application RAM usage must remain under $512\ \text{MB}$ on free cloud hosting tiers. |

---

## 7. Dataset Specifications

### 7.1 Entity Schema

```text
+------------------------------------------------------------------------+
|                              IMDb TV SHOWS                             |
+-------------------+--------------+-------------------------------------+
| Field Name        | Data Type    | Pipeline Role                       |
+-------------------+--------------+-------------------------------------+
| Title             | String       | Display Identifier                  |
| Release_Year      | Integer      | Input Feature (X)                   |
| Runtime_Mins      | Float        | Input Feature (X)                   |
| Certificate       | Categorical  | Input Feature (X)                   |
| Primary_Genre     | Categorical  | Input Feature (X)                   |
| Key_Cast          | Text String  | Input Feature (X)                   |
| IMDb_Rating       | Continuous   | Regression Target (y_reg)           |
| Success_Category  | Categorical  | Classification Target (y_class)     |
| No_of_Votes       | Integer      | EXCLUDED (Prevents Leakage)         |
+-------------------+--------------+-------------------------------------+
```

### 7.2 Scalability & Validation Benchmarks

| Parameter | Target |
| :--- | :--- |
| **Dataset Size** | 3,000 unique TV show records (`tv_shows_raw.csv`) |
| **Cross-Validation** | 5-Fold Cross Validation across all candidate models during training |
| **Split Ratio** | $80\%$ Training Set / $20\%$ Holdout Test Set |

---

## 8. Dashboard Requirements & Layout

The application interface is partitioned into three main views.

### 8.1 Tab 1 — Single Show Predictor

- **Left Panel (Input Form):** Sliders for Year and Runtime, dropdowns for Genre and Certificate, text fields for Cast/Crew.
- **Right Panel (Results Display):** Metric cards displaying:
  - Expected Rating (e.g., `8.2 / 10`)
  - Success Category Badge (e.g., `HIGH SUCCESS`)
  - Model Confidence Score

### 8.2 Tab 2 — Model Benchmarking

- Split toggle between **Regression** ($R^2$, MAE, RMSE) and **Classification** (Accuracy, Precision, Recall, F1).
- Interactive bar chart displaying $R^2$ / Accuracy scores across all models.
- Plotly Confusion Matrix heatmap.

### 8.3 Tab 3 — Exploratory Data Analytics

- Interactive distribution plots.
- Genre rank charts.
- Feature correlation heatmaps.

---

## 9. Team Structure & Work Division

```text
+-------------------------------------------------------------------------+
|                           TEAM WORK DIVISION                            |
+-------------------+-----------------------------------------------------+
| Member            | Core Technical Responsibilities                     |
+-------------------+-----------------------------------------------------+
| Member 1          | Data Cleaning, Preprocessing, Feature Engineering,  |
| (Data Lead)       | Notebook 01, Exploratory Data Analytics Dashboard.  |
+-------------------+-----------------------------------------------------+
| Member 2          | Regression Pipeline, Hyperparameter Tuning,         |
| (ML Lead)         | Model Benchmark Dashboard, Notebook 02.             |
+-------------------+-----------------------------------------------------+
| Member 3          | Classification Pipeline, Single-Show Predictor UI,  |
| (WebApp Lead)     | Streamlit Application Setup, Notebook 03.           |
+-------------------+-----------------------------------------------------+
```

---

## 10. Constraints & Open-Source Compliance

- **100% Free / Open-Source Stack:** Python, Pandas, NumPy, Scikit-Learn, Streamlit, Plotly.
- **No paid API dependencies** (e.g., OpenAI API, paid cloud databases).
- **Permissive licenses only:** All dependencies must use permissive OSI-approved licenses (MIT, BSD, Apache 2.0, PSF).

---

## 11. Success Criteria & Evaluation Rubric

| Target | Metric | Initial Target | Phase 2–3 Baseline Empirical Result |
| :--- | :--- | :--- | :--- |
| **Regression** | RMSE (Linear Regression) | — | **0.9216** |
| **Regression** | MAE (Linear Regression) | $\le 0.65$ | **0.7097** |
| **Regression** | $R^2$ (Linear Regression) | $\ge 0.35$ | **0.0804** |
| **Classification** | Accuracy (Gradient Boosting) | $\ge 70\%$ | **45.67%** |
| **Classification** | F1-Score (Gradient Boosting) | $\ge 0.68$ | **0.3956** |
| **System** | Web App stability | Executes smoothly | *In Progress (Phase 4)* |

---

## References

[^1]: El Fayq et al. (2024) — foundational study on TV program success prediction using broadcast audience telemetry. Add the full citation (title, venue, DOI) here.
