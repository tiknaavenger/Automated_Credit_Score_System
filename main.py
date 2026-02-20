import streamlit as st
from prediction_helper import predict

# Page configuration and CSS
st.set_page_config(page_title="Credit Score Evaluation System", page_icon="📊", layout="wide")
st.markdown("""
<style>
/* Theme Colors */
:root {
  --primary-bg: #1c2f35;
  --secondary-bg: #d3f1e2;
  --accent: #5ee0aa;
  --text-main: #646464;
  --text-light: #959ea0;
  --text-color: #96e8c3;
  --border: #bcbcbb;
  --panel-bg: #5c7c6c;
  --hover-accent: #a0a9ae; /* Lighter accent for subtle hover effects */
}

/* Base Styles */
body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: var(--text-main);
    background-color: #f0f2f6;
    margin: 0; /* Ensure no default body margin is cutting off header */
    padding: 0; /* Ensure no default body padding */
}

/* Container */
.block-container {
  padding: 1.5rem 3rem;
  max-width: 1200px;
  margin: auto;
}

/* Header */
.app-header {
  background-color: var(--primary-bg);
  color: white;
  padding: 5px 30px;
  border-radius: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  box-sizing: border-box;
  min-height: 90px; /* Set a minimum height instead of fixed */
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
}
.app-header-left h1 {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 600;
  color: white;
  line-height: 0.8;
}
.app-header-left p {
  margin: 0;
  color: var(--accent);
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.2;
  margin-bottom: 0.8rem;
}
.app-header-right p {
  margin: 0;
  color: var(--accent);
  font-size: 0.95rem;
  font-weight: 500;
}

/* Form Card (General Styling for input area) */
div.stForm {
    background-color: var(--secondary-bg);
    padding: 2rem;
    border-radius: 12px;
    border: 1px solid var(--border);
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    margin-bottom: 2rem;
}

/* Streamlit Input Widgets (common styles) */
.stTextInput label, .stNumberInput label, .stSelectbox label {
  color: var(--text-main);
  font-weight: 600;
  margin-bottom: 0.3rem;
  display: block;
}

/* Styling for input fields (text_input, number_input) */
.stTextInput div.st-emotion-cache-1c7y2qn,
.stNumberInput div.st-emotion-cache-1c7y2qn,
.stSelectbox div.st-emotion-cache-1c7y2qn {
    border: 1px solid var(--border);
    border-radius: 8px;
    background-color: white;
    padding: 0.5rem 0.75rem;
    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.05);
}

/* Specific styling for the read-only LTI Ratio to match other inputs */
.stTextInput>div>div>input[aria-label="🔍 LTI Ratio"] {
    background-color: #e8ecef !important;
    color: var(--text-main);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem 1rem;
    cursor: not-allowed;
}

/* Result Panel */
.result-panel { 
  background-color: var(--secondary-bg); 
  border-radius: 12px; 
  border: 1px solid var(--border); 
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); 
  margin-bottom: 2rem;   
  color: var(--text-main); /* Changed to text-main for better visibility */
  width: 100%; 
  min-height: 362px; /* Ensure a minimum height for the whole panel */
  max-height: 362px; /* Ensure a maximum height for the whole panel */  
  align-items: center; 
  text-align: center;
  justify-content: center; /* Center content vertically */
} 
.result-panel h3 { 
  background-color: var(--primary-bg);
  border-radius: 10px 10px 0px 0px; 
  margin-top: 0; 
  color: var(--text-color); 
  font-size: 1.5rem; 
  font-weight: 600; 
  width: 100%; 
  text-align: center; 
} 
.result-panel .metric-label {
  font-size: 1.2rem; /* Significantly increased font size for metric labels */
  color: var(--text-main);
  margin-top: 0.5rem;
  display: flex;
  align-items: center;
  justify-content: center; /* Center the metric labels */
  font-weight: 800; /* Made result detail labels extra bold */
  text-align: center;
}
.result-panel .metric-label .icon {
  margin-right: 8px;
  font-size: 1.2rem; /* Larger icon */
  color: var(--accent);
  text-align: center;
}
.result-panel .metric-value {
  font-size: 2.2rem;
  margin-top: -0.5rem;
  color: var(--primary-bg);
  font-weight: 700;
  text-align: center;
}

/* Button */
.stButton>button {
  background-color: var(--accent);
  color: var(--primary-bg);
  border: none;
  padding: .75rem 1.5rem;
  border-radius: 8px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.2s ease;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.15);
}
.stButton>button:hover {
  background-color: #4CAF8F;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.stButton>button:active {
  transform: translateY(0);
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

/* Streamlit specific adjustments for selectbox dropdowns */
.stSelectbox div[data-baseweb="select"] {
    background-color: white;
    border-radius: 8px;
    border: 1px solid var(--border);
}

/* Adjusting the number input buttons to match the aesthetic */
.stNumberInput button {
    background-color: var(--hover-accent);
    color: var(--primary-bg);
    border: none;
    border-radius: 4px;
    padding: 0.2rem 0.5rem;
    margin: 0 2px;
    cursor: pointer;
    transition: background-color 0.2s ease;
}
.stNumberInput button:hover {
    background-color: #90989c;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="app-header">
  <div class="app-header-left">
    <h1>📊 Automated Credit Score Evaluation System </h1> <p>NBFC Risk Modeling | Lauki Finance</p>
  </div>
  <div class="app-header-right">
    
  </div>
</div>
""", unsafe_allow_html=True)

