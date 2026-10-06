import uuid
from pathlib import Path
from typing import Dict, List, Tuple, Union
from pydub import AudioSegment

def validate_audio(file_path: str) -> Tuple[bool, Union[Dict[str, object], str]]:
    """Decode a WAV or MP3 file and return structured audio metadata or an error."""
    file_type = Path(file_path).suffix.lower().lstrip(".")
    if file_type not in ["wav", "mp3"]:
        return False, "Unsupported file type; use WAV or MP3"
    if not Path(file_path).is_file():
        return False, "File not found"

    try:
        audio = AudioSegment.from_file(file_path)
    except FileNotFoundError:
        return False, "FFmpeg not installed or not in PATH"
    except Exception as error:
        return False, f"Could not decode audio: {error}"

    audio_metadata = {
        "duration_seconds": round(len(audio) / 1000, 3),
        "file_type": file_type,
        "sample_rate_hz": audio.frame_rate,
        "channels": audio.channels,
        "bit_depth": audio.sample_width * 8,
        "frame_count": int(audio.frame_count()),
        "file_size_bytes": Path(file_path).stat().st_size,
    }
    return True, audio_metadata

def upload_batch(files: List[str]):
    """Queue audio files with metadata extracted from each recording."""
    results = []
    for file_path in files:
        is_valid, audio_metadata = validate_audio(file_path)
        if not is_valid:
            results.append({"file": file_path, "status": "error", "reason": audio_metadata})
            continue

        queue_id = str(uuid.uuid4())
        results.append({
            "file": file_path,
            "status": "queued",
            "queue_id": queue_id,
            "metadata": audio_metadata,
        })
    return results

# 🔄 Always look for an 'audio' folder next to this script
audio_dir = Path(__file__).parent / "audio"

# Ensure the folder exists
audio_dir.mkdir(exist_ok=True)

# Collect all supported audio files
files = sorted(
    str(file_path)
    for file_path in audio_dir.glob("*")
    if file_path.is_file() and file_path.suffix.lower() in {".wav", ".mp3"}
)

if not files:
    print(f"No WAV or MP3 files found in {audio_dir}")
else:
    batch_results = upload_batch(files)
    for r in batch_results:
        print(r)
