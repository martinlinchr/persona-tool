import streamlit as st
from typing import Optional, List
from services.chat_service import ChatService

class PersonaCreator:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    async def render(self):
        """Render the persona creation interface."""
        st.header("Create Persona Based on Your Product/Service")

        # Initialize chat thread if not exists
        if "thread_id" not in st.session_state:
            thread = await self.chat_service.create_thread()
            if thread:
                st.session_state.thread_id = thread.id
                # Send initial message
                response = await self.chat_service.send_message(
                    thread.id,
                    "Tell me about your product or service, and I'll help create a perfect persona for it."
                )
            else:
                st.error("Failed to initialize chat. Please refresh the page.")
                return

        # Display chat history
        history = await self.chat_service.get_chat_history(st.session_state.thread_id)
        for message in history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if message := st.chat_input("Tell me about your product/service..."):
            response = await self.chat_service.send_message(
                st.session_state.thread_id,
                message
            )
            if response:
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

                if st.form_submit_button("Save Persona"):
                    if not name or not background:
                        st.error("Please provide at least a name and background.")
                        return None

                    # Create the persona
                    persona = {
                        "name": name,
                        "background": background,
                        "personality": personality,
                        "expertise": expertise,
                        "speech_style": speech_style,
                        "development_chat": history
                    }

                    # Initialize saved_personas if it doesn't exist
                    if 'saved_personas' not in st.session_state:
                        st.session_state.saved_personas = []

                    # Add the new persona to the list
                    st.session_state.saved_personas.append(persona)

                    # Clear current session
                    st.session_state.pop('thread_id', None)
                    st.session_state.pop('show_form', None)

                    st.success(f"Persona '{name}' saved successfully!")
                    return persona

        return None
