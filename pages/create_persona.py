import streamlit as st
from components.persona_creator import PersonaCreator
from services.assistant_service import AssistantService
from services.chat_service import ChatService

async def render_create_persona_page():
    """Render the persona creation page."""
    st.title("Create New Persona")
    
    # Initialize services
    assistant_service = AssistantService(st.session_state.client)
    chat_service = ChatService(st.session_state.client)
    
    # Create and render the persona creator component
    creator = PersonaCreator(assistant_service, chat_service)
    
    # Render the component and handle the result
    persona = await creator.render()
    
    if persona:
        # Store the created persona in session state
        st.session_state.current_persona = persona
        
        # Show success message with next steps
        st.success("Persona created successfully! You can now start chatting.")
        
        # Add a button to start chatting
        if st.button("Start Chatting"):
            st.session_state.current_page = "chat"
            st.rerun()
