# User Stories

Personas used below:
- **QA Reviewer** — listens to/reads calls to assess agent performance
- **Sales Ops Manager** — oversees the QA process, needs aggregate visibility
- **Data Engineer / ML Engineer** — builds and maintains the pipeline
- **System Admin** — manages infrastructure, access, and cost

Prioritization uses MoSCoW (**M**ust / **S**hould / **C**ould / **W**on't-this-phase) for the MVP.

---

## Epic 1: Audio Ingestion

### US-1.1 — Batch upload of call recordings
**As a** Data Engineer, **I want** to upload a batch of call recordings (with basic metadata: agent ID, call timestamp, call ID) **so that** they can be queued for processing without manual per-file handling.
- **Acceptance criteria:**
  - Accepts common audio formats (WAV, MP3, M4A) at minimum.
  - Each upload is associated with a unique call ID and metadata record.
  - Invalid/corrupt files are rejected with a clear error, not silently dropped.
- **Priority:** Must

### US-1.2 — Audio preprocessing
**As a** Data Engineer, **I want** uploaded audio normalized (sample rate, mono channel, volume) **so that** downstream ASR models receive consistent input.
- **Acceptance criteria:**
  - All audio resampled to the target sample rate required by the chosen ASR model(s).
  - Stereo files with separate agent/customer channels are detected and preserved where available (channel info can substitute for/augment diarization).
- **Priority:** Must

### US-1.3 — Language identification
**As a** Data Engineer, **I want** each call (or call segment) automatically tagged with its detected language(s) **so that** the correct ASR model/config is selected per call.
- **Acceptance criteria:**
  - Language ID runs before/alongside transcription and outputs a confidence score.
  - Calls with mixed-language segments are flagged for review rather than forced into a single language.
- **Priority:** Must

---

## Epic 2: Transcription & Diarization

### US-2.1 — Automatic transcription
**As a** QA Reviewer, **I want** each call automatically transcribed to text **so that** I can read the call instead of listening to the full recording.
- **Acceptance criteria:**
  - Transcript covers the full call duration with timestamps at segment level.
  - Supports English, isiZulu, isiXhosa, Afrikaans, Sesotho per the [Project Overview](01_project_overview.md) language scope.
  - Low-confidence segments are marked as such in the output.
- **Priority:** Must

### US-2.2 — Speaker diarization
**As a** QA Reviewer, **I want** the transcript labeled by speaker ("Agent" / "Customer") **so that** I can tell who said what without listening to the audio.
- **Acceptance criteria:**
  - Each transcript segment is tagged with a speaker label and timestamp range.
  - Diarization output is merged with the ASR transcript into one unified, ordered view.
  - Where stereo channel separation is available (US-1.3), it is used to improve/validate diarization.
- **Priority:** Must

### US-2.3 — Per-language model routing
**As a** Data/ML Engineer, **I want** the pipeline to route each call to the ASR model best suited to its detected language **so that** transcription quality is maximized per language rather than using one generic model for all.
- **Acceptance criteria:**
  - Model selection logic is configurable per language (see [Model Selection](05_model_selection_huggingface.md)).
  - Fallback model is used when language ID confidence is low.
- **Priority:** Must

### US-2.4 — Evaluation & quality tracking
**As a** Data/ML Engineer, **I want** WER and DER tracked per language on a held-out evaluation set **so that** I know current transcription/diarization quality and can detect regressions.
- **Acceptance criteria:**
  - Evaluation set covers all 5 target languages.
  - Metrics are recomputed whenever a model is swapped or fine-tuned.
- **Priority:** Should

---

## Epic 3: QA Review Workflow

### US-3.1 — View transcript alongside audio
**As a** QA Reviewer, **I want** to view the diarized transcript next to a playable version of the original audio **so that** I can jump to a specific moment if I need to verify what was said.
- **Acceptance criteria:**
  - Clicking a transcript segment seeks the audio player to that timestamp.
- **Priority:** Should

### US-3.2 — Search across transcripts
**As a** QA Reviewer, **I want** to search text across all processed call transcripts **so that** I can find calls mentioning specific terms without listening to each one.
- **Acceptance criteria:**
  - Search returns matching calls with the matching segment highlighted.
- **Priority:** Could

### US-3.3 — Processing status visibility
**As a** Sales Ops Manager, **I want** to see the processing status of uploaded call batches (queued/processing/done/failed) **so that** I know when transcripts are ready for review.
- **Acceptance criteria:**
  - Status is visible per call and per batch.
  - Failures show a reason (e.g., unsupported format, low-confidence language ID).
- **Priority:** Should

---

## Epic 4: Admin & Operations

### US-4.1 — Access control
**As a** System Admin, **I want** access to call recordings and transcripts restricted to authorized roles **so that** we meet POPIA obligations around sensitive personal data (see [Data Privacy & POPIA](07_data_privacy_popia.md)).
- **Acceptance criteria:**
  - Role-based access (e.g., QA Reviewer, Sales Ops Manager, Admin) enforced on both audio and transcript access.
  - Access events are logged.
- **Priority:** Must

### US-4.2 — Retention & deletion
**As a** System Admin, **I want** configurable retention periods for raw audio and transcripts **so that** we don't retain personal data longer than necessary or permitted.
- **Acceptance criteria:**
  - Retention policy configurable per data type (raw audio vs. transcript).
  - Deletion is verifiable (audit log entry).
- **Priority:** Must

### US-4.3 — Cost & usage monitoring
**As a** System Admin, **I want** to see cloud compute cost and processing volume over time **so that** I can manage the pipeline's operating budget.
- **Acceptance criteria:**
  - Dashboard or report shows cost per call-hour processed, by language.
- **Priority:** Could

---

## Out of Scope This Phase (tracked for future epics)
- Sentiment/compliance scoring stories
- Automatic call summarization stories
- Keyword/topic spotting stories
- Real-time/in-call processing stories

See [Project Overview §4](01_project_overview.md#4-in-scope-vs-out-of-scope) for rationale.
