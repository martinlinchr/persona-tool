import streamlit as st

def render_view_persona_page():
    """Render the persona viewing page."""
    if not st.session_state.get('current_persona'):
        st.warning("No persona selected. Please choose a persona from the sidebar.")
        return

    persona = st.session_state.current_persona
    
    st.title(f"Persona: {persona['name']}")

    # Display persona details in expandable sections
    with st.expander("Background Story", expanded=True):
        st.write(persona['background'])

    with st.expander("Personality Traits"):
        st.write(persona['personality'])

    with st.expander("Areas of Expertise"):
        st.write(persona['expertise'])

    with st.expander("Speech Style"):
        st.write(persona['speech_style'])

    with st.expander("Development Chat History"):
        if 'development_chat' in persona:
            for message in persona['development_chat']:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

    # Add Edit button
    if st.button("Edit Persona"):
        st.session_state.editing_persona = True
        _render_edit_form(persona)

def _render_edit_form(persona):
    """Render the form for editing a persona."""
    with st.form("edit_persona_form"):
        name = st.text_input("Name", value=persona['name'])
        background = st.text_area("Background Story", value=persona['background'])
        personality = st.text_area("Personality Traits", value=persona['personality'])
        expertise = st.text_area("Areas of Expertise", value=persona['expertise'])
        speech_style = st.text_area("Speech Style", value=persona['speech_style'])

        if st.form_submit_button("Save Changes"):
            # Find and update the persona in saved_personas
            for idx, p in enumerate(st.session_state.saved_personas):
                if p['name'] == persona['name']:
                    st.session_state.saved_personas[idx] = {
                        "name": name,
                        "background": background,
                        "personality": personality,
                        "expertise": expertise,
                        "speech_style": speech_style,
                        "development_chat": persona.get('development_chat', [])
                    }
                    st.session_state.current_persona = st.session_state.saved_personas[idx]
                    break

            st.success("Changes saved successfully!")
            st.session_state.editing_persona = False
            st.rerun()
