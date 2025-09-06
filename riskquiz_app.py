import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Set light theme and page layout
st.set_page_config(page_title="Bright Road Risk Quiz", layout="centered")

import streamlit as st

st.markdown("""
<style>

/* App background and base font color */
html, body, .stApp {
    background-color: white !important;
    color: black !important;
}

/* Target titles and section headings */
h1, h2, h3, h4, h5, h6,
.css-10trblm, .css-1v0mbdj, .css-1dp5vir {
    color: black !important;
}

/* Form labels, radio, text, etc */
label, div[role="radiogroup"] label, span, p, .stMarkdown {
    color: black !important;
}

/* Inputs and text fields */
input, select, textarea,
.stNumberInput input,
.stTextInput input {
    background-color: white !important;
    color: black !important;
}

/* Radio button circle */
input[type="radio"] {
    accent-color: black !important;
}

/* Buttons */
.stButton > button {
    background-color: black !important;
    color: white !important;
}

/* Dropdown selected value */
div[data-baseweb="select"] > div {
    background-color: white !important;
    color: black !important;
}

/* Dropdown menu list */
ul[role="listbox"] {
    background-color: white !important;
}

/* Dropdown items */
ul[role="listbox"] > li {
    color: black !important;
    background-color: white !important;
}

/* Highlighted (hovered) dropdown option */
ul[role="listbox"] > li[aria-selected="true"] {
    background-color: #f0f0f0 !important;
    color: black !important;
}

</style>
""", unsafe_allow_html=True)






