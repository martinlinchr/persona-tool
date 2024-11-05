import streamlit as st
from services.assistant_service import AssistantService

async def render_sidebar():
    """Render the application sidebar."""
    with st.sidebar:
        st.title("Navigation")

        # Create new persona button
        if st.button("Create New Persona", key="create_new"):
            st.session_state.current_page = "create_persona"
            # Clear any existing chat/persona state
            st.session_state.pop('thread_id', None)
            st.session_state.pop('chat_history', None)
            st.session_state.pop('current_persona', None)
            st.rerun()

        # Display saved personas
        if 'saved_personas' in st.session_state and st.session_state.saved_personas:
            st.subheader("Your Personas")
            
            for idx, persona in enumerate(st.session_state.saved_personas):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    if st.button(
                        persona['name'],
                        key=f"select_{idx}",
                        help=f"View {persona['name']}'s details"
                    ):
                        st.session_state.current_persona = persona
                        st.session_state.current_page = "view_persona"
                        st.rerun()
                
                with col2:
                    if st.button(
                        "🗑️",
                        key=f"delete_{idx}",
                        help=f"Delete {persona['name']}"
                    ):
                        # Add confirmation
                        if st.button(f"Confirm delete {persona['name']}", key=f"confirm_{idx}"):
                            st.session_state.saved_personas.pop(idx)
                            st.session_state.pop('current_persona', None)
                            st.success(f"Deleted {persona['name']}")
                            st.rerun()
