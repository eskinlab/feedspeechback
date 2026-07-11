from feedspeechback.activities.diarization import diarize_audio
from feedspeechback.queues import DIARIZATION_QUEUE
from feedspeechback.workers._runner import run_worker

if __name__ == "__main__":
    run_worker(DIARIZATION_QUEUE, activities=[diarize_audio])
