
import streamlit as st
import os
import math
from io import StringIO

# Page configuration
st.set_page_config(layout="wide", page_title="SMART CVD Risk Reduction")

# CSS styling
st.markdown("""
<style>
.header { position: sticky; top: 0; background: #f7f7f7; padding: 10px; display: flex; justify-content: flex-end; z-index: 100; }
.card { background: #fff; padding: 20px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
.block-container {
  background-image: url('logo.png');
  background-repeat: no-repeat;
  background-position: center center;
  background-size: 200px 200px;
  opacity: 0.1;
}
</style>
""", unsafe_allow_html=True)

# Header with Logo
st.markdown('<div class="header">', unsafe_allow_html=True)
if os.path.exists("logo.png"):
    st.image("logo.png", width=150)
else:
    st.warning("⚠️ Please upload 'logo.png' alongside this script.")
st.markdown('</div>', unsafe_allow_html=True)

# Sidebar: Patient Information
st.sidebar.header("Patient Demographics")
age = st.sidebar.slider("Age (years)", 30, 90, 60, key="age")
sex = st.sidebar.radio("Sex", ["Male", "Female"], key="sex")
weight = st.sidebar.number_input("Weight (kg)", 40.0, 200.0, 75.0, key="weight")
height = st.sidebar.number_input("Height (cm)", 140.0, 210.0, 170.0, key="height")
bmi = weight / ((height / 100) ** 2)
st.sidebar.markdown(f"**BMI:** {bmi:.1f} kg/m²")

st.sidebar.header("Risk Factors")
smoker = st.sidebar.checkbox("Current smoker", key="smoker")
diabetes = st.sidebar.checkbox("Diabetes", key="diabetes")
st.sidebar.markdown("**Known vascular disease in the following territories:**")
vasc_cor = st.sidebar.checkbox("Coronary artery disease", key="vasc_cor")
vasc_cer = st.sidebar.checkbox("Cerebrovascular disease", key="vasc_cer")
vasc_per = st.sidebar.checkbox("Peripheral artery disease", key="vasc_per")
vasc_count = sum([vasc_cor, vasc_cer, vasc_per])
egfr = st.sidebar.slider("eGFR (mL/min/1.73 m²)", 15, 120, 90, key="egfr")

# Risk calculation functions
def estimate_10y_risk(age, sex, sbp, tc, hdl, smoker, diabetes, egfr, crp, vasc):
    sv = 1 if sex == "Male" else 0
    sm = 1 if smoker else 0
    dm = 1 if diabetes else 0
    crp_l = math.log(crp + 1)
    lp = (0.064 * age + 0.34 * sv + 0.02 * sbp + 0.25 * tc
          - 0.25 * hdl + 0.44 * sm + 0.51 * dm
          - 0.2 * (egfr / 10) + 0.25 * crp_l + 0.4 * vasc)
    raw = 1 - 0.900 ** math.exp(lp - 5.8)
    return min(raw * 100, 95.0)

def convert_5yr(r10):
    p = min(r10, 95.0) / 100
    return min((1 - (1 - p) ** 0.5) * 100, 95.0)

def estimate_lifetime_risk(age, r10):
    years = max(85 - age, 0)
    p10 = min(r10, 95.0) / 100
    annual = 1 - (1 - p10) ** (1 / 10)
    return min((1 - (1 - annual) ** years) * 100, 95.0)

# Output: placeholder
st.title("SMART CVD Risk Reduction Tool")
st.write("This version contains sidebar entry and background logic. Full therapy and results sections follow.")

# Footer
st.markdown("---")
st.markdown("Created by Samuel Panday — 21/04/2025")
st.markdown("PRIME team (Prevention Recurrent Ischaemic Myocardial Events), King's College Hospital, London")
st.markdown("This tool is for informational purposes only and should be used in conjunction with a qualified healthcare provider.")
