import streamlit as st
from typing import List, Optional
from utils.openai_helpers import handle_openai_error

class AssistantService:
    def __init__(self, client):
        self.client = client

    @handle_openai_error
    async def get_assistant(self, assistant_id: str):
        """Fetch a specific assistant by ID."""
        try:
            assistant = await self.client.beta.assistants.retrieve(assistant_id)
            return assistant
        except Exception as e:
            st.error(f"Failed to fetch assistant: {str(e)}")
            return None

    @handle_openai_error
    async def list_assistants(self):
        """Fetch all available assistants."""
        try:
            assistants = await self.client.beta.assistants.list(
                order="desc",
                limit=100
            )
            return assistants.data
        except Exception as e:
            st.error(f"Failed to fetch assistants: {str(e)}")
            return []

    @handle_openai_error
    async def upload_file(self, file_content, file_name: str):
        """Upload a file to OpenAI."""
        try:
            file = await self.client.files.create(
                file=file_content,
                purpose="assistants"
            )
            return file
        except Exception as e:
            st.error(f"Failed to upload file: {str(e)}")
            return None
