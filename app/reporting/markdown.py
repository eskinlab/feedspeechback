"""Render the markdown report."""


def render(result: dict, evaluation: dict, metrics: dict, scenario: str) -> str:
    lines = [
        f"# Speech feedback — {scenario.replace('_', ' ')}",
        "",
        f"**Score:** {evaluation['score']}/100",
        "",
        "## Feedback",
        "",
        evaluation["feedback"],
        "",
        "## Metrics",
        "",
        f"- Duration: {metrics['duration_s']}s",
        f"- Words: {metrics['words']} ({metrics['words_per_minute']} per minute)",
        f"- Longest pause: {metrics['longest_pause_s']}s",
    ]
    for speaker, share in metrics["speaker_share"].items():
        lines.append(f"- {speaker}: {share}% of talk time")
    lines += ["", f"## Transcript ({result['language']})", ""]
    for seg in result["segments"]:
        speaker = seg.get("speaker", "SPEAKER_??")
        lines.append(f"- **{speaker}** [{seg['start']:.0f}s] {seg['text'].strip()}")
    return "\n".join(lines) + "\n"
