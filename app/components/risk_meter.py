import streamlit as st

SEVERITY_COLORS = {
    "SAFE": "🟢",
    "LOW": "🟡",
    "MEDIUM": "🟠",
    "HIGH": "🔴",
}

def render_risk_meter(risk_score: float, severity: str):
    icon = SEVERITY_COLORS.get(severity, "⚪")
    st.markdown("**Current Risk**")
    st.markdown(f"### {risk_score * 100:.0f}%")
    st.markdown(f"{icon} **{severity}**")
    st.progress(min(max(risk_score, 0.0), 1.0))
