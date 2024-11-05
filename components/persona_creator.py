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
        Our AI Persona Generator will create the perfect persona for your product or service. 
        Just start by telling us what you're selling.
        """)

        # Only initialize chat when user provides first input
        if not st.session_state.get('thread_id'):
            message = st.chat_input("What product or service are you selling?")
            if message:  # Only start the process when user inputs something
                thread = await self.chat_service.create_thread()
                if thread:
                    st.session_state.thread_id = thread.id
                    response = await self.chat_service.send_message(
                        thread.id,
                        message
                    )
                    if response:
                        st.rerun()
                else:
                    st.error("Failed to initialize chat. Please refresh the page.")
                    return
        else:
            # Continue existing conversation
            history = await self.chat_service.get_chat_history(st.session_state.thread_id)
            for message in history:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            # Chat input for continued conversation
            if message := st.chat_input("Respond to AI..."):
                with st.spinner("AI is thinking..."):
                    response = await self.chat_service.send_message(
                        st.session_state.thread_id,
                        message
                    )
                    if response:
                        st.rerun()

            # Only show the save button after persona has been generated
            if len(history) > 2 and st.button("Save Generated Persona"):
                # Here we'll let the Assistant compile the persona details
                compile_message = """Please compile all the persona details we've discussed into a structured format with the following sections:
                - Name
                - Background Story
                - Personality Traits
                - Areas of Expertise
                - Speech Style"""
                
                with st.spinner("Compiling persona details..."):
                    response = await self.chat_service.send_message(
                        st.session_state.thread_id,
                        compile_message
                    )
                    if response:
                        st.session_state.show_form = True
                        st.session_state.compiled_persona = response
                        st.rerun()

        if st.session_state.get('show_form', False):
            with st.form("persona_form"):
                st.subheader("Review Generated Persona")
                st.markdown("The AI has generated the following persona. Review and edit if needed:")
                
                st.markdown(st.session_state.compiled_persona)
                
                if st.form_submit_button("Confirm and Save Persona"):
                    # Create the persona
                    history = await self.chat_service.get_chat_history(st.session_state.thread_id)
                    
                    # Initialize saved_personas if it doesn't exist
                    if 'saved_personas' not in st.session_state:
                        st.session_state.saved_personas = []

                    # Add the new persona to the list
                    st.session_state.saved_personas.append({
                        "compiled_details": st.session_state.compiled_persona,
                        "development_chat": history
                    })

                    # Clear current session
                    st.session_state.pop('thread_id', None)
                    st.session_state.pop('show_form', None)
                    st.session_state.pop('compiled_persona', None)

                    st.success("Persona saved successfully!")
                    st.rerun()

        return None
