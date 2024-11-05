import streamlit as st
from typing import Optional, List
from services.chat_service import ChatService

class PersonaCreator:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    async def render(self):
        """Render the persona creation interface."""
        st.header("Create New Persona")
        
        # Initialize chat history if not exists
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
            # Add initial message from assistant
            initial_response = await self.chat_service.chat_with_persona_builder(
                "Help me create a new persona."
            )
            await self.chat_service.save_chat_history(
                "Help me create a new persona.",
                initial_response
            )

        # Display chat history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if message := st.chat_input("Describe your persona ideas..."):
            response = await self.chat_service.chat_with_persona_builder(message)
            await self.chat_service.save_chat_history(message, response)
            st.rerun()

        # Show form when ready
        if st.button("Ready to Save Persona"):
            st.session_state.show_form = True

        if st.session_state.get('show_form', False):
            with st.form("persona_form"):
                st.subheader("Save Your Persona")
                
                name = st.text_input("Persona Name")
                background = st.text_area("Background Story")
                personality = st.text_area("Personality Traits")
                expertise = st.text_area("Areas of Expertise")
                speech_style = st.text_area("Speech Style")

                # File upload for additional context
                uploaded_files = st.file_uploader(
                    "Upload Reference Documents (Optional)",
                    accept_multiple_files=True,
                    type=["pdf", "txt", "doc", "docx"]
                )

                if st.form_submit_button("Save Persona"):
                    if not name or not background:
                        st.error("Please provide at least a name and background.")
                        return None

                    persona = {
                        "name": name,
                        "background": background,
                        "personality": personality,
                        "expertise": expertise,
                        "speech_style": speech_style,
                        "chat_history": st.session_state.chat_history,
                        "files": [f.name for f in (uploaded_files or [])]
                    }

                    # Store the persona in session state
                    st.session_state.current_persona = persona
                    st.success(f"Persona '{name}' saved successfully!")
                    
                    # Clear chat history and form
                    st.session_state.chat_history = []
                    st.session_state.show_form = False
                    
                    return persona

        return None
