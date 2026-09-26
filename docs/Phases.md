# Project Execution Phases & Milestones

**Project:** TV Program Success Predictor
**Document Version:** 1.0

---

## 1. Master Phase Roadmap Overview

| Phase | Description | Deliverable Target | Assigned Lead |
| :--- | :--- | :--- | :--- |
| **Phase 1** | Dataset Preprocessing & EDA | Cleaned CSV + EDA Visuals | Member 1 (Data Lead) |
| **Phase 2** | Regression Pipeline | Regressor `.pkl` + Metrics CSV | Member 2 (ML Lead) |
| **Phase 3** | Classification Pipeline | Classifier `.pkl` + Metrics CSV | Member 3 (WebApp Lead) |
| **Phase 4** | WebApp Development | Full Streamlit Web Application | Member 3 (WebApp Lead) |
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

- [ ] **Task 1.1:** Ingest the Kaggle IMDb Top 5000 dataset into Pandas.
- [ ] **Task 1.2:** Drop redundant text columns (`Synopsis`, `Poster Link`).
- [ ] **Task 1.3:** Extract primary genre from multi-genre strings (e.g., `"Drama, Mystery"` $\rightarrow$ `"Drama"`).
- [ ] **Task 1.4:** Construct EDA visualizations: Rating Distribution, Correlation Heatmaps, Top-Rated Genres.
- [ ] **Task 1.5:** Export `dataset/cleaned_tv_shows.csv`.

**Exit Criteria:** Clean CSV with no nulls in feature columns; EDA notebook committed.

---

### Phase 2: Regression Pipeline Development

**Lead:** Member 2 (ML Lead)

- [ ] **Task 2.1:** Implement feature transformers (`OneHotEncoder` for categorical, `StandardScaler` for numerical).
- [ ] **Task 2.2:** Train 4 regression algorithms:
  1. Linear Regression
  2. K-Nearest Neighbors (KNN) Regressor
  3. Decision Tree Regressor
  4. Random Forest Regressor
- [ ] **Task 2.3:** Calculate MAE, RMSE, and $R^2$ using an 80/20 train/test split.
- [ ] **Task 2.4:** Save the optimal regressor artifact to `models/best_regressor.pkl`.

**Exit Criteria:** `results/regression_metrics.csv` generated; best model meets $R^2 \ge 0.35$, MAE $\le 0.65$.

---

### Phase 3: Classification Pipeline Development

**Lead:** Member 3 (WebApp Lead)

- [ ] **Task 3.1:** Construct target vector $y_{\text{class}}$ using 3-tier categorization:
  - Low: $< 7.0$
  - Moderate: $7.0 \le x < 8.0$
  - High: $\ge 8.0$
- [ ] **Task 3.2:** Train 4 classification algorithms:
  1. Logistic Regression
  2. K-Nearest Neighbors (KNN) Classifier
  3. Decision Tree Classifier
  4. Random Forest Classifier
- [ ] **Task 3.3:** Calculate Accuracy, Precision, Recall, F1-Score, and Confusion Matrix.
- [ ] **Task 3.4:** Save the optimal classifier artifact to `models/best_classifier.pkl`.

**Exit Criteria:** `results/classification_metrics.csv` generated; best model meets Accuracy $\ge 70\%$, F1 $\ge 0.68$.

---

### Phase 4: Streamlit WebApp Development

**Lead:** Member 3 (WebApp Lead)

- [ ] **Task 4.1:** Build `app/app.py` with multi-page navigation layout.
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
