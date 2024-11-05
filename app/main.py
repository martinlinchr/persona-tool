import streamlit as st
from app.config import AppConfig, UIConfig
from app.components.sidebar import render_sidebar
from app.utils.openai_helpers import initialize_openai_client

def main():
    st.set_page_config(
        page_title=AppConfig.APP_NAME,
        page_icon="🎭",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session state
    if "initialized" not in st.session_state:
        st.session_state.initialized = True
        st.session_state.client = initialize_openai_client()
        st.session_state.persona = None
        st.session_state.assistant = None
        st.session_state.chat_history = []

    # Render sidebar
    render_sidebar()

    # Main content area
    st.title(AppConfig.APP_NAME)
    
    if not st.session_state.persona:
        st.info("👈 Start by creating a new persona in the sidebar!")
    
if __name__ == "__main__":
    main()
