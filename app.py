import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set page config
st.set_page_config(
    page_title="Creative Catalysts - Chemistry Lab",
    page_icon=":test_tube:",
    layout="wide"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = "home"
    st.session_state.phenol_data = pd.DataFrame(columns=[
        "Phenol (ml)", "Water (ml)", "% Phenol", 
        "Disappear Temp (°C)", "Reappear Temp (°C)", "Mean Temp (°C)"
    ])
    st.session_state.water_vol = 3.0  # Initialize water volume

# Home Page
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
        st.subheader("Phenol-Water CST Determination")
        st.write("Study phase behavior of partially miscible liquids")
        if st.button("Start Experiment", key="phenol"):
            st.session_state.page = "phenol_intro"
    
    with col2:
        st.subheader("Conductometric Titration")
        st.write("Determine strength of HCl and CH₃COOH in mixture")
        if st.button("Start Experiment", key="cond"):
            st.session_state.page = "cond_intro"

# Phenol-Water Experiment
def phenol_intro():
    st.title("Phenol-Water CST Determination")
    st.write("**Aim:** Determine critical solution temperature")
    
    if st.button("Start Experiment"):
        st.session_state.page = "phenol_exp1"

def phenol_exp1():
    st.title("Add Reagents")
    
    # Fixed the number_input range issue
    water = st.number_input(
        "Water volume (ml)", 
        min_value=3.0, 
        max_value=36.0, 
        value=float(st.session_state.water_vol),  # Ensure float conversion
        step=0.1
    )
    
    phenol = st.number_input(
        "Phenol volume (ml)", 
        min_value=5.0, 
        max_value=10.0, 
        value=5.0,
        step=0.1
    )
    
    if st.button("Heat Mixture"):
        st.session_state.phenol_vol = phenol
        st.session_state.water_vol = water
        st.session_state.page = "phenol_exp2"

def phenol_exp2():
    st.title("Observe Turbidity")
    
    # Calculate percentage
    total = st.session_state.phenol_vol + st.session_state.water_vol
    percent = (st.session_state.phenol_vol / total) * 100
    
    # Simulate realistic temperatures
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
    
    # Store data
    new_row = {
        "Phenol (ml)": st.session_state.phenol_vol,
        "Water (ml)": st.session_state.water_vol,
        "% Phenol": (st.session_state.phenol_vol / 
                    (st.session_state.phenol_vol + st.session_state.water_vol)) * 100,
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
            st.session_state.water_vol += 2
            st.session_state.page = "phenol_exp1"
    else:
        if st.button("Show Graph"):
            st.session_state.page = "phenol_graph"

def phenol_graph():
    st.title("Phase Diagram")
    
    df = st.session_state.phenol_data
    fig, ax = plt.subplots(figsize=(8,5))
    ax.plot(df["% Phenol"], df["Mean Temp (°C)"], 'bo-')
    
    # Mark CST point
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

# Main App Control
if st.session_state.page == "home":
    home()
elif st.session_state.page == "phenol_intro":
    phenol_intro()
elif st.session_state.page == "phenol_exp1":
    phenol_exp1()
elif st.session_state.page == "phenol_exp2":
    phenol_exp2()
elif st.session_state.page == "phenol_exp3":
    phenol_exp3()
elif st.session_state.page == "phenol_graph":
    phenol_graph()
