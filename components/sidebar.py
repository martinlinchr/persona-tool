import streamlit as st
from services.assistant_service import AssistantService
from config import UIConfig

async def render_sidebar():
    """Render the application sidebar."""
    with st.sidebar:
        st.title("Navigation")
        
        # Initialize services
        assistant_service = AssistantService(st.session_state.client)
        
        # Fetch available assistants
        assistants = await assistant_service.list_assistants()
        
        # Create new persona button
        if st.button("Create New Persona", key="create_new"):
            st.session_state.current_page = "create_persona"
            st.rerun()

        # Existing personas section
        if assistants:
            st.subheader("Your Personas")
            
            for assistant in assistants:
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if st.button(
                        assistant.name,
                        key=f"select_{assistant.id}",
                        help="Click to chat with this persona"
                    ):
                        st.session_state.current_persona = assistant
                        st.session_state.current_page = "chat"
                        st.rerun()
                
                with col2:
                    if st.button(
                        "🗑️",
                        key=f"delete_{assistant.id}",
                        help="Delete this persona"
                    ):
                        if await _delete_persona(assistant_service, assistant.id):
                            st.rerun()

async def _delete_persona(assistant_service: AssistantService, assistant_id: str) -> bool:
    """Delete a persona and its associated files."""
    if st.sidebar.button("Confirm Delete"):
        try:
            await assistant_service.delete_assistant(assistant_id)
            st.sidebar.success("Persona deleted successfully!")
            
            # Clear current persona if it was the deleted one
            if (st.session_state.get("current_persona") and 
                st.session_state.current_persona.id == assistant_id):
                st.session_state.current_persona = None
            
            return True
        except Exception as e:
            st.sidebar.error(f"Failed to delete persona: {str(e)}")
            return False
    return False
