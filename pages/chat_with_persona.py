import streamlit as st
from components.chat_interface import ChatInterface
from services.chat_service import ChatService

async def render_chat_page():
    """Render the chat interface page."""
    if not st.session_state.get("current_persona"):
        st.warning("Please select or create a persona first!")
        if st.button("Create New Persona"):
            st.session_state.current_page = "create_persona"
            st.rerun()
        return

    # Initialize services
    chat_service = ChatService(st.session_state.client)
    
    # Create and render the chat interface
    chat_interface = ChatInterface(chat_service)
    
    # Display persona info in an expander
    with st.expander("Current Persona Info", expanded=False):
        st.write(f"**Name:** {st.session_state.current_persona.name}")
        st.write("**Instructions:**")
        st.text(st.session_state.current_persona.instructions)
        
        if hasattr(st.session_state.current_persona, "file_ids") and st.session_state.current_persona.file_ids:
            st.write("**Associated Files:**")
            for file_id in st.session_state.current_persona.file_ids:
                st.write(f"- File ID: {file_id}")
    
    # Render the chat interface
    await chat_interface.render(
        assistant_id=st.session_state.current_persona.id,
        persona_name=st.session_state.current_persona.name
    )
