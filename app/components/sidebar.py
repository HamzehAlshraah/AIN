import streamlit as st


def render_sidebar():
    with st.sidebar:

        # =============================================
        # شعار AIN
        # =============================================

        st.image(
            "/workspaces/AIN/app/logo AIN.png",
            use_container_width=True,
        )

        st.markdown(
            """
            <div style="
                text-align: center;
                font-size: 18px;
                font-weight: 800;
                margin-top: 5px;
                margin-bottom: 15px;
                direction: rtl;
            ">
                نظام حماية الأطفال AIN
            </div>
            """,
            unsafe_allow_html=True,
        )