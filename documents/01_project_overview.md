# Project Overview — Sales Call Review

## 1. Purpose & Background

Sales agents' calls are currently reviewed manually by QA staff, who listen to raw audio to check what was said, by whom, and how. This is slow, inconsistent, and does not scale as call volume grows. This project builds an automated pipeline that **transcribes sales agent call audio and identifies who spoke when (speaker diarization)**, producing a searchable, reviewable transcript for each call so QA reviewers spend their time reviewing content instead of listening to raw recordings.

The pipeline is built primarily on open Hugging Face models, with a specific focus on models that perform well on **South African languages**, since a meaningful share of calls are conducted partly or fully in a language other than English.

## 2. Goals

- Automatically transcribe recorded sales calls into text.
- Separate and label speaker turns (agent vs. customer) within each call.
- Support the languages actually spoken on these calls (see §4).
- Produce output that plugs into a QA review workflow (transcript + speaker labels, timestamped).
- Establish a model-selection and evaluation process so language coverage/quality can be improved over time.

## 3. Success Criteria

- Transcription pipeline runs end-to-end on a batch of uploaded call recordings without manual intervention.
- Word Error Rate (WER) and Diarization Error Rate (DER) are measured per language against a held-out evaluation set, with documented baselines.
- QA reviewers can open a call and see a diarized, timestamped transcript instead of (or alongside) the raw audio.
- Pipeline cost per call-hour processed is known and tracked.

## 4. In Scope vs. Out of Scope

### In scope (this phase)
- Audio ingestion (batch upload) and preprocessing (format normalization, language identification).
- Automatic Speech Recognition (ASR) — speech-to-text transcription.
- Speaker diarization — who spoke when.
- Storage of transcripts + diarization output for QA review.
- Language coverage: English + isiZulu, isiXhosa, Afrikaans, Sesotho (see §5 for rationale).

### Explicitly out of scope for this phase (future extensions)
- Sentiment analysis / tone detection.
- Compliance / required-disclosure phrase detection and scoring.
- Automatic call summarization.
- Keyword/topic spotting (competitor mentions, objections, complaints).
- Real-time (in-call) processing — this phase is batch-only.

These are noted here so future phases have an obvious home; they are not designed or built in this iteration.

## 5. Language Scope

South Africa has 11 official languages plus significant code-switching in everyday speech. Building and evaluating for all 11 at once would spread effort too thin, especially since open model/dataset coverage varies a lot by language. This phase targets the **five languages with the most mature open ASR resources and highest call-centre relevance**:

| Language | ISO 639-1/3 | Family | Rationale |
|---|---|---|---|
| English | en | Germanic | Primary business language, best model coverage |
| isiZulu | zu | Nguni (Bantu) | Most-spoken home language in SA, strong dataset support (DSFSI, MMS, Whisper fine-tunes) |
| isiXhosa | xh | Nguni (Bantu) | Second-largest Nguni language, covered by MMS and DSFSI resources |
| Afrikaans | af | Germanic | Best-resourced non-English SA language on Hugging Face (multiple mature model families) |
| Sesotho | st | Sotho-Tswana (Bantu) | Strong dataset support (DSFSI Swivuriso, Lelapa Vulavula), representative of Sotho-Tswana languages |

Setswana, Sepedi, Xitsonga, Tshivenda, siSwati, and isiNdebele are deferred to a later phase (tracked in the [Implementation Roadmap](06_implementation_roadmap.md)) pending more open model/data maturity, per the [Model Selection](05_model_selection_huggingface.md) doc.

## 6. Stakeholders

| Role | Interest |
|---|---|
| Sales Ops / QA Lead | Primary consumer of transcripts; drives requirements for the review workflow |
| Compliance team | Longer-term consumer once compliance-scoring (future phase) is added |
| Data/ML team | Owns model selection, fine-tuning, evaluation, and pipeline reliability |
| System Admin / Platform team | Owns cloud infra, storage, cost, and access control |
| Sales Agents | Subjects of the recordings; consent and privacy handling affects them directly |

## 7. Assumptions & Constraints

- Calls are recorded and available as audio files (not live streams) — this is a **batch** pipeline (see [Technical Architecture](03_technical_architecture.md)).
- Audio quality varies (call-centre headsets, mobile handoffs); pipeline must tolerate moderate noise.
- Some calls include **code-switching** (mixing English with an African language mid-sentence) — flagged as a known accuracy risk, not solved in this phase.
- Recordings contain personal information and must be handled under South Africa's **POPIA** — see [Data Privacy & POPIA](07_data_privacy_popia.md).
- Cloud GPU compute is available and budgeted; on-prem deployment is not in scope for this phase.

## 8. Related Documents

- [User Stories](02_user_stories.md)
- [Technical Architecture](03_technical_architecture.md)
- [Process Flow](04_process_flow.md)
- [Model Selection (Hugging Face)](05_model_selection_huggingface.md)
- [Implementation Roadmap](06_implementation_roadmap.md)
- [Data Privacy & POPIA](07_data_privacy_popia.md)
