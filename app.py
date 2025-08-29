import streamlit as st
import math

st.set_page_config(page_title="First Cell Height Calculator (y+)", layout="centered")

st.title("🌫 First Cell Height Calculator (y+) - for External, Near Wall Flows")

st.markdown(
    """
    This app calculates the **first cell height** for near wall flow studies using the **y-plus (y⁺) method**.  
    Provide the input parameters below in **SI units**.

    Formulation taken from  Frank M. White's Fluid Mechanics 5th edition, page 467.
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
            U_tau = math.sqrt(tau_w / rho)

            # First cell height (y)
            Δs = (y_plus * mu) / (U_tau * rho)

            # --- Output section ---
            st.header("📊 Results")
            st.write(f"**Fluid Velocity (U):** {U:.6f} m/s")
            st.write(f"**Coefficient of Friction (Cf):** {Cf:.6e}")
            st.write(f"**Wall Shear Stress (τw):** {tau_w:.6f} N/m²")
            st.write(f"**Frictional Velocity (uτ):** {U_tau:.6f} m/s")

            # 🔴 Highlight First Cell Height
            st.markdown(
                f"""
                <div style="background-color:#f8f9fa;
                            border-radius:12px;
                            padding:20px;
                            margin-top:20px;
                            border:2px solid #ff4b4b;">
                    <h2 style="color:#ff4b4b; text-align:center;">
                        📏 First Cell Height (Δs): {Δs:.6e} m
                    </h2>
                </div>
                """,
                unsafe_allow_html=True
            )

        except Exception as e:
            st.error(f"⚠️ Error in calculation: {e}")
