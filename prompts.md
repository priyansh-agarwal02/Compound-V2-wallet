# 🧠 Project Prompt: AI-Powered Credit Scoring for Compound V2 Wallets

## 🚩 Objective

Create a complete credit scoring pipeline in **Jupyter Notebook(s)** that:
- Parses and cleans transaction-level JSON data from Compound V2
- Engineers wallet-level features
- Clusters wallets and computes a **credit score (0–100)**
- Outputs wallet scores and intermediate analysis

## Data Cleaning
Design an end-to-end pipeline that:
- Parses raw transaction-level JSON data from Compound V2 in the Data Folder
- Normalizes and engineers features at the **wallet level**
- Builds a credit scoring mechanism (0–100) using **unsupervised learning**
- Outputs results for further analytics or dashboarding

---

## 📁 Input Data

Located in `Data/` directory:

Each contains records like:
```json
{
  "id": "0x...",
  "amount": "123.45",
  "amountUSD": "1234.56",
  "asset": { "id": "0xeee..." , "symbol":"USDT"}
  "account": { "id": "0xabc123..." },
  "timestamp": "1638200000",
  "hash": "0x123..."
}
