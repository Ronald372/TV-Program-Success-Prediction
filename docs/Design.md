# UI/UX & Dashboard Design System

**Project:** TV Program Success Predictor
**Document Version:** 1.0

---

## 1. Design Philosophy & Academic Context

The interface uses a **dark cinematic theme** inspired by modern media platforms. It balances:

- **Intuitive visual badges** for non-technical stakeholders, and
- **Rigorous analytical benchmark displays** for academic evaluation.

---

## 2. Visual Token System & Palette

| Token Name | Hex Code | Usage |
| :--- | :--- | :--- |
| **Primary Background** | `#0E1117` | App background |
| **Card Surface** | `#1E222A` | Elevated panels, containers |
| **Primary Accent** | `#E50914` | Streaming red, action buttons |
| **Success – High** | `#00CC96` | Badge for ratings $\ge 8.0$ |
| **Success – Moderate** | `#FFAA00` | Badge for ratings 7.0 – < 8.0 |
| **Success – Low** | `#FF4B4B` | Badge for ratings < 7.0 |
| **Text Primary** | `#FAFAFA` | Main body headers and titles |
| **Text Muted** | `#A0AAB2` | Subtitles and metadata labels |

### 2.1 Streamlit Theme Configuration

`.streamlit/config.toml`:

```toml
[theme]
base = "dark"
primaryColor = "#E50914"
backgroundColor = "#0E1117"
secondaryBackgroundColor = "#1E222A"
textColor = "#FAFAFA"
```

---

## 3. Layout Structure & Navigation

| Region | Contents |
| :--- | :--- |
| **Top Header** | Display title (*TV Program Success Predictor*), subtitle, and repository links. |
| **Sidebar Navigation** | Radio selector between *Single-Show Predictor*, *Model Benchmarks*, and *Exploratory Analytics*. |
| **Main Container** | Responsive multi-column grid (`st.columns`) hosting interactive inputs and dynamic metrics. |

---

## 4. Component Design Specifications

| Component | Specification |
| :--- | :--- |
| **Metric Card Container** | Background `#1E222A`, border radius `8px`, padding `16px`. |
| **Prediction Badges** | High-contrast text badges: green `#00CC96`, amber `#FFAA00`, red `#FF4B4B`. |
| **Form Inputs** | Clearly labeled controls with default pre-filled values. |

### 4.1 Reference CSS

```css
.metric-card {
    background-color: #1E222A;
    border-radius: 8px;
    padding: 16px;
    color: #FAFAFA;
}

.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 8px;
    font-weight: 700;
    color: #0E1117;
}

.badge-high     { background-color: #00CC96; }
.badge-moderate { background-color: #FFAA00; }
.badge-low      { background-color: #FF4B4B; }
```

---

## 5. Main Dashboard Tabs & Visual Hierarchies

### 5.1 Predictor Tab Hierarchy

```text
[ Input Form Column (Left 40%) ]   │   [ Prediction Results Column (Right 60%) ]
- Title Text                       │   - Expected Rating Card (Big Number: e.g. 8.1)
- Genre Dropdown                   │   - Success Category Badge (HIGH SUCCESS)
- Runtime Slider                   │   - Model Confidence Indicator
- Certificate Selector             │   - Key Driving Feature Breakdown Plot
```

Implementation hint:

```python
left, right = st.columns([2, 3])  # 40% / 60%
```

### 5.2 Benchmark Tab Hierarchy

```text
[ Model Metric Comparison Table ]
- Model Name | MAE | RMSE | R2 / Accuracy | Precision | Recall | F1-Score
-----------------------------------------------------------------------
[ Plotly Bar Chart: R2 / Accuracy Scores across Models ]
[ Plotly Confusion Matrix Heatmap (Best Classifier) ]
```

---

## 6. System States & UX Edge Cases

| State | Behavior |
| :--- | :--- |
| **Initial State** | Form fields pre-populated with standard defaults: *Drama*, *45 mins*, *TV-14*, *Release Year 2026*. |
| **Processing State** | Spinner displayed during execution: `st.spinner("Executing Prediction Pipeline...")` |
| **Error State** | Inline warning for incomplete input: `st.warning("Please complete all required fields.")` |
