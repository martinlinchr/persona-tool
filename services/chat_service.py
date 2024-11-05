from typing import List, Dict, Optional
import streamlit as st
from config import OpenAIConfig
from utils.openai_helpers import handle_openai_error

class ChatService:
    def __init__(self, client):
        self.client = client

    @handle_openai_error
    async def create_thread(self):
        """Create a new chat thread."""
        try:
            thread = await self.client.beta.threads.create()
            return thread
        except Exception as e:
            st.error(f"Failed to create thread: {str(e)}")
            return None

    @handle_openai_error
    async def send_message(
        self,
        thread_id: str,
        assistant_id: str,
        message: str,
        file_ids: Optional[List[str]] = None
    ):
        """Send a message and get the assistant's response."""
        try:
            # Add the user's message to the thread
            await self.client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=message,
                file_ids=file_ids or []
            )

            # Run the assistant
            run = await self.client.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=assistant_id
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
            
            return messages.data[0].content[0].text.value

        except Exception as e:
            st.error(f"Failed to process message: {str(e)}")
            return None

    @handle_openai_error
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

    def generate_summary(self, chat_history: List[Dict]) -> str:
        """Generate a summary of the chat history."""
        try:
            summary_prompt = "Please summarize the key points from this conversation:\n\n"
            for msg in chat_history:
                summary_prompt += f"{msg['role']}: {msg['content']}\n"

            response = self.client.chat.completions.create(
                model=OpenAIConfig.DEFAULT_MODEL,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes conversations."},
                    {"role": "user", "content": summary_prompt}
                ]
            )
            
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Failed to generate summary: {str(e)}")
            return "Failed to generate summary"