# Global CSS for light theme and readable text
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: white !important;
        color: black !important;
    }

    div[role="radiogroup"] label {
        color: black !important;
        font-size: 16px !important;
    }

    .risk-question {
        font-size: 20px;
        font-weight: 600;
        margin-top: 20px;
        color: black !important;
    }

    input, .stNumberInput input, .stTextInput input, .stSelectbox div {
        background-color: white !important;
        color: black !important;
    }

    .stButton>button {
        background-color: black !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# APP TITLE & LOGO
# -----------------------------
st.image("brightroad_logo.jpg", width=400)
st.title("Bright Road Wealth Management Risk Quiz")

st.markdown("""
Welcome to the Bright Road Risk Tool.

This tool estimates your portfolio’s potential returns, **adjusted** for your tax, inflation,
and your personal risk tolerance.

*Note: This is an educational tool and not a guarantee of future results.*
""")

# -----------------------------
# TAX & INFLATION INPUTS
# -----------------------------
st.header("Your Tax & Inflation Info")

marginal_tax = st.number_input("Marginal Tax Rate (%)", min_value=0.0, max_value=50.0, value=17.0, step=0.1) / 100
state_tax = st.number_input("State Tax Rate (%)", min_value=0.0, max_value=20.0, value=7.0, step=0.1) / 100
inflation = st.number_input("Inflation Rate (%)", min_value=0.0, max_value=10.0, value=3.0, step=0.1) / 100
combined_tax = marginal_tax + state_tax - (marginal_tax * state_tax)

# -----------------------------
# VOLATILITY BANDS (6 options — dropdown shows only SD + range)
# -----------------------------
bands = [
    {"mean_pct": 5.15, "vol_pct": 2.55},   # 0/100
    {"mean_pct": 6.56, "vol_pct": 4.09},   # 20/80
    {"mean_pct": 7.89, "vol_pct": 6.66},   # 40/60
    {"mean_pct": 8.94, "vol_pct": 9.38},   # 60/40
    {"mean_pct": 9.90, "vol_pct": 12.20},  # 80/20
    {"mean_pct": 10.72,"vol_pct": 15.04},  # 100/0
]

# Build labels for dropdown (only SD + range shown)
labels = []
for b in bands:
    lower = b["mean_pct"] - b["vol_pct"]
    upper = b["mean_pct"] + b["vol_pct"]
    label = f"1 SD: ±{b['vol_pct']:.2f}% | Range: {lower:.2f}% to {upper:.2f}%"
    labels.append(label)

st.header("Choose Your Volatility Band")
choice_label = st.selectbox(
    "Select the return/volatility profile that matches your comfort:",
    labels
)

# Map back to the selected band
sel_idx = labels.index(choice_label)
sel_band = bands[sel_idx]

# Convert to decimals for calculations (annualized return still drives outputs/simulation)
base_nominal = sel_band["mean_pct"] / 100.0
sigma = sel_band["vol_pct"] / 100.0

# -----------------------------
# Source disclosure
# -----------------------------
st.caption("Data source: Matrix Book 2025 (DFA). Calculations/illustration by BRWM.")




# -----------------------------
# RISK TOLERANCE QUESTIONS
# -----------------------------
st.header("Risk Tolerance Questionnaire")

questions = [
    ("You can take $100 guaranteed, or flip a coin to win $200 or nothing. Which do you choose?", ["Take the sure $100", "Flip the coin for $200"]),
    ("If your portfolio dropped 10% in a month, would you:", ["Sell investments to stop the losses", "Stay invested and wait for recovery"]),
    ("You can lock in a 5% gain or risk a 50/50 chance between gaining 15% or losing 5%. Which do you pick?", ["Lock in the 5% gain", "Risk the 50/50 outcome"]),
    ("If the news says a market crash is coming, would you:", ["Move to cash to avoid losses", "Keep your investments and stay the course"]),
    ("A friend shares a hot investment tip that could earn 40%, but might lose 20%. Do you:", ["Avoid the risk", "Invest and take the chance"]),
    ("You can earn a safe 2% or take a 70% chance of earning 10% and a 30% chance of losing 10%. Do you:", ["Take the safe 2%", "Go for the higher return despite the risk"]),
    ("If you own 10 different stocks, would you:", ["Keep them all to spread risk", "Sell them all and invest in your favorite stock"]),
    ("You’re up 10% for the year. Do you:", ["Stop now and secure the gain", "Keep investing, even if the market might drop"]),
    ("You can choose a portfolio with smaller ups and downs, or one that could go way up or way down. Which do you prefer?", ["Smaller ups and downs", "Big swings for bigger gains"]),
    ("You’re given a choice between a savings account that grows slowly but safely, or investing in stocks which could make more but also lose money. Do you:", ["Choose the savings account", "Invest in stocks for higher potential"]),
]

risk_points = []
for i, (q_text, choices) in enumerate(questions):
    st.markdown(f"<div class='risk-question'>{q_text}</div>", unsafe_allow_html=True)
    choice = st.radio("", choices, key=f"q{i}")
    risk_points.append(-2 if choice == choices[0] else 2)

risk_score = sum(risk_points)
risk_adjustment = risk_score * 0.001

# -----------------------------
# CALCULATIONS
# -----------------------------
adjusted_nominal = base_nominal + risk_adjustment
after_tax_nominal = adjusted_nominal * (1 - combined_tax)
net_net_net_return = (1 + after_tax_nominal) / (1 + inflation) - 1

# -----------------------------
# RESULTS
# -----------------------------
st.markdown(f"""
## Your Results

- **Risk-Adjusted Nominal Return:** {adjusted_nominal*100:.2f}%
- **Risk-Adjusted After-Tax and Inflation Return:** {net_net_net_return*100:.2f}%
""")

# -----------------------------
# PROJECTION SIMULATION CHART
# -----------------------------
st.header("Projection Simulation")

years = 30
start_value = 100000
mu = np.log(1 + adjusted_nominal)
sigma = std_dev
t = np.arange(years + 1)

mean_path = start_value * np.exp(mu * t)
path_upper_1 = np.minimum(mean_path * np.exp(sigma * t), mean_path * 2.5)
path_lower_1 = mean_path * np.exp(-sigma * t)
path_upper_2 = np.minimum(mean_path * np.exp(2 * sigma * t), mean_path * 3)
path_lower_2 = mean_path * np.exp(-2 * sigma * t)

random_shocks = np.random.normal(0, sigma, size=years)
log_returns = mu + random_shocks - (sigma**2)/2
simulated_path = start_value * np.exp(np.insert(np.cumsum(log_returns), 0, 0))

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(t, mean_path, label="Expected Value (EV)", color="red", linewidth=2)
ax.fill_between(t, path_lower_1, path_upper_1, color="green", alpha=0.3, label="±1 SD")
ax.fill_between(t, path_lower_2, path_upper_2, color="gold", alpha=0.2, label="±2 SD")
ax.plot(t, simulated_path, color="cyan", label="Simulated Path", linewidth=1.5)

ax.set_title("Projected Portfolio Value Over 30 Years")
ax.set_xlabel("Years")
ax.set_ylabel("Portfolio Value ($)")
ax.legend()
ax.ticklabel_format(style='plain', axis='y')
ax.get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f'${x:,.0f}'))

st.pyplot(fig)

# -----------------------------
# DISCLOSURE
# -----------------------------
st.markdown("""
---
**Disclosure**  

Bright Road Wealth Management, LLC (“BRWM”) is a Registered Investment Adviser ("RIA"). Registration as an investment adviser does not imply a certain level of skill or training, and the content of this communication has not been approved or verified by the United States Securities and Exchange Commission or by any state securities authority. BRWM renders individualized investment advice to persons in a particular state only after complying with the state's regulatory requirements, or pursuant to an applicable state exemption or exclusion. All investments carry risk, and no investment strategy can guarantee a profit or protect from loss of capital. Past performance is not indicative of future results.
""")


