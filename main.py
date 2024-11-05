import streamlit as st
import asyncio
from config import AppConfig
from components.sidebar import render_sidebar
from utils.openai_helpers import initialize_openai_client
from pages.create_persona import render_create_persona_page
from pages.chat_with_persona import render_chat_page

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
        st.session_state.persona = None
        st.session_state.assistant = None
        st.session_state.chat_history = []
        st.session_state.current_page = "create_persona"

    # Render sidebar
    await render_sidebar()

    # Render current page
    if st.session_state.current_page == "create_persona":
        await render_create_persona_page()
    elif st.session_state.current_page == "chat":
        await render_chat_page()
    else:
        st.info("👈 Start by creating a new persona in the sidebar!")

if __name__ == "__main__":
    asyncio.run(main())
