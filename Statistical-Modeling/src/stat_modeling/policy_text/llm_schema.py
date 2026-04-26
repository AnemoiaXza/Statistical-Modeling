from __future__ import annotations


def build_scoring_payload(title: str, content_text: str) -> dict[str, object]:
    return {
        "document": {
            "title": title,
            "content_text": content_text,
            "task_role": "mechanism_or_moderation_only",
        },
        "schema": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "policy_strength": {"type": "number", "minimum": 1, "maximum": 5},
                "execution_clarity": {"type": "number", "minimum": 1, "maximum": 5},
                "digital_green_synergy": {"type": "number", "minimum": 1, "maximum": 5},
            },
            "required": ["policy_strength", "execution_clarity", "digital_green_synergy"],
        },
    }
