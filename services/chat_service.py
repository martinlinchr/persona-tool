from typing import List, Dict, Optional
import streamlit as st
from openai import AsyncOpenAI

PERSONA_BUILDER_ID = "asst_IQgwDHzRMhnidyPJ2BQRJ3"

class ChatService:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def create_thread(self):
        """Create a new chat thread."""
        try:
            thread = await self.client.beta.threads.create()
            return thread
        except Exception as e:
            st.error(f"Failed to create thread: {str(e)}")
            return None

    async def send_message(self, thread_id: str, message: str):
        """Send a message and get the assistant's response."""
        try:
            # Add the user's message to the thread
            await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message
            )

            # Run the assistant
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=PERSONA_BUILDER_ID
            )

            # Wait for the run to complete
            while True:
                run_status = await self.client.beta.threads.runs.retrieve(
                    thread_id=thread_id,
                    run_id=run.id
                )
                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    raise Exception(f"Run failed with status: {run_status.status}")

            # Get the messages
            messages = await self.client.beta.threads.messages.list(
                thread_id=thread_id
            )
            
            if messages.data:
                return messages.data[0].content[0].text.value
            return None

        except Exception as e:
            st.error(f"Failed to process message: {str(e)}")
            return None

    async def get_chat_history(self, thread_id: str) -> List[Dict]:
        """Retrieve the chat history for a thread."""
        try:
            messages = await self.client.beta.threads.messages.list(
                thread_id=thread_id
            )
            
            history = []
            for msg in reversed(messages.data):
                history.append({
                    "role": msg.role,
                    "content": msg.content[0].text.value
                })
            
            return history
        except Exception as e:
            st.error(f"Failed to fetch chat history: {str(e)}")
            return []
