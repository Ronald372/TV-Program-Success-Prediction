# Project Execution Phases & Milestones

**Project:** TV Program Success Predictor
**Document Version:** 1.1 (Phases 1–3 Completed)

---

## 1. Master Phase Roadmap Overview

| **Phase 1** | Dataset Preprocessing & EDA | Cleaned CSV + EDA Visuals | Member 1 (Data Lead) — COMPLETED |
| **Phase 2** | Regression Pipeline | Regressor `.pkl` Pipeline | Member 2 (ML Lead) — COMPLETED |
| **Phase 3** | Classification Pipeline | Classifier `.pkl` Pipeline | Member 2 (ML Lead) — COMPLETED |
| **Phase 4** | WebApp Development | Full Streamlit Web Application | Member 3 (WebApp Lead) — IN PROGRESS |
| **Phase 5** | Integration, Testing & Docs | Final Repository + Presentation | All Members |

```text
Phase 1 ──► Phase 2 ──┐
    │                 ├──► Phase 4 ──► Phase 5
    └─────► Phase 3 ──┘
```

---

## 2. Detailed Phase Specifications

### Phase 1: Preprocessing & Exploratory Analytics

**Lead:** Member 1 (Data Lead)

- [x] **Task 1.1:** Ingested raw Kaggle IMDb dataset (3,000 records) into Pandas.
- [x] **Task 1.2:** Cleaned runtime and release year columns; handled nulls.
- [x] **Task 1.3:** Extracted primary genre from multi-genre strings.
- [x] **Task 1.4:** Constructed EDA visualizations in `notebooks/01_data_cleaning_eda.ipynb`.
- [x] **Task 1.5:** Exported `dataset/cleaned_tv_shows.csv`.

**Exit Criteria Status:** PASSED — Cleaned CSV and EDA notebook generated and committed.
---

### Phase 2: Regression Pipeline Development

**Lead:** Member 2 (ML Lead)

- [x] **Task 2.1:** Implemented ColumnTransformer preprocessing pipeline (`StandardScaler` + `OneHotEncoder`).
- [x] **Task 2.2:** Evaluated candidate regression models (Linear Regression, Random Forest, Gradient Boosting).
- [x] **Task 2.3:** Evaluated metrics on 80/20 train/test split (Best: Linear Regression RMSE 0.9216, MAE 0.7097).
- [x] **Task 2.4:** Exported best pipeline artifact to `models/regression_model.pkl`.

**Exit Criteria Status:** PASSED — Saved `models/regression_model.pkl`.

---

### Phase 3: Classification Pipeline Development

**Lead:** Member 3 (WebApp Lead)

- [x] **Task 3.1:** Binned ratings into Low (< 7.0), Moderate (7.0–8.0), and High ($\ge 8.0$) tiers in `src/preprocessing.py`.
- [x] **Task 3.2:** Evaluated candidate classifiers (Logistic Regression, Random Forest, Gradient Boosting).
- [x] **Task 3.3:** Calculated Accuracy, Precision, Recall, and F1-Score (Best: Gradient Boosting Weighted F1 0.3956, Accuracy 45.67%).
- [x] **Task 3.4:** Exported best pipeline artifact to `models/classification_model.pkl`.

**Exit Criteria Status:** PASSED — Saved `models/classification_model.pkl`.

---

### Phase 4: Streamlit WebApp Development

**Lead:** Member 3 (WebApp Lead)

- [ ] **Task 4.1:** Build Streamlit entrypoint `app/main.py` loading `models/regression_model.pkl` and `models/classification_model.pkl`.
- [ ] **Task 4.2:** Implement Single-Show Predictor form connected to `.pkl` artifacts.
- [ ] **Task 4.3:** Build Model Benchmark page rendering saved evaluation CSVs.
- [ ] **Task 4.4:** Build Exploratory Analytics tab displaying Plotly EDA charts.

**Exit Criteria:** All three views render without errors; single prediction completes in $< 200\ \text{ms}$.

---

### Phase 5: Integration, Testing & Documentation

**Lead:** All Members

- [ ] **Task 5.1:** Perform end-to-end integration testing across user input edge cases.
- [ ] **Task 5.2:** Verify zero-leakage compliance (confirm `No_of_Votes` is omitted from feature inputs $X$).
- [ ] **Task 5.3:** Finalize repository documentation and present the project demo.

**Exit Criteria:** README complete, `Memory.md` Section 10 populated with final metrics, demo delivered.
