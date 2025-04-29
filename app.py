import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
    st.session_state.phenol_data = pd.DataFrame(columns=[
        "Phenol (ml)", "Water (ml)", "% Phenol", 
        "Disappear Temp (°C)", "Reappear Temp (°C)", "Mean Temp (°C)"
    ])
    st.session_state.water_vol = 3.0
    st.session_state.cond_data = pd.DataFrame(columns=["NaOH (ml)", "Conductance (mS)"])
    st.session_state.naoh_normality = 0.1
    st.session_state.current_naoh = 0.0

# --------------------------
# PHENOL-WATER EXPERIMENT (FIXED DUPLICATE ROWS)
# --------------------------

def phenol_intro():
    st.title("Phenol-Water CST Determination")
    st.write("**Aim:** Determine critical solution temperature")
    if st.button("Start Experiment"):
        st.session_state.phenol_data = pd.DataFrame(columns=[  # Reset data
            "Phenol (ml)", "Water (ml)", "% Phenol", 
            "Disappear Temp (°C)", "Reappear Temp (°C)", "Mean Temp (°C)"
        ])
        st.session_state.water_vol = 3.0
        st.session_state.page = "phenol_exp1"

def phenol_exp1():
    st.title("Add Reagents")
    
    water = st.number_input(
        "Water volume (ml)", 
        min_value=3.0,
        max_value=36.0,
        value=st.session_state.water_vol,
        step=0.1,
        key="water_input"
    )
    
    phenol = st.number_input(
        "Phenol volume (ml)",
        min_value=5.0,
        max_value=10.0,
        value=5.0,
        step=0.1,
        key="phenol_input"
    )
    
    if st.button("Heat Mixture"):
        st.session_state.phenol_vol = phenol
        st.session_state.water_vol = water
        st.session_state.page = "phenol_exp2"

def phenol_exp2():
    st.title("Observe Turbidity")
    
    total = st.session_state.phenol_vol + st.session_state.water_vol
    percent = (st.session_state.phenol_vol / total) * 100
    
    # Realistic temperature model
    if percent < 20:
        disappear = 50 + percent * 0.5
    elif percent > 80:
        disappear = 90 - (percent - 80) * 0.5
    else:
        disappear = 60 + (percent - 20) * 0.3
    
    reappear = disappear - 2 - (percent * 0.05)
    
    st.write(f"**Turbidity disappears at:** {disappear:.1f}°C")
    
    if st.button("Cool Mixture"):
        st.session_state.disappear = disappear
        st.session_state.reappear = reappear
        st.session_state.page = "phenol_exp3"

def phenol_exp3():
    st.title("Record Temperatures")
    
    # Check if this observation already exists
    existing = st.session_state.phenol_data[
        (st.session_state.phenol_data["Phenol (ml)"] == st.session_state.phenol_vol) &
        (st.session_state.phenol_data["Water (ml)"] == st.session_state.water_vol)
    ].empty
    
    if existing:
        new_row = {
            "Phenol (ml)": st.session_state.phenol_vol,
            "Water (ml)": st.session_state.water_vol,
            "% Phenol": (st.session_state.phenol_vol / total) * 100,
            "Disappear Temp (°C)": st.session_state.disappear,
            "Reappear Temp (°C)": st.session_state.reappear,
            "Mean Temp (°C)": (st.session_state.disappear + st.session_state.reappear) / 2
        }
        st.session_state.phenol_data = pd.concat([
            st.session_state.phenol_data,
            pd.DataFrame([new_row])
        ], ignore_index=True)
    
    st.dataframe(st.session_state.phenol_data.style.format("{:.2f}"))
    
    if st.session_state.water_vol < 36:
        if st.button("Add 2ml More Water"):
            st.session_state.water_vol = min(st.session_state.water_vol + 2, 36.0)
            st.session_state.page = "phenol_exp1"
    else:
        if st.button("Show Graph"):
            st.session_state.page = "phenol_graph"

