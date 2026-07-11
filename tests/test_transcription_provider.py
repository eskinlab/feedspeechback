"""Unit tests for the transcription provider factory."""

import pytest

from feedspeechback.services.transcription import get_transcriber
from feedspeechback.services.transcription.cloud_api import CloudTranscriber
from feedspeechback.services.transcription.whisperx import WhisperXTranscriber


@pytest.fixture(autouse=True)
def clear_provider_cache():
    """The factory caches per process; isolate each test's env var choice."""
    get_transcriber.cache_clear()
    yield
    get_transcriber.cache_clear()


def test_defaults_to_whisperx(monkeypatch):
    monkeypatch.delenv("TRANSCRIPTION_PROVIDER", raising=False)
    assert isinstance(get_transcriber(), WhisperXTranscriber)


@pytest.mark.parametrize(
    ("provider", "expected_type"),
    [("whisperx", WhisperXTranscriber), ("cloud", CloudTranscriber)],
)
def test_selects_configured_provider(monkeypatch, provider, expected_type):
    monkeypatch.setenv("TRANSCRIPTION_PROVIDER", provider)
    assert isinstance(get_transcriber(), expected_type)


def test_unknown_provider_fails_fast(monkeypatch):
    monkeypatch.setenv("TRANSCRIPTION_PROVIDER", "karaoke-machine")
    with pytest.raises(ValueError, match="TRANSCRIPTION_PROVIDER"):
        get_transcriber()


def test_transcriber_is_cached_per_process(monkeypatch):
    monkeypatch.setenv("TRANSCRIPTION_PROVIDER", "whisperx")
    assert get_transcriber() is get_transcriber()
