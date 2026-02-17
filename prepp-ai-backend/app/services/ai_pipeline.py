"""
AI Pipeline Service
Handles structured brief generation using LLM with RAG context
"""

import json
from typing import Dict, Any, List
import structlog
import google.generativeai as genai

from app.core.config import settings

logger = structlog.get_logger(__name__)

class AIPipeline:
    """AI Pipeline for generating structured teaching briefs"""

    _model: genai.GenerativeModel | None = None

    def __init__(self):
        self.model_name = settings.LLM_MODEL
        # Configure Gemini API
        genai.configure(api_key=settings.GEMINI_API_KEY)

    @property
    def model(self) -> genai.GenerativeModel:
        if AIPipeline._model is None:
            AIPipeline._model = genai.GenerativeModel(self.model_name)
        return AIPipeline._model

    async def generate_brief(
        self,
        subject: str,
        grade: str,
        topic: str,
        rag_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a structured teaching brief using AI

        Args:
            subject: Norwegian subject (fag)
            grade: Grade level (1-13 or VG1-VG3)
            topic: Topic to cover
            rag_context: Retrieved context from RAG search

        Returns:
            Structured brief content as dictionary
        """

        # Build context string from RAG results
        context_parts = []
        if rag_context.get("lk20_goals"):
            context_parts.append(f"LK20 kompetansemål: {rag_context['lk20_goals']}")

        if rag_context.get("source_chunks"):
            sources_text = "\n".join([
                f"Kilde: {chunk.get('title', 'Uten tittel')}\n{chunk.get('content', '')}"
                for chunk in rag_context["source_chunks"][:3]  # Limit to top 3
            ])
            context_parts.append(f"Relevante kilder:\n{sources_text}")

        context = "\n\n".join(context_parts) if context_parts else "Ingen spesifikk kontekst funnet."

        # System prompt for structured brief generation
        system_prompt = f"""Du er en erfaren norsklærer som lager kvalitetssikrede undervisningsbriefer for norske lærere.

Din oppgave er å generere en strukturert lærermansual som gir læreren alt de trenger for å undervise i et tema uten å være ekspert på området.

Bruk følgende kontekst som utgangspunkt:
{context}

GENERER EN STRUKTURERT BRIEF MED DISSE SEKSJONENE:

1. LÆREPLANKOBLING: Relevante kompetansemål fra LK20, tverrfaglige temaer og grunnleggende ferdigheter for {subject} trinn {grade}

2. FAGLIG DYBDE: Kjernekonsepter, sammenhenger og faglig kontekst rundt temaet "{topic}"

3. PEDAGOGISKE TIPS: Metafører, analogier, "knagger" og konkrete undervisningsforslag

4. ELEVSPØRSMÅL OG FELLER: Forventede spørsmål fra elever og vanlige misforståelser å være forberedt på

5. KILDER: Direkte henvisninger til SNL, NDLA og Udir med sitatreferanser

SVAR UTELUKKENDE MED EN JSON-OBJEKT som har disse nøyaktige nøklene:
{{
    "lk20_kobling": "tekst her",
    "faglig_dybde": "tekst her",
    "pedagogiske_tips": "tekst her",
    "elev_sporsmal_feller": "tekst her",
    "kilder": "tekst her"
}}

Ingen tilleggstekst, bare gyldig JSON."""

        # User prompt
        user_prompt = f"""Generer lærermanual for:
- Fag: {subject}
- Trinn: {grade}
- Tema: {topic}"""

        try:
            # Configure generation parameters
            generation_config = genai.GenerationConfig(
                temperature=0.1,  # Low temperature for consistent, factual output
                max_output_tokens=settings.MAX_BRIEF_TOKENS,
                response_mime_type="application/json"
            )

            # Create model with system prompt as part of the prompt
            full_prompt = f"{system_prompt}\n\n{user_prompt}"

            # Call Gemini API
            response = await self.model.generate_content_async(
                full_prompt,
                generation_config=generation_config
            )

            # Extract and parse JSON response
            content = response.text.strip()

            # Remove potential markdown code blocks
            if content.startswith("```json"):
                content = content[7:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            # Parse JSON
            brief_data = json.loads(content)

            # Validate required keys
            required_keys = ["lk20_kobling", "faglig_dybde", "pedagogiske_tips", "elev_sporsmal_feller", "kilder"]
            for key in required_keys:
                if key not in brief_data:
                    brief_data[key] = f"Manglende innhold for {key}"

            logger.info(
                "Brief generated successfully",
                subject=subject,
                grade=grade,
                topic=topic,
                # Note: Gemini doesn't provide detailed token usage in the same way
            )

            return brief_data

        except json.JSONDecodeError as e:
            logger.error("Failed to parse AI response as JSON", error=str(e), content=content[:500])
            # Fallback: return structured error response
            return {
                "lk20_kobling": "Feil ved generering av læreplankobling",
                "faglig_dybde": "Feil ved generering av faglig dybde",
                "pedagogiske_tips": "Feil ved generering av pedagogiske tips",
                "elev_sporsmal_feller": "Feil ved generering av elevspørsmål og feller",
                "kilder": "Feil ved generering av kilder",
            }

        except Exception as e:
            logger.error("AI pipeline failed", error=str(e))
            raise

    async def followup_brief(
        self,
        original_brief: Dict[str, Any],
        followup_topic: str,
        rag_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Generate a follow-up brief for deeper dive into a sub-topic
        """
        # Similar to generate_brief but focused on a sub-topic
        # Implementation would be similar but with different prompt
        # For MVP, we'll implement this later
        pass