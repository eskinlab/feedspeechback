"""Objective speech metrics computed from the transcript segments."""


def analyze(segments: list[dict]) -> dict:
    if not segments:
        return {
            "duration_s": 0,
            "words": 0,
            "words_per_minute": 0,
            "longest_pause_s": 0,
            "speaker_share": {},
        }

    duration = segments[-1]["end"] - segments[0]["start"]
    words = sum(len(seg["text"].split()) for seg in segments)
    pauses = [b["start"] - a["end"] for a, b in zip(segments, segments[1:])]

    talk_time: dict[str, float] = {}
    for seg in segments:
        speaker = seg.get("speaker", "SPEAKER_??")
        talk_time[speaker] = talk_time.get(speaker, 0.0) + seg["end"] - seg["start"]
    total_talk = sum(talk_time.values()) or 1.0

    return {
        "duration_s": round(duration),
        "words": words,
        "words_per_minute": round(words / duration * 60) if duration else 0,
        "longest_pause_s": round(max(pauses), 1) if pauses else 0,
        "speaker_share": {
            speaker: round(t / total_talk * 100) for speaker, t in talk_time.items()
        },
    }
