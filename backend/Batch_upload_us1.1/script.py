import os
import uuid
import datetime
from pathlib import Path
from typing import List, Dict
from pydub import AudioSegment

# Example metadata structure
class CallMetadata:
    def __init__(self, agent_id: str, call_id: str, timestamp: datetime.datetime):
        self.agent_id = agent_id
        self.call_id = call_id
        self.timestamp = timestamp

def validate_audio(file_path: str) -> tuple[bool, str]:
    """Decode a WAV or MP3 file and return its audio details or an error."""
    if os.path.splitext(file_path)[1].lower() not in [".wav", ".mp3"]:
        return False, "Unsupported file type; use WAV or MP3"
    if not Path(file_path).is_file():
        return False, "File not found"

    try:
        audio = AudioSegment.from_file(file_path)
    except FileNotFoundError:
        return False, "Audio decoder not found; install FFmpeg to test MP3 files"
    except Exception as error:
        return False, f"Could not decode audio: {error}"

    details = (
        f"{len(audio) / 1000:.1f}s, {audio.frame_rate} Hz, "
        f"{audio.channels} channel(s), {audio.sample_width * 8}-bit"
    )
    return True, details

def upload_batch(files: List[str], metadata_records: List[Dict]):
    """Upload batch of call recordings with metadata validation."""
    results = []
    for file_path, meta in zip(files, metadata_records):
        call_id = meta.get("call_id")
        agent_id = meta.get("agent_id")
        timestamp = meta.get("timestamp")

        # Basic metadata validation
        if not (call_id and agent_id and timestamp):
            results.append({"file": file_path, "status": "error", "reason": "Missing metadata"})
            continue

        # Audio validation
        is_valid, audio_details = validate_audio(file_path)
        if not is_valid:
            results.append({"file": file_path, "status": "error", "reason": audio_details})
            continue

        # Simulate queuing for processing
        queue_id = str(uuid.uuid4())
        results.append({
            "file": file_path,
            "status": "queued",
            "queue_id": queue_id,
            "metadata": meta,
            "audio": audio_details
        })

    return results

# Test the sample recordings stored next to this script.
audio_dir = Path(__file__).parent / "Audio"
files = [
    str(audio_dir / "Sample Call_ENG_MA.wav"),
    str(audio_dir / "Sample Call_ENG_MA.mp3"),
]
metadata = [
    {"agent_id": "A123", "call_id": "C001", "timestamp": datetime.datetime.now()},
    {"agent_id": "A124", "call_id": "C002", "timestamp": datetime.datetime.now()},
]

batch_results = upload_batch(files, metadata)
for r in batch_results:
    print(r)
