class AppConfig:
    """Application configuration settings."""
    APP_NAME = "Persona Creator & Chat"
    PERSONA_STORAGE_KEY = "current_persona"
    ASSISTANT_STORAGE_KEY = "current_assistant"
    MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
    ALLOWED_FILE_TYPES = ["pdf", "txt", "doc", "docx"]
    
    # Model configurations
    DEFAULT_MODEL = "gpt-4-turbo-preview"
    ALLOWED_MODELS = ["gpt-4-turbo-preview", "gpt-4", "gpt-3.5-turbo"]
    
    # Assistant configurations
    DEFAULT_ASSISTANT_NAME = "Persona Assistant"
    DEFAULT_ASSISTANT_INSTRUCTIONS = """
    You are a persona creation and roleplay assistant. Your role is to help users create 
    detailed, consistent personas and then embody those personas in conversation.
    """

class UIConfig:
    """UI-specific configuration settings."""
    SIDEBAR_WIDTH = 300
    MAX_CHAT_MESSAGES = 50
    THEME_COLOR = "#FF4B4B"
