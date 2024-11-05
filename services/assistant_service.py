import streamlit as st
from typing import List, Optional
from utils.openai_helpers import handle_openai_error
from config import AppConfig

class AssistantService:
    def __init__(self, client):
        self.client = client

    @handle_openai_error
    async def create_assistant(
        self,
        name: str,
        instructions: str,
        file_ids: Optional[List[str]] = None
    ):
        """Create a new OpenAI assistant with the given configuration."""
        try:
            assistant = await self.client.beta.assistants.create(
                name=name,
                instructions=instructions,
                model=AppConfig.DEFAULT_MODEL,
                file_ids=file_ids or [],
                tools=[{"type": "retrieval"}]
            )
            return assistant
        except Exception as e:
            st.error(f"Failed to create assistant: {str(e)}")
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
    async def delete_assistant(self, assistant_id: str):
        """Delete an assistant by ID."""
        try:
            return await self.client.beta.assistants.delete(assistant_id)
        except Exception as e:
            st.error(f"Failed to delete assistant: {str(e)}")
            return None

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
