import streamlit as st
from typing import Optional, List
from services.assistant_service import AssistantService
from utils.file_handlers import validate_file
from config import OpenAIConfig, AppConfig

class PersonaCreator:
    def __init__(self, assistant_service: AssistantService):
        self.assistant_service = assistant_service

    def render(self):
        """Render the persona creation interface."""
        st.header("Create New Persona")

        # Basic Persona Information
        with st.form("persona_form"):
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

            submit_button = st.form_submit_button("Create Persona")

            if submit_button:
                return self._handle_persona_creation(
                    persona_name,
                    background,
                    personality,
                    expertise,
                    speech_style,
                    uploaded_files
                )

        return None

    async def _handle_persona_creation(
        self,
        name: str,
        background: str,
        personality: str,
        expertise: str,
        speech_style: str,
        files: Optional[List] = None
    ):
        """Handle the creation of a new persona."""
        if not name or not background:
            st.error("Please provide at least a name and background for your persona.")
            return None

        with st.spinner("Creating your persona..."):
            # Upload files if provided
            file_ids = []
            if files:
                for file in files:
                    if validate_file(file):
                        uploaded_file = await self.assistant_service.upload_file(
                            file.getvalue(),
                            file.name
                        )
                        if uploaded_file:
                            file_ids.append(uploaded_file.id)

            # Create the instruction set for the assistant
            instructions = f"""
            You are now embodying a persona with the following characteristics:

            Name: {name}

            Background:
            {background}

            Personality Traits:
            {personality}

            Areas of Expertise:
            {expertise}

            Speech Style:
            {speech_style}

            Instructions:
            1. Always stay in character and respond as this persona would.
            2. Use the speech style and mannerisms described above.
            3. Draw from the background and expertise provided.
            4. If asked something outside your expertise, acknowledge it while staying in character.
            5. Maintain consistent personality traits throughout interactions.
            """

            # Create the assistant
            assistant = await self.assistant_service.create_assistant(
                name=name,
                instructions=instructions,
                file_ids=file_ids
            )

            if assistant:
                st.success(f"Persona '{name}' created successfully!")
                return assistant
            else:
                st.error("Failed to create persona. Please try again.")
                return None
