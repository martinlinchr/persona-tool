import streamlit as st
from components.persona_creator import PersonaCreator
from services.assistant_service import AssistantService
from config import AppConfig

async def render_create_persona_page():
    """Render the persona creation page."""
    st.title("Create New Persona")
    
    # Initialize services
    assistant_service = AssistantService(st.session_state.client)
    
    # Check if we have the persona creation assistant in session state
    if "persona_creator_assistant" not in st.session_state:
        with st.spinner("Initializing persona creation assistant..."):
            # Try to find existing persona creator assistant
            assistants = await assistant_service.list_assistants()
            creator_assistant = next(
                (a for a in assistants if a.name == "Persona Creator Assistant"),
                None
            )
            
            if not creator_assistant:
                # Create the persona creator assistant if it doesn't exist
                creator_assistant = await assistant_service.create_assistant(
                    name="Persona Creator Assistant",
                    instructions="""You are a specialized AI assistant designed to help create detailed and consistent personas. 
                    Your role is to guide users through the persona creation process, helping them develop:
                    1. Rich background stories
                    2. Consistent personality traits
                    3. Clear speech patterns and mannerisms
                    4. Well-defined areas of expertise
                    5. Authentic character voice

                    For each aspect of the persona, you should:
                    - Ask probing questions to elicit more detail
                    - Suggest improvements and additions
                    - Ensure internal consistency
                    - Help develop unique and memorable characteristics
                    - Identify potential conflicts or inconsistencies
                    
                    Always maintain a helpful and encouraging tone, while ensuring the personas created are:
                    - Well-rounded and believable
                    - Internally consistent
                    - Detailed enough for meaningful interaction
                    - Appropriate for their intended use
                    """,
                    model=AppConfig.DEFAULT_MODEL
                )
            
            if creator_assistant:
                st.session_state.persona_creator_assistant = creator_assistant
            else:
                st.error("Failed to initialize persona creator assistant")
                return
    
    # Create and render the persona creator component
    creator = PersonaCreator(assistant_service)
    
    # Render the component and handle the result
    persona = await creator.render()
    
    if persona:
        # Store the created persona in session state
        st.session_state.current_persona = persona
        
        # Show success message with next steps
        st.success("Persona created successfully! You can now start chatting.")
        
        # Add a button to start chatting
        if st.button("Start Chatting"):
            st.session_state.current_page = "chat"
            st.rerun()
