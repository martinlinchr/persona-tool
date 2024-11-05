import streamlit as st
from components.persona_creator import PersonaCreator
from services.assistant_service import AssistantService
from services.chat_service import ChatService

PERSONA_BUILDER_ID = "asst_IQgwDHzRMhnidyPJ2BQRJ3"

async def render_create_persona_page():
    """Render the persona creation page."""
    st.title("Create New Persona")
    
    # Initialize services
    assistant_service = AssistantService(st.session_state.client)
    chat_service = ChatService(st.session_state.client)
    
    # Get the Persona Builder Assistant
    if "persona_builder" not in st.session_state:
        with st.spinner("Loading Persona Builder..."):
            builder = await assistant_service.get_assistant(PERSONA_BUILDER_ID)
            if builder:
                st.session_state.persona_builder = builder
            else:
                st.error("Failed to load Persona Builder Assistant")
                return
    
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
