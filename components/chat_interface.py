import streamlit as st
from services.chat_service import ChatService

class ChatInterface:
    def __init__(self, chat_service: ChatService):
        self.chat_service = chat_service

    async def render(self):
        """Render the chat interface."""
        st.header("Create Persona Based on Your Product/Service")

        # Initialize chat thread if not exists
        if "thread_id" not in st.session_state:
            thread = await self.chat_service.create_thread()
            if thread:
                st.session_state.thread_id = thread.id
                # Send initial message
                initial_msg = "Let's create a persona for your product or service. Tell me about what you sell."
                response = await self.chat_service.send_message(thread.id, initial_msg)
                if response:
                    st.rerun()
            else:
                st.error("Failed to initialize chat. Please refresh the page.")
                return

        # Display chat history
        history = await self.chat_service.get_chat_history(st.session_state.thread_id)
        for message in history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Chat input
        if message := st.chat_input("Type your message here..."):
            response = await self.chat_service.send_message(
                st.session_state.thread_id,
                message
            )
            if response:
                st.rerun()

        # Action buttons
        if st.button("Save Progress"):
            st.session_state.persona_progress = history
            st.success("Progress saved!")
