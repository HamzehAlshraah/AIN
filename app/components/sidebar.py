from pathlib import Path
import streamlit as st


def render_sidebar():
    with st.sidebar:

        # =============================================
        # شعار AIN
        # =============================================

        logo_path = (
            Path(__file__).resolve().parent.parent
            / "logo AIN.png"
        )

        if logo_path.exists():
            st.image(
                str(logo_path),
                use_container_width=True,
            )
        else:
            st.warning("⚠️ لم يتم العثور على شعار AIN")

        st.markdown(
            """
            <div style="
                text-align: center;
                font-size: 18px;
                font-weight: 800;
                margin-top: 5px;
                margin-bottom: 15px;
            ">
                AIN
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.divider()

        # =============================================
        # Navigation
        # =============================================

        