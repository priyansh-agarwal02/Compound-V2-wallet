# Compound-V2-wallet
Zeru Finance Credit Score Predictor

# Compound V2 Wallet Credit Scoring: Methodology & Results

---


### Overview
Zeru Finance aims to build an AI-powered, decentralized credit scoring system for Compound V2 wallets. The goal is to assign a credit score (0–100) to each wallet based solely on historical transaction behavior, reflecting reliability and risk.

### Data Processing Pipeline
- **Load & Parse:** Raw JSON transaction data is loaded and normalized into a single DataFrame.
- **Feature Engineering:** Wallet-level features are computed, including activity, volume, diversity, and behavioral metrics.
- **Scoring:** Two approaches are used:
  - **A. Clustering-Based (Unsupervised)**
  - **B. Explicit Weighted-Score (Rule-Based)**

---

### A. Clustering-Based Approach
- **Feature Extraction:**
  - Total transactions, total/average/std transaction amount (USD), wallet age, asset diversity, transactions per day.
- **Scaling & Dimensionality Reduction:**
  - Features are normalized (MinMaxScaler) and reduced (PCA) for clustering.
- **Clustering:**
  - KMeans groups wallets by behavioral similarity (optimal clusters via silhouette score).
- **Scoring:**
  - Each cluster is ranked by composite behavioral quality. Clusters are mapped to score bands (0–100).
  - A small feature-based adjustment is added for granularity.
- **Wallet Quality Band:**
  - Clusters are labeled as "Good" or "Bad" based on whether their median activity, age, and diversity exceed global medians.

#### Rationale
- Unsupervised clustering reveals natural groupings and outliers, supporting protocol health and explainability.

---

### B. Explicit Weighted-Score Approach
- **Feature Extraction:**
  - Same as above.
- **Scoring:**
  - Each feature is normalized and combined using a weighted sum:
    - Transaction consistency (30%)
    - Risk management (25%)
    - Protocol engagement (20%)
    - Financial stability (15%)
    - Time-based factors (10%)
  - The result is scaled to 0–100.
- **Score Band:**
  - Scores are mapped to bands: Risky, Low, Good, Very Good, Excellent.

#### Rationale
- This approach is transparent, customizable, and easy to justify in interviews or audits.

---


- **Notebook:** `compound_wallet_scoring.ipynb`
  - Loads and processes raw JSON data
  - Extracts wallet-level features
  - Implements both scoring approaches
  - Outputs scores (0–100) for each wallet

---

## CSV Output

- **Top 1,000 Wallets:**
  - `wallet_scores_top1000_with_behavior.csv` (clustering approach, includes wallet address, score, and quality band)
  - `weighted_wallet_scores.csv` (weighted-score approach)



#### Justification
- **High scores:** Indicate responsible, consistent, and engaged protocol usage.
- **Low scores:** Indicate risky, bot-like, or minimal engagement behavior.

---

## Visualization & Streamlit App

- **App:** `app.py` (Streamlit UI)
  - Sidebar for inputting wallet features
  - Main area displays animated gauge, credit score, credit band, and wallet quality band
![Screenshot 2025-05-05 210319](https://github.com/user-attachments/assets/be26db55-a05b-4952-8873-5a2f448e8b6f)


---
