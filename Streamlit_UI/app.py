import streamlit as st
import numpy as np
import joblib
import plotly.graph_objects as go
import time

# Load models and config
scaler = joblib.load('scaler.joblib')
pca = joblib.load('pca.joblib')
kmeans = joblib.load('kmeans.joblib')
feature_cols = joblib.load('feature_cols.joblib')
cluster_to_score = joblib.load('cluster_to_score.joblib')

st.title("Compound V2 Wallet Credit Score Predictor")

st.markdown("""
Enter your wallet's transaction summary in the sidebar to estimate your credit score.
""")

# --- SIDEBAR INPUTS ---
st.sidebar.header("Wallet Transaction Summary")
user_input = {}
user_input['total_transactions'] = st.sidebar.number_input("Total Transactions", min_value=1, value=10)
user_input['total_amount_usd'] = st.sidebar.number_input("Total Amount (USD)", min_value=0.0, value=1000.0)
user_input['avg_amount_usd'] = st.sidebar.number_input("Average Transaction Amount (USD)", min_value=0.0, value=100.0)
user_input['std_amount_usd'] = st.sidebar.number_input("Std Dev of Transaction Amount (USD)", min_value=0.0, value=10.0)
user_input['wallet_age_days'] = st.sidebar.number_input("Wallet Age (days)", min_value=1, value=30)
user_input['asset_diversity'] = st.sidebar.number_input("Number of Unique Assets Used", min_value=1, value=2)
user_input['txn_per_day'] = st.sidebar.number_input("Transactions per Day", min_value=0.0, value=0.5)

def score_band_label(score):
    if score < 20:
        return "Risky"
    elif score < 40:
        return "Low"
    elif score < 60:
        return "Good"
    elif score < 80:
        return "Very Good"
    else:
        return "Excellent"
    
def wallet_quality_band(user_input):
    if (
        user_input['total_transactions'] >= 10 and
        user_input['wallet_age_days'] >= 30 and
        user_input['asset_diversity'] >= 2
    ):
        return "Good"
    else:
        return "Bad"

# --- MAIN AREA: PREDICT BUTTON AND OUTPUT ---
if st.sidebar.button("Predict Credit Score"):
    with st.spinner('Calculating your credit score...'):
        time.sleep(1.5)  # Simulate loading

        # Prepare input
        X = np.array([[user_input[col] for col in feature_cols]])
        X_scaled = scaler.transform(X)
        X_pca = pca.transform(X_scaled)
        cluster = kmeans.predict(X_pca)[0]
        base_score = cluster_to_score[cluster]
        feature_adj = X_scaled.mean(axis=1)[0] * (100 / len(cluster_to_score) / 2)
        credit_score = np.clip(base_score + feature_adj, 0, 100)
        credit_band = score_band_label(credit_score)
        wallet_band = wallet_quality_band(user_input)

        # Plotly gauge chart
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = credit_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Credit Score", 'font': {'size': 24}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 20], 'color': "#d9534f"},      # Risky
                    {'range': [20, 40], 'color': "#f0ad4e"},     # Low
                    {'range': [40, 60], 'color': "#ffd700"},     # Good
                    {'range': [60, 80], 'color': "#5bc0de"},     # Very Good
                    {'range': [80, 100], 'color': "#5cb85c"}     # Excellent
                ],
                'threshold': {
                    'line': {'color': "black", 'width': 6},
                    'thickness': 0.75,
                    'value': credit_score
                }
            }
        ))

        st.plotly_chart(fig, use_container_width=True)
        st.success(f"Estimated Credit Score: **{credit_score:.2f}**")
        st.info(f"Credit Score Quality: **{credit_band}**")
        st.info(f"Wallet Quality: **{wallet_band}**")