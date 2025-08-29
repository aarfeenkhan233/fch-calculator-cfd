import streamlit as st
import math

st.set_page_config(page_title="First Cell Height Calculator (y+)", layout="centered")

st.title("🌊 First Cell Height Calculator (y+) - Near Wall Flow Study")

st.markdown(
    """
    This app calculates the **first cell height** for near wall flow studies using the **y-plus (y⁺) method**.  
    Provide the input parameters below in **SI units**.
    """
)

# --- Input section ---
st.header("🔢 Input Parameters")

def get_input(label, default):
    """Helper function to safely get numeric input from text boxes"""
    val = st.text_input(label, value=str(default))
    try:
        return float(val)
    except ValueError:
        st.error(f"⚠️ Please enter a valid number for {label}")
        return None

Re = get_input("Reynolds Number (Re)", 1e5)
L = get_input("Characteristic Length (m)", 1.0)
rho = get_input("Fluid Density (kg/m³)", 1.225)
mu = get_input("Fluid Dynamic Viscosity (Pa·s)", 1.8e-5)
y_plus = get_input("y-plus Factor (y⁺)", 30.0)

# --- Calculation section ---
if st.button("Calculate"):
    if None not in [Re, L, rho, mu, y_plus]:
        try:
            # Fluid velocity (U)
            U = (Re * mu) / (rho * L)

            # Coefficient of friction (Cf)
            Cf = 0.026 / (Re ** (1/7))

            # Wall shear stress (τw)
            tau_w = ((Cf * rho) * (U ** 2)) / 2

            # Frictional velocity (u_tau)
            u_tau = math.sqrt(tau_w / rho)

            # First cell height (y)
            y = (y_plus * mu) / (u_tau * rho)

            # --- Output section ---
            st.header("📊 Results")
            st.write(f"**Fluid Velocity (U):** {U:.6f} m/s")
            st.write(f"**Coefficient of Friction (Cf):** {Cf:.6e}")
            st.write(f"**Wall Shear Stress (τw):** {tau_w:.6f} N/m²")
            st.write(f"**Frictional Velocity (uτ):** {u_tau:.6f} m/s")
            st.write(f"**First Cell Height (y):** {y:.6e} m")

        except Exception as e:
            st.error(f"⚠️ Error in calculation: {e}")