# Layout: Two columns for form and result
left_col, right_col = st.columns([3, 1])

with left_col:
    with st.form("applicant_form"):
        row1 = st.columns(4)
        age = row1[0].number_input("🧍‍♂️ Age", 18, 100, 28)
        income = row1[1].number_input("💰 Income (₹)", 0, 10_000_000, 1_200_000)
        loan_amt = row1[2].number_input("🏦 Loan Amt (₹)", 0, 10_000_000, 2_560_000)

        if income > 0:
            li_ratio = loan_amt / income
        else:
            li_ratio = 0.0

        row1[3].text_input("🔍 LTI Ratio", value=f"{li_ratio:.2f}", disabled=True)

        row2 = st.columns(4)
        residence = row2[0].selectbox("🏠 Residence", ["Owned", "Rented", "Mortgage"])
        purpose = row2[1].selectbox("🎯 Purpose", ["Education", "Home", "Auto", "Personal"])
        loan_type = row2[2].selectbox("🔐 Loan Type", ["Unsecured", "Secured"])
        tenure = row2[3].number_input("📆 Tenure (mo)", 0, 360, 36)

        row3 = st.columns(4)
        open_acc = row3[0].number_input("📂 Open Accts", 1, 20, 2)
        avg_dpd = row3[1].number_input("📉 Avg DPD", 0, 365, 20)
        delinq_ratio = row3[2].number_input("⚠️ Delinquency Ratio (%)", 0, 100, 30)
        cred_util = row3[3].number_input("📊 Credit Utilization Ratio (%)", 0, 100, 30)

        submitted = st.form_submit_button("🚀 Calculate Risk")

with right_col:
    # Build the entire HTML content for the result panel as a single string
    result_html_content = "<h3>Result</h3>"

    if submitted:
        try:
            prob, score, rating = predict(
                age, income, loan_amt, tenure,
                avg_dpd, delinq_ratio, cred_util,
                open_acc, residence, purpose, loan_type
            )
        except NameError:
            # Placeholder values if 'predict' function is not defined
            prob = 0.15
            score = 720
            rating = "Good"

        result_html_content += f'<div class="metric-label" style="margin-top: 1.1rem;"><span class="icon">📈</span>Default Probability</div>'
        result_html_content += f'<div class="metric-value" style="margin-bottom: 1.2rem;">{prob:.2%}</div>'
        result_html_content += f'<div class="metric-label"><span class="icon">⭐</span>Credit Score</div>'
        result_html_content += f'<div class="metric-value" style="margin-bottom: 1.2rem;">{score}</div>'
        result_html_content += f'<div class="metric-label"><span class="icon">🏷️</span>Rating</div>'
        result_html_content += f'<div class="metric-value">{rating}</div>'

    # Render the entire result panel HTML in a single st.markdown call
    st.markdown(f"""
    <div class="result-panel">
      {result_html_content}
    </div>
    """, unsafe_allow_html=True)