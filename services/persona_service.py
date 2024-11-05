from typing import Optional, Dict, List
from services.assistant_service import AssistantService
from utils.openai_helpers import handle_openai_error
import streamlit as st

class PersonaService:
    def __init__(self, assistant_service: AssistantService):
        self.assistant_service = assistant_service

    @handle_openai_error
    async def create_persona(
        self,
        name: str,
        background: str,
        personality: str,
        expertise: str,
        speech_style: str,
        file_ids: Optional[List[str]] = None
    ) -> Optional[Dict]:
        """Create a new persona using the Assistant API."""
        instructions = self._generate_persona_instructions(
            name,
            background,
            personality,
            expertise,
            speech_style
        )

        assistant = await self.assistant_service.create_assistant(
            name=name,
            instructions=instructions,
            file_ids=file_ids
        )

        return assistant

    @handle_openai_error
    async def get_all_personas(self) -> List[Dict]:
        """Get all created personas."""
        return await self.assistant_service.list_assistants()

    @handle_openai_error
    async def delete_persona(self, persona_id: str) -> bool:
        """Delete a persona."""
        result = await self.assistant_service.delete_assistant(persona_id)
        return result is not None

    def _generate_persona_instructions(
        self,
        name: str,
        background: str,
        personality: str,
        expertise: str,
        speech_style: str
    ) -> str:
        """Generate the instruction set for the persona."""
        return f"""You are now embodying a persona with the following characteristics:

Name: {name}

Background:
{background}

Personality Traits:
{personality}

Areas of Expertise:
{expertise}

Speech Style:
{speech_style}

Instructions:
1. Always stay in character and respond as this persona would.
2. Use the speech style and mannerisms described above.
3. Draw from the background and expertise provided.
4. If asked something outside your expertise, acknowledge it while staying in character.
5. Maintain consistent personality traits throughout interactions.
6. When appropriate, reference your background story and experiences.
7. Use vocabulary and expressions that match your character's background.
8. Keep emotional responses consistent with your personality traits.
"""

    @handle_openai_error
    async def update_persona(
        self,
        persona_id: str,
        name: Optional[str] = None,
        background: Optional[str] = None,
        personality: Optional[str] = None,
        expertise: Optional[str] = None,
        speech_style: Optional[str] = None,
        file_ids: Optional[List[str]] = None
    ) -> Optional[Dict]:
        """Update an existing persona's characteristics."""
        # First get the existing persona
        personas = await self.get_all_personas()
        current_persona = next((p for p in personas if p.id == persona_id), None)
        
        if not current_persona:
            st.error(f"Persona with ID {persona_id} not found.")
            return None

        # Update only the provided fields
        new_name = name or current_persona.name
        new_instructions = self._generate_persona_instructions(
            name or current_persona.name,
            background or self._extract_field(current_persona.instructions, "Background"),
            personality or self._extract_field(current_persona.instructions, "Personality Traits"),
            expertise or self._extract_field(current_persona.instructions, "Areas of Expertise"),
            speech_style or self._extract_field(current_persona.instructions, "Speech Style")
        )

        # Update the assistant
        try:
            updated_assistant = await self.assistant_service.client.beta.assistants.update(
                assistant_id=persona_id,
                name=new_name,
                instructions=new_instructions,
                file_ids=file_ids if file_ids is not None else current_persona.file_ids
            )
            return updated_assistant
        except Exception as e:
            st.error(f"Failed to update persona: {str(e)}")
            return None

    def _extract_field(self, instructions: str, field_name: str) -> str:
        """Extract a field from the instruction text."""
        try:
            start = instructions.index(f"{field_name}:") + len(field_name) + 1
            end = instructions.index("\n\n", start)
            return instructions[start:end].strip()
        except ValueError:
            return ""
