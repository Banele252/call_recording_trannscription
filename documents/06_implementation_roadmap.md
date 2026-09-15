# Implementation Roadmap

Phased delivery plan for the pipeline described in [Technical Architecture](03_technical_architecture.md), built against the user stories in [User Stories](02_user_stories.md).

## Phase 0 — Discovery & Data Collection

**Goal:** Have real data and a real evaluation baseline before writing pipeline code.

- Collect/obtain a small representative sample of real call recordings across all 5 target languages (with consent — see [Data Privacy & POPIA](07_data_privacy_popia.md)).
- Assemble the per-language held-out evaluation set (US-2.4), using `dsfsi-anv/za-african-next-voices` (Swivuriso) as the primary source per [Model Selection §3](05_model_selection_huggingface.md).
- Run baseline benchmarks: `facebook/mms-1b-all` vs. the language-specific fine-tunes listed in [Model Selection §1](05_model_selection_huggingface.md), recording WER per language.
- **Exit criteria:** documented WER baseline per language; go/no-go call on whether open models are viable or a vendor fallback (Vulavula) is needed for any language.

## Phase 1 — MVP: English + Afrikaans Transcription (no diarization)

**Goal:** Prove the batch pipeline end-to-end on the two best-resourced languages before tackling diarization or the harder Bantu languages.

- Build: Firebase upload + FastAPI trigger, Azure Data Factory orchestration into Storage account/Datalake, Databricks preprocessing + language ID + ASR job (`facebook/mms-1b-all`, English/Afrikaans routing only) (US-1.1, US-1.2, US-1.3, US-2.1, US-2.3).
- Build: Postgres DB structured results + minimal React QA Review UI (read-only transcript view, no diarization yet) (US-3.1, US-3.3).
- Build: Access control on audio/transcripts (US-4.1).
- **Exit criteria:** a batch of real English/Afrikaans calls processed end-to-end, reviewable by QA, WER within an agreed threshold of the Phase 0 baseline.

## Phase 2 — Add isiZulu, isiXhosa, Sesotho + Diarization

**Goal:** Full 5-language coverage with speaker labeling.

- Extend ASR routing to isiZulu, isiXhosa, Sesotho (US-2.3); apply fine-tuning on Swivuriso data where benchmarks from Phase 0 show it's needed.
- Build: Databricks diarization job (`pyannote/speaker-diarization-3.1`) + merge step writing to Datalake/Postgres DB (US-2.2).
- Handle mixed-language/code-switching flagging (US-1.3 edge case, per [Process Flow §3](04_process_flow.md)).
- Add search across transcripts (US-3.2).
- **Exit criteria:** all 5 languages meet agreed WER/DER thresholds; diarized transcripts reviewable end-to-end.

## Phase 3 — Hardening, Scale & Monitoring

**Goal:** Make the pipeline production-reliable and cost-visible.

- Retry/failure handling hardening across all workers (per [Process Flow §3](04_process_flow.md) edge cases).
- Retention & deletion automation (US-4.2).
- Cost/usage monitoring dashboard (US-4.3).
- Re-evaluate deferred languages (Setswana, Sepedi, Xitsonga, Tshivenda, siSwati, isiNdebele) for a future phase based on model/data maturity at that time (per [Project Overview §5](01_project_overview.md)).
- Revisit future-phase capabilities explicitly deferred in [Project Overview §4](01_project_overview.md): sentiment/compliance scoring, summarization, keyword spotting.

## Key Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Lower ASR accuracy for isiZulu/isiXhosa/Sesotho vs. English/Afrikaans (less mature open models) | Poor QA experience, low trust in transcripts for those languages | Phase 0 baseline benchmarking; fine-tune on Swivuriso data; vendor fallback (Vulavula) per [Model Selection §5](05_model_selection_huggingface.md) if needed |
| Code-switching mid-call | Transcription errors, mismatched language routing | Flag rather than force-transcribe (Process Flow §3); revisit as a dedicated feature if volume warrants |
| GPU compute cost scaling with call volume | Budget overrun | Cost monitoring from Phase 3 (US-4.3); scale-to-zero batch workers ([Technical Architecture §4](03_technical_architecture.md)) |
| Audio quality variance (noisy lines, low-quality mobile audio) | Degraded WER regardless of model | Included as an explicit evaluation dimension in Phase 0 sample collection |
| POPIA compliance gaps | Legal/regulatory exposure | Access control and retention built into Phase 1/3, not bolted on later ([Data Privacy & POPIA](07_data_privacy_popia.md)) |

## Dependencies

- Phase 0 evaluation depends on the Swivuriso dataset being accessible and its license terms confirmed for ASR training/eval use ([Model Selection §3](05_model_selection_huggingface.md)).
- Phase 1 depends on cloud GPU compute and storage being provisioned ([Technical Architecture §4](03_technical_architecture.md)).
- Phase 2 diarization depends on Phase 1's Databricks batch job and merge/write-back scaffolding already existing (extended, not rebuilt).
