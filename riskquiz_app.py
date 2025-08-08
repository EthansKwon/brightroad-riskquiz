import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Bright Road Risk Quiz",
    layout="centered"
)

# -----------------------------
# HEADER & INTRO
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
# USER INPUTS
# -----------------------------
st.header("Your Tax & Inflation Info")
marginal_tax = st.number_input("Marginal Tax Rate (%)", min_value=0.0, max_value=60.0, value=17.0)
state_tax = st.number_input("State Tax Rate (%)", min_value=0.0, max_value=20.0, value=7.0)
inflation = st.number_input("Inflation Rate (%)", min_value=0.0, max_value=10.0, value=3.0)

st.header("Choose Your Volatility Band")
vol_band = st.selectbox(
    "Select the volatility range that matches your comfort with market swings:",
    options=[
        "Worst Year: -3%, Best Year: +6%",
        "Worst Year: -10%, Best Year: +18%",
        "Worst Year: -20%, Best Year: +30%"
    ]
)

# -----------------------------
# RISK TOLERANCE QUESTIONS
# -----------------------------
st.header("Risk Tolerance Questionnaire")

questions = [
    ("You can take $100 guaranteed, or flip a coin to win $200 or nothing. Which do you choose?",
     ["Take the sure $100", "Flip the coin for $200"]),

    ("If your portfolio dropped 10% in a month, would you:",
     ["Sell investments to stop the losses", "Stay invested and wait for recovery"]),

    ("You can lock in a 5% gain or risk a 50/50 chance between gaining 15% or losing 5%. Which do you pick?",
     ["Lock in the 5% gain", "Risk the 50/50 outcome"]),

    ("If the news says a market crash is coming, would you:",
     ["Move to cash to avoid losses", "Keep your investments and stay the course"]),

    ("A friend shares a hot investment tip that could earn 40%, but might lose 20%. Do you:",
     ["Avoid it", "Invest a portion"]),

    ("When thinking about your money, do you worry more about:",
     ["Losing money", "Missing out on gains"]),

    ("Would you rather invest in something steady or something with big swings?",
     ["Steady", "Big swings"]),

    ("How would you feel seeing your portfolio lose 15% in one year?",
     ["Nervous", "Fine — I know markets go up and down"]),

    ("When markets fall, do you:",
     ["Want to pull money out", "Want to buy more while it's cheaper"]),

    ("You win $1,000. Do you:",
     ["Put it in savings", "Invest it for long-term growth"]),
]

risk_score = 0
for i, (q, options) in enumerate(questions):
    answer = st.radio(f"{i+1}. {q}", options, key=f"q{i}")
    if options.index(answer) == 1:
        risk_score += 1  # award 1 point for risk-tolerant answer

# -----------------------------
# RETURN CALCULATION
# -----------------------------
if vol_band == "Worst Year: -3%, Best Year: +6%":
    nominal_return = 4.0
elif vol_band == "Worst Year: -10%, Best Year: +18%":
    nominal_return = 7.0
else:
    nominal_return = 10.0

# Adjust for risk tolerance (centered at 5 risk points)
risk_adjustment = (risk_score - 5) * 0.3  # ±1.5% max adjustment
adjusted_nominal = nominal_return + risk_adjustment

# After-tax & after-inflation
tax_effect = (1 - ((marginal_tax + state_tax) / 100))
after_tax = adjusted_nominal * tax_effect
real_return = after_tax - inflation

# -----------------------------
# RESULTS SUMMARY
# -----------------------------
st.subheader("Your Adjusted Results")
st.markdown(f"**Risk-Adjusted Nominal Return:** {adjusted_nominal:.2f}%")
st.markdown(f"**After Tax & Inflation Return:** {real_return:.2f}%")

# -----------------------------
# SIMULATION PLOT
# -----------------------------
st.subheader("Projection Range")

years = 30
mean = adjusted_nominal / 100
std_dev = (abs(float(vol_band.split(":")[1].split(",")[0].replace('%', ''))) + 
           abs(float(vol_band.split(",")[1].split(":")[1].replace('%', '')))) / 2 / 100

sim_years = np.arange(1, years + 1)
ev = 100000 * np.power(1 + mean, sim_years)
sd1_upper = 100000 * np.power(1 + (mean + std_dev), sim_years)
sd1_lower = 100000 * np.power(1 + (mean - std_dev), sim_years)
sd2_upper = 100000 * np.power(1 + (mean + 2 * std_dev), sim_years)
sd2_lower = 100000 * np.power(1 + (mean - 2 * std_dev), sim_years)

plt.figure(figsize=(10, 5))
plt.plot(sim_years, ev, label="Expected Value", color="deepskyblue", linewidth=2)
plt.plot(sim_years, sd1_upper, linestyle="--", color="orange", label="1 SD Above")
plt.plot(sim_years, sd1_lower, linestyle="--", color="orange", label="1 SD Below")
plt.plot(sim_years, sd2_upper, linestyle="--", color="red", label="2 SD Above")
plt.plot(sim_years, sd2_lower, linestyle="--", color="red", label="2 SD Below")
plt.xlabel("Years")
plt.ylabel("Portfolio Value ($)")
plt.title("Simulation Range (Based on Risk & Volatility)")
plt.legend()
plt.grid(True)
st.pyplot(plt)

# -----------------------------
# DISCLOSURE
# -----------------------------
st.markdown("""---""")
st.caption("""
**Disclosure**: Bright Road Wealth Management, LLC (“BRWM”) is a Registered Investment Adviser ("RIA"). 
Registration as an investment adviser does not imply a certain level of skill or training, and the content 
of this communication has not been approved or verified by the United States Securities and Exchange Commission 
or by any state securities authority. BRWM renders individualized investment advice to persons in a particular 
state only after complying with the state's regulatory requirements, or pursuant to an applicable state 
exemption or exclusion. All investments carry risk, and no investment strategy can guarantee a profit or 
protect from loss of capital. Past performance is not indicative of future results.
""")

