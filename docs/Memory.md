# Persistent Project Memory & State Log

> **Agent Rule:** Read this file before editing any codebase logic. Update Section 5 after creating new pipeline files or structural components.

---

## 1. Project Status Summary

| Field | Value |
| :--- | :--- |
| **Project Name** | TV Program Success Predictor |
| **Target Completion** | Academic Submission Cycle 2026 |
| **Current Status** | Initialization & Architecture Setup Phase |
| **Core Objective** | Develop a dual-stage ML system predicting television program success using pre-production metadata on open IMDb data. |

---

## 2. Approved Technology Stack

| Layer | Selected Tool | License | Justification |
| :--- | :--- | :--- | :--- |
| **Language** | Python 3.10+ | PSF | Standard ML ecosystem compatibility |
| **Data Processing** | Pandas, NumPy | BSD | High-performance array and frame manipulation |
| **Machine Learning** | Scikit-Learn | BSD | Standard suite of regression and classification models |
| **Visualization** | Plotly Express, Seaborn | MIT / BSD | Interactive charting directly supported by Streamlit |
| **Web Framework** | Streamlit | Apache 2.0 | Pure Python web interface deployment |

---

## 3. Dataset Schemas & Relationships

- **Primary Entity:** `dataset/cleaned_tv_shows.csv`
- **Input Features ($X$):** `release_year`, `runtime_mins`, `certificate`, `primary_genre`, `key_cast`
- **Targets:** `imdb_rating` (regression), `success_category` (classification)
- **Excluded:** `no_of_votes` (leakage)

---

## 4. Documented Mathematical & Analytical Formulas

### 4.1 Regression Metrics

**Mean Absolute Error (MAE):**

$$
\text{MAE} = \frac{1}{n} \sum_{i=1}^{n} \left| y_i - \hat{y}_i \right|
$$

**Root Mean Squared Error (RMSE):**

$$
\text{RMSE} = \sqrt{\frac{1}{n} \sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2}
$$

**Coefficient of Determination ($R^2$):**

$$
R^2 = 1 - \frac{\sum_{i=1}^{n} \left( y_i - \hat{y}_i \right)^2}{\sum_{i=1}^{n} \left( y_i - \bar{y} \right)^2}
$$

### 4.2 Classification Metrics

$$
\text{Precision} = \frac{TP}{TP + FP} \qquad
\text{Recall} = \frac{TP}{TP + FN} \qquad
F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}
$$

### 4.3 Target Classification Binning

$$
\text{Category} =
\begin{cases}
\text{Low Success}, & \text{if } \text{Rating} < 7.0 \\
\text{Moderate Success}, & \text{if } 7.0 \le \text{Rating} < 8.0 \\
\text{High Success}, & \text{if } \text{Rating} \ge 8.0
\end{cases}
$$

---

## 5. Project Phase Progress Log

- [x] Initialized project repository structure.
- [x] Drafted core requirements documents (PRD, Architecture, Design, Memory, Rules, Phases).
- [ ] **In Progress:** Member 1 executing dataset cleaning and EDA.
- [ ] **Pending:** Member 2 regression model training.
- [ ] **Pending:** Member 3 classification model training & Streamlit UI construction.

---

## 6. Team Responsibility Matrix

| Task | Member 1 (Data) | Member 2 (ML) | Member 3 (WebApp) |
| :--- | :---: | :---: | :---: |
| Data Cleaning & Preprocessing | **LEAD** | Support | Support |
| EDA & Analytics Dashboard | **LEAD** | Review | Support |
| Regression Pipeline & Benchmarks | Support | **LEAD** | Support |
| Classification Pipeline & Models | Support | Support | **LEAD** |
| Streamlit App & Single Predictor UI | Support | Support | **LEAD** |

---

## 7. Architectural Decisions Log (ADR)

| ID | Decision | Rationale |
| :--- | :--- | :--- |
| **ADR-01** | Rejected live API scraping in favor of the Kaggle IMDb dataset. | Execution stability and speed. |
| **ADR-02** | Selected Random Forest as the primary baseline architecture. | Empirical findings in El Fayq et al. (2024). |
| **ADR-03** | Strictly excluded `No_of_Votes` from input features $X$. | Eliminates post-broadcast data leakage. |

---

## 8. Assumptions Log

- Public IMDb ratings provide a reliable proxy for general media success and viewer reception.
- User system environments support standard HTML5 canvas and a Python 3.10 runtime.

---

## 9. Important File Locations

| Asset | Path |
| :--- | :--- |
| Raw Dataset | `dataset/tv_shows_raw.csv` |
| Processed Data | `dataset/cleaned_tv_shows.csv` |
| Trained Models | `models/best_regressor.pkl`, `models/best_classifier.pkl` |
| Preprocessing Transformers | `models/encoder_scaler.pkl` |
| Metrics | `results/regression_metrics.csv`, `results/classification_metrics.csv` |
| Application Entrypoint | `app/app.py` |

---

## 10. Empirical Verification & Performance Metrics

> *To be populated after the model training phase completes.*

| Model | Task | MAE | RMSE | $R^2$ | Accuracy | F1 |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| — | — | — | — | — | — | — |

---

## 11. Immediate Next Steps

1. Download the Kaggle IMDb Top 5000 TV Shows CSV into `dataset/tv_shows_raw.csv`.
2. Execute `notebooks/01_data_cleaning_eda.ipynb` to clean raw features.