def phenol_graph():
    st.title("Phase Diagram")
    
    df = st.session_state.phenol_data.drop_duplicates()  # Ensure no duplicates
    
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(df["% Phenol"], df["Mean Temp (°C)"], 'bo-')
    
    max_temp = df["Mean Temp (°C)"].max()
    cst_conc = df.loc[df["Mean Temp (°C)"] == max_temp, "% Phenol"].values[0]
    ax.plot(cst_conc, max_temp, 'ro', markersize=8, label=f"CST: {max_temp:.1f}°C")
    
    ax.set_xlabel("% Phenol")
    ax.set_ylabel("Temperature (°C)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    
    if st.button("Return Home"):
        st.session_state.page = "home"

# --------------------------
# CONDUCTOMETRIC TITRATION
# --------------------------

def cond_intro():
    st.title("Conductometric Titration")
    st.write("**Aim:** Determine strength of HCl and CH₃COOH in mixture")
    if st.button("Start Experiment"):
        st.session_state.cond_data = pd.DataFrame(columns=["NaOH (ml)", "Conductance (mS)"])
        st.session_state.current_naoh = 0.0
        st.session_state.page = "cond_standardize"

def cond_standardize():
    st.title("Standardize NaOH Solution")
    
    naoh_used = st.number_input(
        "Volume of NaOH used (ml)", 
        min_value=0.1, 
        max_value=50.0, 
        value=18.5, 
        step=0.1
    )
    
    if st.button("Calculate NaOH Normality"):
        oxalic_normality = 0.05
        oxalic_vol = 25.0
        st.session_state.naoh_normality = (oxalic_vol * oxalic_normality) / naoh_used
        st.success(f"NaOH Normality: {st.session_state.naoh_normality:.4f} N")
        
    if st.button("Proceed to Titration"):
        st.session_state.page = "cond_titration"

def cond_titration():
    st.title("Conductometric Titration")
    
    naoh_added = st.number_input(
        "Add NaOH (ml)", 
        min_value=0.0, 
        max_value=8.0, 
        value=st.session_state.current_naoh, 
        step=0.2
    )
    
    # Simulate conductance curve
    if naoh_added <= 4.0:
        conductance = 0.8 - 0.02 * (naoh_added / 0.2)
    else:
        conductance = 0.6 + 0.03 * ((naoh_added - 4.0) / 0.2)
    
    if st.button("Record Measurement"):
        if naoh_added not in st.session_state.cond_data["NaOH (ml)"].values:
            new_row = {"NaOH (ml)": naoh_added, "Conductance (mS)": conductance}
            st.session_state.cond_data = pd.concat([
                st.session_state.cond_data,
                pd.DataFrame([new_row])
            ], ignore_index=True)
            st.session_state.current_naoh = min(naoh_added + 0.2, 8.0)
    
    st.dataframe(st.session_state.cond_data.style.format("{:.2f}"))
    
    if naoh_added >= 8.0:
        if st.button("Complete Titration"):
            st.session_state.page = "cond_graph"

def cond_graph():
    st.title("Titration Curve")
    
    df = st.session_state.cond_data.sort_values("NaOH (ml)")
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(df["NaOH (ml)"], df["Conductance (mS)"], 'bo-')
    
    # Find endpoints
    df['diff'] = df["Conductance (mS)"].diff() / df["NaOH (ml)"].diff()
    try:
        hcl_end = df.iloc[df['diff'].idxmin()]["NaOH (ml)"]
        ax.axvline(hcl_end, color='r', linestyle='--', label=f'HCl endpoint: {hcl_end:.2f} ml')
    except:
        hcl_end = 0
    
    try:
        ch3cooh_end = df.iloc[df['diff'].idxmax()]["NaOH (ml)"]
        ax.axvline(ch3cooh_end, color='g', linestyle='--', label=f'CH₃COOH endpoint: {ch3cooh_end:.2f} ml')
    except:
        ch3cooh_end = 0
    
    ax.set_xlabel("Volume of NaOH (ml)")
    ax.set_ylabel("Conductance (mS)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
    
    if st.button("Show Results"):
        st.session_state.page = "cond_results"

def cond_results():
    st.title("Results")
    
    df = st.session_state.cond_data.sort_values("NaOH (ml)")
    df['diff'] = df["Conductance (mS)"].diff() / df["NaOH (ml)"].diff()
    
    try:
        hcl_end = df.iloc[df['diff'].idxmin()]["NaOH (ml)"]
        ch3cooh_end = df.iloc[df['diff'].idxmax()]["NaOH (ml)"]
        
        hcl_normality = (st.session_state.naoh_normality * hcl_end) / 10
        ch3cooh_normality = (st.session_state.naoh_normality * (ch3cooh_end - hcl_end)) / 10
        
        hcl_amount = hcl_normality * 36.5 * 100 / 1000
        ch3cooh_amount = ch3cooh_normality * 60 * 100 / 1000
        
        st.markdown(f"""
        - **Amount of HCl:** {hcl_amount:.4f} g
        - **Amount of CH₃COOH:** {ch3cooh_amount:.4f} g
        """)
    except:
        st.error("Could not calculate endpoints. Please check your titration data.")
    
    if st.button("Return Home"):
        st.session_state.page = "home"

# --------------------------
# MAIN APP CONTROL
# --------------------------

def home():
    st.markdown("""
    <div style='text-align: center; margin-bottom: 2rem;'>
        <h1 style='color: #2c3e50;'>Welcome to Creative Catalysts</h1>
        <p style='color: #7f8c8d;'>
            A virtual Physical & Analytical Chemistry lab created by Chemical Engineering students of SRMIST
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Phenol-Water CST")
        st.write("Determine critical solution temperature")
        if st.button("Start CST Experiment", key="phenol"):
            st.session_state.page = "phenol_intro"
    
    with col2:
        st.subheader("Conductometric Titration")
        st.write("Analyze HCl-CH₃COOH mixture")
        if st.button("Start Titration", key="cond"):
            st.session_state.page = "cond_intro"

# Router
page_functions = {
    "home": home,
    "phenol_intro": phenol_intro,
    "phenol_exp1": phenol_exp1,
    "phenol_exp2": phenol_exp2,
    "phenol_exp3": phenol_exp3,
    "phenol_graph": phenol_graph,
    "cond_intro": cond_intro,
    "cond_standardize": cond_standardize,
    "cond_titration": cond_titration,
    "cond_graph": cond_graph,
    "cond_results": cond_results
}

page_functions[st.session_state.page]()
