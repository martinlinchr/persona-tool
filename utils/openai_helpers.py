import functools
import streamlit as st
from openai import OpenAI, AsyncOpenAI
from openai.types.error import APIError
from config import OpenAIConfig

def initialize_openai_client() -> AsyncOpenAI:
    """Initialize the OpenAI client with credentials from Streamlit secrets."""
    try:
        client = AsyncOpenAI(
            api_key=OpenAIConfig.api_key,
            organization=OpenAIConfig.organization
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
        except APIError as e:
            if e.code == "rate_limit_exceeded":
                st.error("Rate limit exceeded. Please try again in a few moments.")
            elif e.code == "invalid_api_key":
                st.error("Invalid API key. Please check your OpenAI API key.")
            else:
                st.error(f"OpenAI API error: {str(e)}")
            return None
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            return None
    return wrapper
