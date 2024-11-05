import streamlit as st
import asyncio
from config import AppConfig
from components.sidebar import render_sidebar
from utils.openai_helpers import initialize_openai_client
from pages.create_persona import render_create_persona_page
from pages.view_persona import render_view_persona_page

async def main():
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
        st.session_state.current_page = "create_persona"
        if 'saved_personas' not in st.session_state:
            st.session_state.saved_personas = []

    # Render sidebar
    await render_sidebar()

    # Render current page
    if st.session_state.current_page == "create_persona":
        await render_create_persona_page()
    elif st.session_state.current_page == "view_persona":
        render_view_persona_page()

if __name__ == "__main__":
    asyncio.run(main())
