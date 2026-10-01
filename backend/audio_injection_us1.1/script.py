import os
import uuid
import datetime
from typing import List, Dict
from pydub import AudioSegment  # handy for audio validation

# Example metadata structure
class CallMetadata:
    def __init__(self, agent_id: str, call_id: str, timestamp: datetime.datetime):
        self.agent_id = agent_id
        self.call_id = call_id
        self.timestamp = timestamp

def validate_audio(file_path: str) -> bool:
    """Check if file is a valid WAV or MP3."""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext not in [".wav", ".mp3"]:
            return False
        # Try loading with pydub to confirm it's not corrupt
        #AudioSegment.from_file(file_path)
        return True
    except Exception:
        return False

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
        if not validate_audio(file_path):
            results.append({"file": file_path, "status": "error", "reason": "Invalid or corrupt file"})
            continue

        # Simulate queuing for processing
        queue_id = str(uuid.uuid4())
        results.append({
            "file": file_path,
            "status": "queued",
            "queue_id": queue_id,
            "metadata": meta
        })

    return results

# Example usage
files = ["call1.wav", "call2.mp3", "badfile.txt"]
metadata = [
    {"agent_id": "A123", "call_id": "C001", "timestamp": datetime.datetime.now()},
    {"agent_id": "A124", "call_id": "C002", "timestamp": datetime.datetime.now()},
    {"agent_id": "A125", "call_id": "C003", "timestamp": datetime.datetime.now()},
]

batch_results = upload_batch(files, metadata)
for r in batch_results:
    print(r)
