"""``tag_audio`` — composer that chains transcription → generate tags."""

from typing import Any

from centeba_smart_llm.base import Tool
from centeba_smart_llm.builtins.parsing.parse_audio import ParseAudioTranscriptSkill
from centeba_smart_llm.builtins.tagging.generate_tags import GenerateTagsSkill
from centeba_smart_llm.db.models import MODALITY_AUDIO
from centeba_smart_llm.registry import register_tool


class TagAudioSkill(Tool):
    """Pipe-line: transcribe the audio → ask LLM for tags on the transcript."""

    def run(self, input_text: str, **kwargs: Any) -> str:
        try:
            text = ParseAudioTranscriptSkill().run(input_text)
        except NotImplementedError:
            # Phase E5 wires real Whisper/provider fallbacks.
            text = input_text
        return GenerateTagsSkill().run(text)


register_tool(
    "tag_audio",
    TagAudioSkill,
    label="Tag Audio",
    description="Transcribe an audio file and generate tag suggestions in one step.",
    modality=MODALITY_AUDIO,
)
