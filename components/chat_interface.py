import streamlit as st
from typing import Optional
import pandas as pd
from services.chat_service import ChatService
from config import UIConfig

class ChatInterface:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service
        
        # Initialize session state for chat
        if "thread_id" not in st.session_state:
            self._initialize_chat()

    async def _initialize_chat(self):
        """Initialize a new chat thread."""
        thread = await self.chat_service.create_thread()
        if thread:
            st.session_state.thread_id = thread.id
        else:
            st.error("Failed to initialize chat. Please refresh the page.")

    def render(self, assistant_id: str, persona_name: str):
        """Render the chat interface."""
        st.header(f"Chat with {persona_name}")

        # Display chat history
        self._display_chat_history()

        # Chat input
        with st.container():
            message = st.chat_input("Type your message here...")
            if message:
                self._handle_message(message, assistant_id)

        # Action buttons
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Download Chat History"):
                self._download_chat_history()
        with col2:
            if st.button("Get Summary"):
                self._generate_and_display_summary()

    async def _handle_message(self, message: str, assistant_id: str):
        """Handle sending and receiving messages."""
        if not message.strip():
            return

        with st.spinner("Processing..."):
            response = await self.chat_service.send_message(
                thread_id=st.session_state.thread_id,
                assistant_id=assistant_id,
                message=message
            )

            if response:
                # Update chat history in session state
                st.session_state.chat_history = await self.chat_service.get_chat_history(
                    st.session_state.thread_id
                )
                st.rerun()

    def _display_chat_history(self):
        """Display the chat history."""
        if not st.session_state.get("chat_history"):
            return

        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    def _download_chat_history(self):
        """Download chat history as CSV."""
        if not st.session_state.get("chat_history"):
            st.warning("No chat history to download.")
            return

        # Convert chat history to DataFrame
        df = pd.DataFrame(st.session_state.chat_history)
        
        # Convert DataFrame to CSV
        csv = df.to_csv(index=False)
        
        # Create download button
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="chat_history.csv",
            mime="text/csv"
        )

    async def _generate_and_display_summary(self):
        """Generate and display a summary of the chat."""
        if not st.session_state.get("chat_history"):
            st.warning("No chat history to summarize.")
            return

        with st.spinner("Generating summary..."):
            summary = await self.chat_service.generate_summary(
                st.session_state.chat_history
            )
            
            if summary:
                st.info("Chat Summary:")
                st.write(summary)
                
                # Offer summary download
                st.download_button(
                    label="Download Summary",
                    data=summary,
                    file_name="chat_summary.txt",
                    mime="text/plain"
                )