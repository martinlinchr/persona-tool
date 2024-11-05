import streamlit as st
from typing import Optional, List
from services.chat_service import ChatService

class PersonaCreator:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    async def render(self):
        """Render the persona creation interface."""
        st.header("Persona Generator")
        st.markdown("""
        Let our AI help you create the perfect persona for your product or service. 
        Just tell us what you're selling, and we'll help develop a detailed persona.
        """)

        # Initialize chat thread if not exists
        if "thread_id" not in st.session_state:
            thread = await self.chat_service.create_thread()
            if thread:
                st.session_state.thread_id = thread.id
                # Send initial message
                response = await self.chat_service.send_message(
                    thread.id,
                    "I'm here to help create a persona for your product or service. "
                    "To get started, please tell me what product or service you're selling?"
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
        if message := st.chat_input("Describe your product or service..."):
            with st.spinner("Generating response..."):
                response = await self.chat_service.send_message(
                    st.session_state.thread_id,
                    message
                )
                if response:
                    st.rerun()

        # Only show the save button after some conversation has happened
        if history and len(history) > 2:  # After at least one exchange
            if st.button("Save Generated Persona"):
                st.session_state.show_form = True

        if st.session_state.get('show_form', False):
            with st.form("persona_form"):
                st.subheader("Save Generated Persona")
                
                # Extract the last assistant message for context
                last_assistant_message = next(
                    (msg["content"] for msg in reversed(history) 
                     if msg["role"] == "assistant"), 
                    ""
                )
                
                st.markdown("Review and edit the generated persona details before saving:")
                
                name = st.text_input(
                    "Persona Name",
                    help="The name suggested by the AI for your persona"
                )
                background = st.text_area(
                    "Background Story",
                    help="The background story developed during our conversation"
                )
                personality = st.text_area(
                    "Personality Traits",
                    help="Key personality traits identified for your persona"
                )
                expertise = st.text_area(
                    "Areas of Expertise",
                    help="Relevant expertise for your product/service"
                )
                speech_style = st.text_area(
                    "Speech Style",
                    help="How this persona communicates"
                )

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
