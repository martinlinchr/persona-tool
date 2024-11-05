import streamlit as st
from components.persona_creator import PersonaCreator
from services.assistant_service import AssistantService

async def render_create_persona_page():
    """Render the persona creation page."""
    st.session_state.current_page = "create_persona"
    
    # Initialize services
    assistant_service = AssistantService(st.session_state.client)
    
    # Create and render the persona creator component
    creator = PersonaCreator(assistant_service)
    
    # Render the component and handle the result
    assistant = await creator.render()
    
    if assistant:
        # Store the created assistant in session state
        st.session_state.current_persona = assistant
        
        # Show success message with next steps
        st.success("Persona created successfully! You can now start chatting.")
        
        # Add a button to start chatting
        if st.button("Start Chatting"):
            st.session_state.current_page = "chat"
            st.rerun()
