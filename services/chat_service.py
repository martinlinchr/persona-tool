from typing import List, Dict, Optional
import streamlit as st
from openai import AsyncOpenAI

class ChatService:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def chat_with_persona_builder(self, message: str) -> str:
        """Chat with the persona builder using direct chat completions."""
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a specialized AI assistant designed to help create detailed and consistent personas. 
                        Your role is to guide users through the persona creation process, helping them develop:
                        1. Rich background stories
                        2. Consistent personality traits
                        3. Clear speech patterns and mannerisms
                        4. Well-defined areas of expertise
                        5. Authentic character voice

                        Guide users by asking probing questions and making suggestions. Be creative and detailed.
                        If users are unsure, provide examples and ideas."""
                    },
                    {"role": "user", "content": message}
                ],
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error in chat: {str(e)}")
            return "I apologize, but I encountered an error. Please try again."

    async def save_chat_history(self, message: str, response: str):
        """Save chat history to session state."""
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        st.session_state.chat_history.extend([
            {"role": "user", "content": message},
            {"role": "assistant", "content": response}
        ])
