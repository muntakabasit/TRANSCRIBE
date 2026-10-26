# DAWT DESIGN — TRANSCRIBE / PRESERVATION-VALIDATION HUMAN CONSEQUENCE 001

**Date:** 26 October 2026  
**FROM:** DAWT.studio → DAWT Design (visual, perceptual, interaction and human–machine experience).  
**TO:** Transcribe technical owner, [Issue #8](https://github.com/muntakabasit/TRANSCRIBE/issues/8).  
**Human source:** Explicit post-audit technical direction: **validate four irreversible-risk mechanisms against the exact audited Build 7 source first, using disposable data; no Build 8, no general twelve-repair implementation; then investigate identity, duplicate link intake and link/file failure; propose minimal repair envelope and stop for approval.**  
**Standing:** BOUNDED DESIGN-RECEIVING CONTRIB​​UTION / HUMAN-OBSERVABLE ACCEPTANCE QUESTIONS. **NOT A VALIDATION RUN, TECHNICAL FIX, SOURCE TRUTH PROMOTION, ARCHITECTURE SELECTION OR EXECUTION AUTHORISATION.**

## Source standing and identity

- The [independent Claude audit result](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6415979029) was a **read-only static** Build 7 inspection, with **0 test-reproduced defects**. It checked 98/98 tracked files of the isolated Build 7 source against the commission. It found four source-supported high-consequence mechanisms, **not historical user-data losses**.
- [RAT's bounded confirmation](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6415952788) confirms the mechanisms by its own source read; it marks other behaviours **not independently established** and holds architectural recommendations as hypotheses.
- [DAWT Design's independent human-machine audit](https://github.com/muntakabasit/TRANSCRIBE/blob/main/docs/design/DAWT_DESIGN_TRANSCRIBE_BUILD7_HUMAN_MACHINE_EXPERIENCE_AUDIT_001.md) and [repair-compatible three-surface interface contract](https://github.com/muntakabasit/TRANSCRIBE/blob/main/docs/design/DAWT_DESIGN_TRANSCRIBE_LIBRARY_CAPTURE_SOURCE_INTERFACE_CONTRACT_001.md) already describe Library, Capture and source-encounter presentation. **This document adds only the human-observable conditions for the newly bounded preservation fixture.**
- The exact original tested source must be the **isolated Build 7 tree** `~/DAWT_Transcriber/reports/TRANSCRIBE_CAPTURE_LIBRARY_SWEEP_20261026_001/ios/DAWT-Transcribe/`, not the divergent dirty root checkout. Preserve current source fingerprints and test on synthetic/disposable data. Do not touch installed iPhone records or captured originals. The technical owner independently controls fixture execution and tests.

## Four preservation gates and corresponding experience truths

| Owner's technical test (synthetic only) | The user-facing behaviour that must become true after verified repair | UI behaviour held until proof | Evidence needed from technical owner |
|---|---|---|---|
| **V1 Original video survival:** video selected in file/Photos intake, original bytes still retrievable after processing and reopen | Real video frame is **Watch**; extracted soundtrack may independently be **Listen to original**; original vs derivative identities distinct | No playable-video overlay based only on a temporary m4a, URL or Photos reference | Input/output fingerprints and reopening actual video stream; **PASS/FAIL/BLOCKED** |
| **V2 Transcript concurrent writers:** local and server writers target same capture, including interleaving/failure/retry | “Previous transcript available” stays true while new attempt is pending; after success source/version identity and ability to inspect both results remain | No one-tap re-transcribe that can silently replace older words; no “corrected” claim from last-writer status alone | Before/after separate version IDs, bytes/hash survival, stable source link; **PASS/FAIL/BLOCKED** |
| **V3 Unreadable notes / image index:** corrupt or inaccessible synthetic backing file then attempt reload/save | **“Couldn't open saved notes/images”** with cautious recovery; keep old bytes untouched; never present decoded failure as genuinely empty collection | No cheerful “empty Library” followed by a normal save that destroys inaccessible records | Original synthetic bytes/hash unchanged after failed read and attempted save; fail-closed status; **PASS/FAIL/BLOCKED** |
| **V4 Already-busy transcription:** submit a second synthetic capture while prior processing is ongoing | The second source has an independently verifiable saved state, with **Waiting** or **Request received** if actually queued; never drop a person's source silently | No optimistic “Transcribing” if request was refused/dropped; no erased draft on unknown outcome | Durable second-source receipt + job outcome and restart/interruption check; **PASS/FAIL/BLOCKED** |

**Result state at handoff:** V1–V4 **NOT RUN BY DAWT DESIGN**; the prior read-only audits show source-supported risk mechanisms, not execution-falsified or verified repair outcomes. Only the technical owner should assign actual test PASS/FAIL/BLOCKED after running a bounded fixture; **do not substitute an attractive prototype for these proofs**.

## After V1–V4, three owner-bound questions

1. **Capture identity:** one pasted URL entered twice may represent a re-encounter or intentional second capture. How can Library show source relation without silently merging distinct human actions? Design requirement: source attribution remains truthful and both captures' user labels survive where distinct.
2. **Duplicate link and source path:** if direct in-app link and Share Extension differ, can the UI say exactly what was captured and not label an in-app action as “from Share Extension”? Does one human submit create one recognisable receipt, not two unacknowledged entries?
3. **Failed-link / successful-file scenario:** distinguish **remote acquisition**, **retained bytes**, **audio track extraction** and **transcription outcome**; display “Couldn’t transcribe from this link” without asserting original source is silent; offer local file choice if actually supported. The backend root cause remains **UNKNOWN** pending specific job/media evidence.

## Minimal repair envelope — Design conditions only, NOT engineering scope approval

**Must remain true:** source bytes recoverable; prior words survive, notes/images don't silently reset; new capture remains durable under busy operation; any displayed Watch/Read/Listen target opens available real material; status shows what is known, not what looks reassuring.

**No new technical architecture mandated.** The technical owner may compare small guarded fixes against broad suggestions such as “one encounter ledger” / “one universal queue”; the static audit did not establish the latter as required. A unified player is an eventual source-identifiable human requirement but is **not a replacement for this four-risk preservation fixture**.

**Human/project decisions still open:** repeated-URL capture equivalence; retention/fallback when original source cannot be copied; presentation and retrieval of multiple transcript attempts; when an unavailable or unsafe action is disabled vs disclosed; overall approved repair scope and admission before any Build 8. DAWT Design advises on clarity, not on schema choices or permission.

**Feed, Quiet Reader integration, automatic AI generation, social connectors and broad visual refoundation remain HELD.**

## Receiving and stop rule

**Transcribe technical owner** returns a source-linked fixture table with four independent **PASS / FAIL / BLOCKED**, exact isolated Build 7 fingerprint, synthetic-data status, reproduction observations, falsifiers and what remains unproven, followed by next investigation (identity/link/file) and **proposed minimal repair envelope**. The report must say **STOP — NOT IMPLEMENTED** until authorised.

**DAWT Design** then critiques **human-facing consequences**, particularly misleading Watch/Read/Listen/status affordances, against actual recorded technical outcomes. No source write, Swift UI implementation, device validation or owner approval is performed by this Design return.

**Keeper:** *Before a doorway becomes beautiful, prove there is real material behind it. Before a status becomes comforting, prove it is true.*
