import functools
import streamlit as st
from openai import AsyncOpenAI

def initialize_openai_client() -> AsyncOpenAI:
    """Initialize the OpenAI client with credentials from Streamlit secrets."""
    try:
        client = AsyncOpenAI(
            api_key=st.secrets["OPENAI_API_KEY"],
            organization=st.secrets.get("OPENAI_ORGANIZATION", None)
        )
        return client
    except Exception as e:
        st.error(f"Failed to initialize OpenAI client: {str(e)}")
        st.stop()

def handle_openai_error(func):
    """Decorator to handle OpenAI API errors."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            error_message = str(e).lower()
            if "rate_limit" in error_message:
                st.error("Rate limit exceeded. Please try again in a few moments.")
            elif "invalid_api_key" in error_message:
                st.error("Invalid API key. Please check your OpenAI API key.")
            else:
                st.error(f"OpenAI API error: {str(e)}")
            return None
    return wrapper
