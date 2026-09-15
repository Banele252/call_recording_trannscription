# Model Selection — Hugging Face Models for South African Languages

This document evaluates candidate Hugging Face models for the ASR and diarization stages described in [Technical Architecture](03_technical_architecture.md), for the five target languages: English, isiZulu, isiXhosa, Afrikaans, Sesotho.

## 1. ASR (Speech-to-Text) Candidates

| Model | Coverage of target languages | Notes | License |
|---|---|---|---|
| [`facebook/mms-1b-all`](https://huggingface.co/facebook/mms-1b-all) (Meta MMS) | English, isiZulu, isiXhosa, Afrikaans, Sesotho — all covered (MMS spans 1,100+ languages, including most Bantu languages) | Single model handles all 5 target languages via language adapters; strong baseline for lower-resource languages where fine-tuned alternatives don't exist yet | CC-BY-NC 4.0 (research use; check commercial terms before production use) |
| OpenAI Whisper large-v3 (general) | English strong; African languages weaker out of the box | Good general baseline for English only; not recommended as-is for the other 4 | MIT |
| [`Sunbird/asr-whisper-51-african-languages`](https://huggingface.co/Sunbird/asr-whisper-51-african-languages) | Whisper large-v3 fine-tuned across 51 African languages incl. Afrikaans, Sotho, Xhosa, Zulu | Whisper-family fine-tune specifically adapted for African language ASR; worth benchmarking against MMS | Check model card for license/terms |
| `asr-africa` Afrikaans collection ([link](https://huggingface.co/collections/asr-africa/afrikaans)) | Afrikaans only | Multiple architectures available (Whisper-Small, Wav2Vec2-BERT, MMS-1B, Wav2Vec2 XLSR-300M) — useful for a head-to-head Afrikaans benchmark | Varies by model, check individually |
| TheirStory Whisper-Zulu ASR collection ([link](https://huggingface.co/collections/TheirStory/whisper-zulu-asr-models-66c25b7926fef28c3e890f5d)) | isiZulu | Whisper fine-tuned specifically for isiZulu | Check model card |

### Recommendation
Start with **`facebook/mms-1b-all`** as the default model across all 5 languages — it's the only candidate with native, consistent coverage of all target languages from one model family, simplifying the "per-language routing" logic in [Technical Architecture §2](03_technical_architecture.md). Benchmark it against the language-specific fine-tunes (`Sunbird/asr-whisper-51-african-languages`, the `asr-africa` Afrikaans set, TheirStory's Zulu Whisper models) on a held-out evaluation set per language (US-2.4); swap in whichever fine-tune wins per-language if it clearly outperforms MMS for that language. English can additionally be benchmarked against a plain Whisper large-v3 baseline, since English is Whisper's strongest language.

## 2. Speaker Diarization

| Model | Notes |
|---|---|
| [`pyannote/speaker-diarization-3.1`](https://huggingface.co/pyannote/speaker-diarization-3.1) | Industry-standard open diarization pipeline on Hugging Face; language-agnostic (operates on acoustic features, not transcribed text), so it applies uniformly across all 5 target languages without per-language tuning |

### Recommendation
Use `pyannote/speaker-diarization-3.1` as the diarization component. Where stereo recordings with separate agent/customer channels are available (US-1.2), prefer channel-based speaker separation and use diarization as a fallback/validation for mono recordings — channel separation is inherently more reliable than acoustic diarization.

## 3. South African Research Assets (for fine-tuning & evaluation)

| Resource | Description | Use |
|---|---|---|
| [`dsfsi-anv/za-african-next-voices`](https://huggingface.co/datasets/dsfsi-anv/za-african-next-voices) (Swivuriso dataset, DSFSI / University of Pretoria) | 3,000+ hours of speech across 7 SA languages (isiZulu, isiXhosa, Sesotho, Setswana, Sepedi, isiNdebele, Tshivenda), scripted + unscripted, community-collected | Primary candidate dataset for building the per-language evaluation set (US-2.4) and for fine-tuning MMS/Whisper on isiZulu, isiXhosa, and Sesotho specifically. **Note:** dataset terms currently prohibit TTS/voice-cloning use — ASR training/evaluation use is the intended use case here and is permitted, but confirm current terms before use. |
| [`dsfsi/zabantu-xlm-roberta`](https://huggingface.co/dsfsi/zabantu-xlm-roberta) | XLM-RoBERTa encoder for South African languages | Not used for ASR directly, but relevant if/when future phases add text-based NLP (sentiment, compliance detection — currently out of scope per [Project Overview §4](01_project_overview.md)) |

## 4. Language ID

Use `facebook/mms-lid-256` (or `mms-lid-4017` for finer granularity) for the Language ID Worker in [Technical Architecture](03_technical_architecture.md) — same model family as the MMS ASR model, keeping the pipeline's dependency footprint small.

## 5. Build vs. Buy Reference Point

[Lelapa AI's Vulavula](https://lelapa.ai/products/vulavula/) is a commercial API offering ASR + NER for English, Afrikaans, isiZulu, and Sesotho (with more SA languages planned), built by a team specializing in African-language AI. It's a relevant **build-vs-buy comparison**: if in-house open-model performance (MMS/Whisper fine-tunes) doesn't reach an acceptable WER for a given language within Phase 1/2 timelines (see [Implementation Roadmap](06_implementation_roadmap.md)), Vulavula (or a similar vendor) is a fallback worth costing out for that language, rather than open-sourcing further fine-tuning effort indefinitely. Lelapa's [InkubaLM](https://lelapa.ai/publications) (a compact multilingual African-language LLM) is also worth revisiting if/when future phases add summarization or sentiment analysis.

## 6. Summary Recommendation

| Pipeline stage | Chosen model | Fallback / to benchmark |
|---|---|---|
| Language ID | `facebook/mms-lid-256` | — |
| ASR (all 5 languages, default) | `facebook/mms-1b-all` | `Sunbird/asr-whisper-51-african-languages`, `asr-africa` Afrikaans models, TheirStory Zulu Whisper, plain Whisper large-v3 (English only) |
| Diarization | `pyannote/speaker-diarization-3.1` | Stereo channel separation where available |
| Fine-tuning data | `dsfsi-anv/za-african-next-voices` (Swivuriso) | — |
| Vendor fallback (per language, if needed) | Lelapa AI Vulavula | — |

Model choices here feed directly into the Databricks batch jobs and the A.I inference layer in [Technical Architecture §4](03_technical_architecture.md#4-where-the-hugging-face-models-plug-in), and the per-language benchmarking work is scheduled in [Implementation Roadmap](06_implementation_roadmap.md).
