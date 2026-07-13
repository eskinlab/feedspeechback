"""Rubrics and prompt templates for the evaluation LLM."""

RUBRICS = {
    "interview": ["technical depth", "communication clarity", "structure of answers"],
    "job_meeting": ["negotiation tone", "active listening", "expectation alignment"],
}


def evaluation_prompt(transcript: str, scenario: str, metrics: dict) -> str:
    criteria = "\n".join(f"- {c}" for c in RUBRICS[scenario])
    return (
        "You are an expert speech coach. Evaluate the following "
        f"{scenario.replace('_', ' ')} transcript against these criteria:\n"
        f"{criteria}\n\n"
        f"Objective metrics: {metrics['words_per_minute']} words/min, "
        f"duration {metrics['duration_s']}s, "
        f"longest pause {metrics['longest_pause_s']}s, "
        f"talk-time share {metrics['speaker_share']}.\n\n"
        f"Transcript:\n{transcript}\n\n"
        "Respond with JSON only: "
        '{"score": <integer 0-100>, "feedback": "<concise, actionable feedback>"}'
    )
