import streamlit as st
from components.persona_creator import PersonaCreator
from services.chat_service import ChatService

async def render_create_persona_page():
    """Render the persona creation page."""
    st.title("Create New Persona")
    
    # Initialize chat service
    chat_service = ChatService(st.session_state.client)
    
    # Create and render the persona creator component
    creator = PersonaCreator(chat_service)
    
    # Render the component and handle the result
    persona = await creator.render()
    
    if persona:
        # Show success message with next steps
        st.success("Persona created successfully! You can now start chatting.")
        
        # Add a button to start chatting
        if st.button("Start Chatting"):
            st.session_state.current_page = "chat"
            st.rerun()
