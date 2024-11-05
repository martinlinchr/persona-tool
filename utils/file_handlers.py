import streamlit as st
from config import AppConfig

def validate_file(uploaded_file):
    """Validate uploaded files for size and type."""
    if uploaded_file is None:
        return False
        
    # Check file size
    if uploaded_file.size > AppConfig.MAX_FILE_SIZE:
        st.error(f"File {uploaded_file.name} is too large. Maximum size is {AppConfig.MAX_FILE_SIZE/1024/1024}MB")
        return False
        
    # Check file type
    file_type = uploaded_file.name.split('.')[-1].lower()
    if file_type not in AppConfig.ALLOWED_FILE_TYPES:
        st.error(f"File type .{file_type} is not supported. Allowed types: {', '.join(AppConfig.ALLOWED_FILE_TYPES)}")
        return False
        
    return True

def format_file_size(size_in_bytes):
    """Format file size in bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.1f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.1f} GB"

def get_file_icon(file_type):
    """Return an appropriate icon for the file type."""
    icons = {
        'pdf': '📄',
        'txt': '📝',
        'doc': '📃',
        'docx': '📃',
        'default': '📎'
    }
    return icons.get(file_type.lower(), icons['default'])
