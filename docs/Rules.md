# Project Rules & Engineering Standards

**Project:** TV Program Success Predictor
**Document Version:** 1.1 (Phases 1–3 Complete)

---

## 1. General Project Principles

- **Open Source Mandate:** All libraries must be 100% free and open-source. Paid API dependencies or cloud service requirements are prohibited.
- **Reproducibility:** All stochastic processes (data splits, model initializations) must enforce a fixed seed:

  ```python
  RANDOM_STATE = 42
  ```

---

## 2. Code Quality & Software Engineering Rules

- **Modular Design:** Production ML code must reside within `src/` modules as reusable functions. Do **not** write inline pipeline execution inside Jupyter cells.
- **Type Hinting:** All functions in `src/` modules must include Python type hints and docstrings.

```python
def predict_rating(features: dict) -> float:
    """Executes single show continuous rating prediction.

    Args:
        features (dict): Pre-processed input feature dictionary.

    Returns:
        float: Predicted IMDb Rating (1.0 to 10.0).
    """
```

---

## 3. Data Integrity & Zero-Hallucination Policy

> ⚠️ **STRICT ANTI-LEAKAGE RULE**
> Under no circumstances should target-adjacent features be included in the input feature matrix $X$.

| Status | Features |
| :--- | :--- |
| ❌ **Forbidden in $X$** | `no_of_votes` / `Votes`, `Popularity_Rank`, `User_Reviews`, `imdb_rating` |
| ✅ **Allowed in $X$** | `release_year`, `runtime_mins`, `certificate`, `primary_genre`, `key_cast` |

---

## 4. Business Analytics & Formulation Rules

Target classes must adhere strictly to these cutoffs:

| Class | Rule |
| :--- | :--- |
| **Low Success** | $\text{Rating} < 7.0$ |
| **Moderate Success** | $7.0 \le \text{Rating} < 8.0$ |
| **High Success** | $\text{Rating} \ge 8.0$ |

Reference implementation:

```python
def bin_rating(rating: float) -> str:
    """Maps a continuous IMDb rating to a success category."""
    if rating < 7.0:
        return "Low"
    if rating < 8.0:
        return "Moderate"
    return "High"
```

---

## 5. Dashboard & UI Design Rules

- UI components must enforce cinematic dark mode tokens:
  - Background: `#0E1117`
  - Card surface: `#1E222A`
- Real-time models must be pre-loaded into Streamlit memory using `@st.cache_resource` on application startup.
- **Never** fit models inside page load routines.

```python
@st.cache_resource
def load_models():
    regressor = joblib.load("models/regression_model.pkl")
    classifier = joblib.load("models/classification_model.pkl")
    return regressor, classifier
```

---

## 6. AI Assistant & Coding Agent Operational Rules

1. Agents must check `Memory.md` for context before editing codebase logic.
2. Agents must update `Memory.md` progress logs after creating new pipeline files or structural components.
3. Do not introduce alternative framework dependencies (such as PyTorch or TensorFlow) unless explicitly requested.

---

## 7. Security & Compliance

- Ensure no proprietary API credentials or local absolute file paths are hardcoded in public repository files.
- Ensure all dataset sources adhere to their public usage terms.
