from typing import List, Dict, Optional
import streamlit as st
from openai import AsyncOpenAI

class ChatService:
    def __init__(self, client: AsyncOpenAI):
        self.client = client

    async def create_thread(self):
        """Initialize a new conversation thread."""
        # In our simplified version, we just need to reset the chat history
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        return {"id": "simple_thread"}  # Dummy thread object

    async def chat_with_persona_builder(self, message: str, context: str = "") -> str:
        """Chat with the persona builder using direct chat completions."""
        try:
            # Initialize system message with focus on product/service
            system_message = """You are a specialized AI assistant designed to create detailed personas based on products or services. 
            Your first task is to understand the product/service thoroughly.
            Then, help create a persona that would be ideal for marketing, selling, or representing this product/service.
            
            Your process should:
            1. First understand the product/service details
            2. Ask relevant questions about target market, price point, unique features
            3. Based on the answers, suggest and develop a persona that would be perfect for this product/service
            4. Help flesh out the persona's:
               - Background that relates to the product/service
               - Relevant expertise and experiences
               - Communication style that would resonate with the target market
               - Personality traits that align with the brand
            
            Be collaborative and creative while keeping the focus on developing a persona that makes sense for the product/service."""

            messages = [
                {"role": "system", "content": system_message}
            ]

            # Add context if it exists
            if context:
                messages.append({"role": "assistant", "content": context})

            # Add chat history from session state
            for msg in st.session_state.get('chat_history', []):
                messages.append({"role": msg["role"], "content": msg["content"]})

            # Add the current message
            messages.append({"role": "user", "content": message})

            response = await self.client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=messages,
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
