from feedspeechback.activities.transcription import transcribe_audio
from feedspeechback.queues import TRANSCRIPTION_QUEUE
from feedspeechback.workers._runner import run_worker

if __name__ == "__main__":
    run_worker(TRANSCRIPTION_QUEUE, activities=[transcribe_audio])
