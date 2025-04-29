import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Set page config
st.set_page_config(
    page_title="Creative Catalysts - Chemistry Virtual Lab",
    page_icon=":test_tube:",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        max-width: 1200px;
        padding: 2rem;
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .title {
        font-size: 2.5rem;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #7f8c8d;
        margin-bottom: 2rem;
    }
    .experiment-card {
        padding: 1.5rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        margin-bottom: 1rem;
        transition: transform 0.2s;
    }
    .experiment-card:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .experiment-title {
        color: #3498db;
        margin-bottom: 0.5rem;
    }
    .button {
        background-color: #3498db;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        cursor: pointer;
        font-size: 1rem;
        margin-top: 1rem;
    }
    .button:hover {
        background-color: #2980b9;
    }
    .observation-table {
        width: 100%;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Session state management
if 'current_page' not in st.session_state:
    st.session_state.current_page = "home"
if 'phenol_data' not in st.session_state:
    st.session_state.phenol_data = pd.DataFrame(columns=[
        "Volume of phenol (ml)", "Volume of water (ml)", 
        "Volume % of phenol", "Temp of disappearance (°C)", 
        "Temp of appearance (°C)", "Mean Temp (°C)"
    ])
if 'water_added' not in st.session_state:
    st.session_state.water_added = 3.0
if 'cond_data' not in st.session_state:
    st.session_state.cond_data = pd.DataFrame(columns=[
        "Volume of NaOH (ml)", "Conductance (mS)"
    ])
if 'naoh_normality' not in st.session_state:
    st.session_state.naoh_normality = 0.0

# Home page
def home_page():
    st.markdown('<div class="header">', unsafe_allow_html=True)
    st.markdown('<h1 class="title">Welcome to Creative Catalysts</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">A virtual Physical & Analytical Chemistry lab created by the Chemical Engineering students of SRMIST</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="experiment-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="experiment-title">DETERMINATION OF CRITICAL SOLUTION TEMPERATURE FOR PHENOL - WATER SYSTEM</h2>', unsafe_allow_html=True)
        st.markdown('<p>Study the phase behavior of partially miscible liquids and determine the critical solution temperature.</p>', unsafe_allow_html=True)
        if st.button("Start Experiment", key="phenol_exp"):
            st.session_state.current_page = "phenol_intro"
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="experiment-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="experiment-title">CONDUCTOMETRIC TITRATION</h2>', unsafe_allow_html=True)
        st.markdown('<p>Determine the strength of hydrochloric acid and acetic acid in a given mixture.</p>', unsafe_allow_html=True)
        if st.button("Start Experiment", key="cond_exp"):
            st.session_state.current_page = "cond_intro"
        st.markdown('</div>', unsafe_allow_html=True)

# Phenol-Water Experiment Functions
def phenol_intro():
    st.title("DETERMINATION OF CRITICAL SOLUTION TEMPERATURE FOR PHENOL - WATER SYSTEM")
    
    with st.expander("Aim"):
        st.write("To determine the critical solution temperature for phenol-water system and to find out the percentage of phenol in the given sample")
    
    with st.expander("Apparatus"):
        st.write("""
        - Burette
        - Boiling tube
        - Thermometer
        - Water bath
        - Stirrer
        - Clamp stand
        """)
    
    with st.expander("Principle"):
        st.write("""
        Phenol and water are partially miscible at ordinary temperatures. On shaking these two liquids, two saturated solutions of different compositions are obtained - one of phenol in water and another of water in phenol. 
        
        The mutual solubility increases with temperature until at a certain temperature (critical solution temperature), the two conjugate solutions become one homogeneous solution.
        """)
    
    if st.button("Start the experiment"):
        st.session_state.current_page = "phenol_exp1"
        st.session_state.water_added = 3.0
        st.session_state.phenol_data = pd.DataFrame(columns=[
            "Volume of phenol (ml)", "Volume of water (ml)", 
            "Volume % of phenol", "Temp of disappearance (°C)", 
            "Temp of appearance (°C)", "Mean Temp (°C)"
        ])

def phenol_exp1():
    st.title("Add phenol and water in the boiling tube")
    
    phenol_vol = st.number_input("Volume of phenol taken (ml)", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    water_vol = st.number_input("Volume of water added (ml)", min_value=0.0, max_value=10.0, value=3.0, step=0.1)
    
    if st.button("Dip the boiling tube into a water bath and slowly heat the mixture with constant stirring"):
        st.session_state.phenol_vol = phenol_vol
        st.session_state.water_vol = water_vol
        st.session_state.current_page = "phenol_exp2"

def phenol_exp2():
    st.title("Observe disappearance of turbidity")
    
    # Simulate temperature based on composition (realistic model)
    phenol_vol = st.session_state.phenol_vol
    water_vol = st.session_state.water_vol
    phenol_percent = (phenol_vol / (phenol_vol + water_vol)) * 100
    
    # Model for disappearance temperature (simplified)
    if phenol_percent < 20 or phenol_percent > 80:
        disappear_temp = 50 + phenol_percent * 0.5
    else:
        disappear_temp = 60 + (phenol_percent - 20) * 0.3
    
    st.write(f"At {disappear_temp:.1f}°C, the turbidity of the mixture just disappears to become a clear solution.")
    
    if st.button("Remove the boiling tube from the heat and cool the mixture slowly with constant stirring"):
        st.session_state.disappear_temp = disappear_temp
        st.session_state.current_page = "phenol_exp3"

def phenol_exp3():
    st.title("Observe reappearance of turbidity")
    
    phenol_vol = st.session_state.phenol_vol
    water_vol = st.session_state.water_vol
    phenol_percent = (phenol_vol / (phenol_vol + water_vol)) * 100
    disappear_temp = st.session_state.disappear_temp
    
    # Model for reappearance temperature (hysteresis effect)
    reappear_temp = disappear_temp - 2 - (phenol_percent * 0.05)
    
    st.write(f"Temperature at which turbidity disappeared: {disappear_temp:.1f}°C")
    st.write(f"Temperature at which turbidity reappears: {reappear_temp:.1f}°C")
    
    mean_temp = (disappear_temp + reappear_temp) / 2
    st.write(f"Mean temperature: {mean_temp:.1f}°C")
    
    # Store data
    new_row = {
        "Volume of phenol (ml)": phenol_vol,
        "Volume of water (ml)": water_vol,
        "Volume % of phenol": phenol_percent,
        "Temp of disappearance (°C)": disappear_temp,
        "Temp of appearance (°C)": reappear_temp,
        "Mean Temp (°C)": mean_temp
    }
    st.session_state.phenol_data = pd.concat([
        st.session_state.phenol_data,
        pd.DataFrame([new_row])
    ], ignore_index=True)
    
    if water_vol < 36:
        if st.button("Add 2 ml more water to the mixture"):
            st.session_state.water_vol += 2
            st.session_state.current_page = "phenol_exp1"
    else:
        if st.button("Provide the observation table"):
            st.session_state.current_page = "phenol_table"

def phenol_table():
    st.title("Observation Table")
    st.dataframe(st.session_state.phenol_data.style.format("{:.2f}"))
    
    if st.button("Provide model graph"):
        st.session_state.current_page = "phenol_graph"

def phenol_graph():
    st.title("Model Graph")
    
    df = st.session_state.phenol_data
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["Volume % of phenol"], df["Mean Temp (°C)"], 'bo-')
    ax.set_xlabel("Volume % of phenol")
    ax.set_ylabel("Mean Temperature (°C)")
    ax.set_title("Critical Solution Temperature for Phenol-Water System")
    ax.grid(True)
    
    # Find and mark CST (highest point)
    max_idx = df["Mean Temp (°C)"].idxmax()
    cst_temp = df.loc[max_idx, "Mean Temp (°C)"]
    cst_conc = df.loc[max_idx, "Volume % of phenol"]
    
    ax.plot(cst_conc, cst_temp, 'ro', markersize=10, 
            label=f'CST: {cst_temp:.1f}°C at {cst_conc:.1f}% phenol')
    ax.legend()
    
    st.pyplot(fig)
    
    if st.button("Compute results"):
        st.session_state.current_page = "phenol_results"

def phenol_results():
    st.title("Result")
    
    df = st.session_state.phenol_data
    max_idx = df["Mean Temp (°C)"].idxmax()
    cst_temp = df.loc[max_idx, "Mean Temp (°C)"]
    cst_conc = df.loc[max_idx, "Volume % of phenol"]
    
    # Random unknown sample (30-60%)
    unknown_percent = np.random.uniform(30, 60)
    
    st.markdown(f"""
    - **The CST of phenol-water system:** {cst_temp:.1f}°C
    - **The critical solution composition:** {cst_conc:.1f}% by volume of phenol
    - **Percentage of phenol in the given sample:** {unknown_percent:.1f}% by volume
    """)
    
    if st.button("Return to home"):
        st.session_state.current_page = "home"

# Conductometric Titration Functions
def cond_intro():
    st.title("CONDUCTOMETRIC TITRATION")
    
    with st.expander("Aim"):
        st.write("To find out the strength of hydrochloric acid and acetic acid in a given mixture by titrating it against sodium hydroxide solution, conductometrically")
    
    with st.expander("Apparatus"):
        st.write("""
        - Conductivity meter
        - Burette
        - Pipette
        - Beakers
        - Volumetric flask
        """)
    
    with st.expander("Principle"):
        st.write("""
        Current is conducted through an electrolytic solution by the movement of ions. 
        - For strong acid (HCl): Conductance decreases as H⁺ are replaced by Na⁺, then increases after equivalence point due to OH⁻
        - For weak acid (CH₃COOH): Conductance increases gradually due to CH₃COO⁻ formation, then sharply after equivalence point
        """)
    
    if st.button("Start the experiment"):
        st.session_state.current_page = "cond_standardization"
        st.session_state.cond_data = pd.DataFrame(columns=[
            "Volume of NaOH (ml)", "Conductance (mS)"
        ])

def cond_standardization():
    st.title("Standardization of NaOH Solution")
    
    st.write("""
    **Procedure:**
    1. Prepare 0.05 N oxalic acid by dissolving 0.7875g in 250 ml water
    2. Pipette out 25 ml of this solution into a clean conical flask
    3. Titrate against the NaOH solution using phenolphthalein indicator
    """)
    
    naoh_vol = st.number_input("Volume of NaOH used (ml)", min_value=0.0, max_value=50.0, value=18.5, step=0.1)
    
    if st.button("Calculate NaOH Normality"):
        oxalic_normality = 0.05
        oxalic_vol = 25.0
        st.session_state.naoh_normality = (oxalic_vol * oxalic_normality) / naoh_vol
        st.write(f"**Calculated NaOH Normality:** {st.session_state.naoh_normality:.4f} N")
        
        if st.button("Proceed to Titration"):
            st.session_state.current_page = "cond_titration"

def cond_titration():
    st.title("Conductometric Titration")
    
    st.write("""
    **Procedure:**
    1. Dilute the acid mixture sample to 100 ml
    2. Pipette out 10 ml into a beaker, add 10 ml water
    3. Measure initial conductance
    4. Add 0.2 ml NaOH, stir, measure conductance
    5. Repeat until 8 ml NaOH added
    """)
    
    naoh_vol = st.number_input("Volume of NaOH added (ml)", min_value=0.0, max_value=8.0, value=0.0, step=0.2)
    
    # Simulate conductance curve
    if naoh_vol <= 4.0:
        conductance = 0.8 - 0.02 * (naoh_vol / 0.2)
    else:
        conductance = 0.6 + 0.03 * ((naoh_vol - 4.0) / 0.2)
    
    conductance += np.random.uniform(-0.01, 0.01)  # Add small noise
    
    if st.button("Record Measurement"):
        new_row = {
            "Volume of NaOH (ml)": naoh_vol,
            "Conductance (mS)": conductance
        }
        st.session_state.cond_data = pd.concat([
            st.session_state.cond_data,
            pd.DataFrame([new_row])
        ], ignore_index=True)
        
        if naoh_vol >= 8.0:
            if st.button("Complete Titration and Show Observation Table"):
                st.session_state.current_page = "cond_table"

def cond_table():
    st.title("Observation Table")
    st.dataframe(st.session_state.cond_data.style.format("{:.2f}"))
    
    if st.button("Show Model Graph"):
        st.session_state.current_page = "cond_graph"

def cond_graph():
    st.title("Model Graph")
    
    df = st.session_state.cond_data.sort_values("Volume of NaOH (ml)")
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df["Volume of NaOH (ml)"], df["Conductance (mS)"], 'bo-')
    ax.set_xlabel("Volume of NaOH (ml)")
    ax.set_ylabel("Conductance (mS)")
    ax.set_title("Conductometric Titration of Acid Mixture")
    ax.grid(True)
    
    # Find endpoints (simplified)
    df['diff'] = df["Conductance (mS)"].diff() / df["Volume of NaOH (ml)"].diff()
    
    try:
        hcl_end = df.iloc[df['diff'].idxmin()]["Volume of NaOH (ml)"]
        ax.axvline(hcl_end, color='r', linestyle='--', 
                  label=f'HCl endpoint: {hcl_end:.2f} ml')
    except:
        hcl_end = 0
    
    try:
        ch3cooh_end = df.iloc[df['diff'].idxmax()]["Volume of NaOH (ml)"]
        ax.axvline(ch3cooh_end, color='g', linestyle='--', 
                  label=f'CH₃COOH endpoint: {ch3cooh_end:.2f} ml')
    except:
        ch3cooh_end = 0
    
    ax.legend()
    st.pyplot(fig)
    
    st.session_state.hcl_end = hcl_end
    st.session_state.ch3cooh_end = ch3cooh_end
    
    if st.button("Show Calculations"):
        st.session_state.current_page = "cond_calc"

def cond_calc():
    st.title("Calculations")
    
    hcl_end = st.session_state.hcl_end
    ch3cooh_end = st.session_state.ch3cooh_end
    naoh_normality = st.session_state.naoh_normality
    
    st.markdown(f"""
    **Given:**
    - Volume of sample taken = 10 ml
    - Normality of NaOH = {naoh_normality:.4f} N
    - Volume of NaOH for HCl (Va) = {hcl_end:.2f} ml
    - Volume of NaOH for CH₃COOH (Vb - Va) = {ch3cooh_end - hcl_end:.2f} ml
    """)
    
    hcl_normality = (naoh_normality * hcl_end) / 10
    ch3cooh_normality = (naoh_normality * (ch3cooh_end - hcl_end)) / 10
    
    hcl_amount = hcl_normality * 36.5 * 100 / 1000  # g in 100 ml
    ch3cooh_amount = ch3cooh_normality * 60 * 100 / 1000  # g in 100 ml
    
    st.markdown(f"""
    **Calculations:**
    1. Normality of HCl = (N_NaOH × Va) / 10 = ({naoh_normality:.4f} × {hcl_end:.2f}) / 10 = {hcl_normality:.4f} N
    2. Amount of HCl = (N_HCl × 36.5 × 100) / 1000 = ({hcl_normality:.4f} × 36.5 × 100) / 1000 = {hcl_amount:.4f} g
    3. Normality of CH₃COOH = (N_NaOH × (Vb - Va)) / 10 = ({naoh_normality:.4f} × {ch3cooh_end - hcl_end:.2f}) / 10 = {ch3cooh_normality:.4f} N
    4. Amount of CH₃COOH = (N_CH₃COOH × 60 × 100) / 1000 = ({ch3cooh_normality:.4f} × 60 × 100) / 1000 = {ch3cooh_amount:.4f} g
    """)
    
    st.session_state.hcl_amount = hcl_amount
    st.session_state.ch3cooh_amount = ch3cooh_amount
    
    if st.button("Show Results"):
        st.session_state.current_page = "cond_results"

def cond_results():
    st.title("Results")
    
    st.markdown(f"""
    - **Amount of HCl in the given mixture:** {st.session_state.hcl_amount:.4f} g
    - **Amount of CH₃COOH in the given mixture:** {st.session_state.ch3cooh_amount:.4f} g
    """)
    
    if st.button("Return to Home page"):
        st.session_state.current_page = "home"

# Main app router
if st.session_state.current_page == "home":
    home_page()
elif st.session_state.current_page == "phenol_intro":
    phenol_intro()
elif st.session_state.current_page == "phenol_exp1":
    phenol_exp1()
elif st.session_state.current_page == "phenol_exp2":
    phenol_exp2()
elif st.session_state.current_page == "phenol_exp3":
    phenol_exp3()
elif st.session_state.current_page == "phenol_table":
    phenol_table()
elif st.session_state.current_page == "phenol_graph":
    phenol_graph()
elif st.session_state.current_page == "phenol_results":
    phenol_results()
elif st.session_state.current_page == "cond_intro":
    cond_intro()
elif st.session_state.current_page == "cond_standardization":
    cond_standardization()
elif st.session_state.current_page == "cond_titration":
    cond_titration()
elif st.session_state.current_page == "cond_table":
    cond_table()
elif st.session_state.current_page == "cond_graph":
    cond_graph()
elif st.session_state.current_page == "cond_calc":
    cond_calc()
elif st.session_state.current_page == "cond_results":
    cond_results()
