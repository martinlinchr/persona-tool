import streamlit as st
from components.chat_interface import ChatInterface
from services.chat_service import ChatService

async def render_chat_page():
    """Render the chat interface page."""
    # Initialize services
    chat_service = ChatService(st.session_state.client)
    
    # Create and render the chat interface
    chat_interface = ChatInterface(chat_service)
    await chat_interface.render()
