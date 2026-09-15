# Data Privacy & POPIA Considerations

Recorded sales calls contain **personal information** (voices, names, possibly ID/account numbers spoken aloud) about both agents and customers, and processing them falls under South Africa's **Protection of Personal Information Act (POPIA)**. This document is a starting checklist of considerations to design into the pipeline described in [Technical Architecture](03_technical_architecture.md) — it is not legal advice; legal/compliance sign-off is still required before production use.

## 1. Lawful Basis & Consent

- Confirm the lawful basis for recording and processing these calls (typically: consent captured at call start via an IVR notice, or a legitimate-interest basis already established for QA purposes).
- Confirm the existing call-recording consent notice (if any) covers **automated transcription and speaker diarization**, not just human review — this project changes *how* the recording is processed, which may need to be reflected in agent/customer-facing disclosures.
- This is a **Phase 0 gate** per [Implementation Roadmap](06_implementation_roadmap.md) — confirm consent scope before processing real customer calls, even in early pipeline testing.

## 2. Data Minimization

- Only ingest what's needed: call audio + minimal metadata (call ID, agent ID, timestamp) per US-1.1 — avoid collecting or storing extraneous personal data alongside the recording.
- Transcripts should not be enriched with additional personal data beyond what's spoken in the call unless there's a defined, lawful purpose for doing so.

## 3. Access Control

Maps to US-4.1 in [User Stories](02_user_stories.md) and the Access Control / Audit Log component in [Technical Architecture §2](03_technical_architecture.md):

- Role-based access: only QA Reviewers, Sales Ops Managers, and System Admins should be able to access raw audio and transcripts, scoped to what each role needs (e.g., a QA Reviewer may not need access to raw audio for calls outside their assigned queue).
- All access to audio/transcripts should be logged (who accessed what call, when) to support accountability obligations under POPIA.
- Encryption at rest and in transit for both audio and transcript storage.

## 4. Retention & Deletion

Maps to US-4.2:

- Define separate retention periods for raw audio vs. derived transcripts — transcripts may need shorter or longer retention than audio depending on the QA process's actual needs; don't default to "keep everything forever."
- Deletion must be enforceable and verifiable (audit log entry per deletion), not just a soft flag.
- Consider whether raw audio can be deleted sooner than transcripts once QA review is complete, reducing the volume of raw voice biometric data retained.

## 5. Cross-Border Processing

- The pipeline uses cloud GPU compute ([Technical Architecture §4](03_technical_architecture.md)); confirm which cloud region(s) process and store the data.
- If processing occurs outside South Africa, POPIA's cross-border transfer conditions apply (e.g., the receiving jurisdiction must have adequate data protection, or another safeguard under POPIA §72 must be in place). This should be confirmed with the cloud provider and legal/compliance before Phase 1 goes live with real customer data.
- Preferring a South African (or adequately-protected) cloud region removes this concern entirely if available and cost-viable.

## 6. Special Category Considerations

- Voice recordings can be considered biometric data depending on how they're processed/used — flag this explicitly with compliance, since biometric data typically warrants stricter handling under POPIA.
- If any call content touches special personal information (e.g., health, financial account details spoken aloud), ensure Postgres DB, the Datalake, and their access controls treat transcripts with the same sensitivity as the source audio, not as "just text."

## 7. Open Items for Compliance Sign-Off

- [ ] Confirm existing call-recording consent notice covers automated transcription/diarization.
- [ ] Confirm cloud processing region and cross-border transfer basis.
- [ ] Define and document retention periods for audio vs. transcripts.
- [ ] Confirm role definitions and access scope with Compliance/Sales Ops.
- [ ] Confirm whether voice data here is treated as biometric data under the org's POPIA policy.

These items should be resolved during [Implementation Roadmap](06_implementation_roadmap.md) Phase 0, before any real customer call data is processed.
