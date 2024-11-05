import streamlit as st
from typing import Optional, List
from services.assistant_service import AssistantService
from services.chat_service import ChatService
from utils.file_handlers import validate_file
from config import AppConfig

PERSONA_BUILDER_ID = "asst_IQgwDHzRMhnidyPJ2BQRJ3"

class PersonaCreator:
    def __init__(self, assistant_service: AssistantService, chat_service: ChatService):
        self.assistant_service = assistant_service
        self.chat_service = chat_service

    async def render(self):
        """Render the persona creation interface."""
        st.header("Create New Persona")

        # Initialize chat with Persona Builder if not already done
        if "builder_thread_id" not in st.session_state:
            thread = await self.chat_service.create_thread()
            if thread:
                st.session_state.builder_thread_id = thread.id
                st.session_state.builder_messages = []
            else:
                st.error("Failed to initialize chat with Persona Builder")
                return

        # Display chat history with Persona Builder
        for message in st.session_state.get("builder_messages", []):
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input for Persona Builder
        if message := st.chat_input("Chat with Persona Builder..."):
            await self._handle_builder_chat(message)

        # Only show the form once the user indicates they're ready to create the persona
        if st.session_state.get("ready_for_creation", False):
            await self._render_persona_form()

        # Button to start persona creation form
        if not st.session_state.get("ready_for_creation", False):
            if st.button("Ready to Create Persona"):
                st.session_state.ready_for_creation = True
                st.rerun()

    async def _handle_builder_chat(self, message: str):
        """Handle chat interaction with the Persona Builder."""
        with st.spinner("Processing..."):
            response = await self.chat_service.send_message(
                thread_id=st.session_state.builder_thread_id,
                assistant_id=PERSONA_BUILDER_ID,
                message=message
            )

            if response:
                # Update chat history
                history = await self.chat_service.get_chat_history(
                    st.session_state.builder_thread_id
                )
                st.session_state.builder_messages = history
                st.rerun()

    async def _render_persona_form(self):
        """Render the form for final persona creation."""
        with st.form("persona_form"):
            st.subheader("Finalize Your Persona")
            
            persona_name = st.text_input(
                "Persona Name",
                help="Enter a name for your persona"
            )
            
            background = st.text_area(
                "Background Story",
                help="Describe the background and history of your persona"
            )
            
            personality = st.text_area(
                "Personality Traits",
                help="Describe key personality traits, behaviors, and mannerisms"
            )
            
            expertise = st.text_area(
                "Areas of Expertise",
                help="List the persona's knowledge domains and expertise"
            )
            
            speech_style = st.text_area(
                "Speech Style",
                help="Describe how the persona speaks and communicates"
            )

            # File Upload Section
            uploaded_files = st.file_uploader(
                "Upload Reference Documents",
                accept_multiple_files=True,
                type=AppConfig.ALLOWED_FILE_TYPES,
                help="Upload documents to provide additional context for your persona"
            )

            if st.form_submit_button("Save Persona"):
                return await self._save_persona(
                    persona_name,
                    background,
                    personality,
                    expertise,
                    speech_style,
                    uploaded_files
                )

    async def _save_persona(
        self,
        name: str,
        background: str,
        personality: str,
        expertise: str,
        speech_style: str,
        files: Optional[List] = None
    ):
        """Save the created persona details."""
        if not name or not background:
            st.error("Please provide at least a name and background for your persona.")
            return None

        # Create a persona object to store in session state
        persona = {
            "name": name,
            "background": background,
            "personality": personality,
            "expertise": expertise,
            "speech_style": speech_style,
            "files": [],  # List to store file information
            "chat_history": await self.chat_service.get_chat_history(
                st.session_state.builder_thread_id
            )
        }

        # Handle file uploads if any
        if files:
            for file in files:
                if validate_file(file):
                    uploaded_file = await self.assistant_service.upload_file(
                        file.getvalue(),
                        file.name
                    )
                    if uploaded_file:
                        persona["files"].append({
                            "name": file.name,
                            "id": uploaded_file.id
                        })

        # Clear the builder chat state for next persona
        st.session_state.pop("builder_thread_id", None)
        st.session_state.pop("builder_messages", None)
        st.session_state.pop("ready_for_creation", None)

        return persona
