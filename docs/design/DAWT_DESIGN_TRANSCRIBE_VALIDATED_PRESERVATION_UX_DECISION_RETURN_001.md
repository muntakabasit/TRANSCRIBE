# DAWT DESIGN — TRANSCRIBE / VALIDATED PRESERVATION → HUMAN EXPERIENCE RETURN 001

**Date:** 26 October 2026
**Role / origin:** DAWT Design — material-first UI, visual hierarchy, intelligible state and human–machine experience.
**To:** Transcribe technical/product owner and separately authorised implementation workers, existing [Issue #8](https://github.com/muntakabasit/TRANSCRIBE/issues/8).
**Human-carried source:** user supplied recommended decisions for Claude after the first validation fixture. The human-reported recommendations are **proposals**, not an accepted implementation order.
**Independent underlying read:** Direct read of original worker-authored `TRANSCRIBE_PRESERVATION_VALIDATION_001_REPORT.md` on Abduls-MacBook-Pro.local at `~/DAWT_Transcriber/reports/TRANSCRIBE_PRESERVATION_VALIDATION_20261026_001/`. Report SHA-256 `211e5079ef7e294cca09cf6911f6209f1883d6756ac554b4ef6371c3192ff16e`, read on 26 Oct.
**Standing:** DESIGN RECEIPT TO A REAL VALIDATION RESULT / MICROCOPY + INTERACTION BOUNDARY / NOT CODE, AN OWNER DECISION, PERMISSION TO RUN BUILD 8, PHYSICAL-DEVICE ACCEPTANCE OR HISTORICAL-LOSS EVIDENCE.

## 1. Evidence distinction after fixture (actual worker claims; not tests run by DAWT Design)

Worker ran 14 synthetic/disposable preservation tests across four suites, twice on an iPhone 17 simulator, using a copy matching 98/98 audited Build 7 source hashes plus one test file; original audit source, phone, backups and real captures remained untouched according to the report.

| Case | Worker evidence | Standing | Interface implication |
|---|---|---|---|
| **V1 Original video survival** | `AudioImporter → importedURL → preserveThenProcess`: a synthetic H.264/AAC MP4 becomes retained M4A audio, not original video. Original video hash differs; direct audio control PASS. | **EXECUTED FAIL**; actual SwiftUI HomeView glue and Photos/`.mov` not run | Don't falsely offer Watch on a retained sound derivative; after verified repair use original frame as actual Watch affordance. |
| **V2 Two transcript writers** | Both local→server and server→local same-id sequences leave only the last output; distinct-ID control keeps both. | **EXECUTED FAIL**; collision occurrence in actual human records still unproven | Preserve a recoverable prior version; make retries visibly separate, not silent text substitution. |
| **V3 Corrupt notes and image indexes** | After synthetic corruption, save overwrites note store; index of three image files becomes one while two files remain orphaned. Missing-file control works. | **EXECUTED FAIL**; real-device corruption occurrence unknown | Never display unreadable store as empty, never mark a new note saved when write is refused. |
| **V4 Busy transcription** | Guard is in a private SwiftUI method before preservation; fixture cannot run it without altered source or live upload. | **SOURCE RISK / BLOCKED**, not an executed failure | Status may say Saved but not processed **only when durable receipt exists**. No invented queue. |

Additional worker identity evidence: in-app paste wrongly marked `share_extension`; one link-options Transcribe action creates two records; two Share Sheet events create two receipts/jobs; URL-keyed label context causes “Monday” to disappear after a later “Friday” save; top-level preferred-transcript projection shows one attempt although older record can remain on disk. The failed-link/successful-file **cause remains UNKNOWN**: the server obtains social link media while the phone uploads its local audio derivative through a different endpoint. The private backend `/share-jobs` evidence and one actual failed receipt remain outstanding.

**Source integrity caveat:** These were disposable fixtures, *not* proof that personal iPhone records have been lost or that the full phone experience has passed.

## 2. What must become perceptible before a design is premium

**The person owns the original source and its captured history.** The interface must distinguish *selected*, *preserved*, *processing requested*, *processing completed*, *representation available*, *failed*, *unreadable*, *unknown*. Avoid equating all with a green checkmark.

**Material-first hierarchy:** actual playable video frame → Watch; authentic audio → Listen to original; real saved passage → Read; actual picture → View; saved URL → Open original. These are independent availability gates under one recognisable source/context; **a URL preview must never impersonate a retained playable movie**.

**Failure treatment:** when something cannot be done, show what the app actually preserved, one safe next action, an optional technical reason, and a clear exit. Do not force explanatory copy on successful normal use.

## 3. Five concrete screen-state/microcopy contracts for owner decision

### A. Video file exceeds unchanged 250 MB cap

**Before destructive processing, with true detected size:** `This video is too large to import.` Subtext: `The limit is 250 MB. This file is [actual size]. Transcribe hasn't kept a copy.` Actions: **Choose another file** and **Cancel**. If explicitly verified, optional `The original is still in Photos / Files`; do **not** claim this for unsupported provider paths.

**Do not:** silently extract only the sound, call the result Video saved, move the original, invent an upload in progress, or pretend that an oversized video can later be watched in Library. A user can still choose a separate **audio-only** workflow if such a capability is genuinely offered and labelled, but it is not an automatic fallback.

**Acceptance:** full-size 249 MB (after actual byte policy) is preserved as video; 251 MB is rejected before alteration with a recoverable original. Test exact threshold, not decimal UI copy alone. These are proposed tests, **not results**.

### B. Saved notes or camera-image index cannot be read

`We can't open your saved notes right now.`
`To protect them, Transcribe isn't making changes to this collection.`
Actions: **Try again**, **See details**, optional **Copy new note** if a freshly typed unsaved draft exists. Image case: `We can't open the saved image list. Your image files may still be present.` The last sentence requires actual observed on-disk evidence; otherwise say `We haven't confirmed which images are available.`

**Do not:** show `No notes yet`, a first-use celebration, a falsely blank Library, or a **Save** button that claims success while the backing store is blocked. If a draft is not durably saved, mark `Draft not saved` and preserve/copy only what current runtime truly can; no false promise through app termination.

**Acceptance:** opening the unreadable store then attempting save preserves corrupt original bytes and does not erase pre-existing notes/image references; screen clearly refuses the attempted write.

### C. Transcript attempts are separate, earlier text stays available

One source detail may show:
- **Transcript · previous result** (real version date when known) — available while a new attempt is running.
- **New transcription · requested / preparing / available / failed** — status as evidenced by actual durable job/attempt.
- A deliberate **View earlier version** affordance, where more than one version actually exists.

The **source/capture identity** is stable while **each processing attempt has its own independently addressable identity and provenance**. This aligns with the human-carried recommended decision; the worker's archive-on-replace (R1-min) remains an alternative engineering proposal, **not equivalent to the full identity contract without demonstrated recoverable mapping**.

**Do not:** silently replace an earlier transcript because another worker returned, pretend a generated version is certified speech, or change a reading anchor's underlying words without making version change visible.

**Acceptance:** local→server and server→local synthetic tests retain two distinct retrievable results; older text remains readable after failed retry, reopen and refresh.

### D. Repeated links and honest capture identity

**Two records accidentally created by one human tap:** UI should show **one confirmed capture outcome** and one receipt, not two apparent new items. Engineer verifies event identity/idempotence; DAWT Design does not choose dedupe keys.

**Two genuinely separate user actions on the same URL:** preserve **both original human encounters**, labels and dates; present two distinct saved instances in Library. Optional visual relationship `Also saved before` is permissible only if actual linked identity exists and doesn't merge/hide either item.

**Do not:** key human label solely by URL if it overwrites prior label; silently decide `same URL = same encounter`; call deliberate saves duplicates; infer project/destination from the label.

**Acceptance:** one click yields one user-visible receipt; two deliberately separate saves yield distinct accessible records and both original labels.

### E. Link failed but imported file worked

Only after a verified saved link/receipt:
`Couldn't transcribe from this link.`
`The link is still saved.` **Only if verified saved.**
Actions: **Open original** · **Choose a file** (only if owner validates import capability) · **See details**.

**Do not:** say `This video has no audio` based solely on a failed server fetch; do not blame TikTok, provider access, rate limits, missing codecs or corrupted original until backend job evidence identifies that failure. Nor show `Downloaded video` when only URL metadata exists.

**Acceptance:** precise failed receipt and server job show whether failure occurred in fetch, validation, audio extraction, speech recognition or response delivery. Correct UI branch only after real evidence; cause remains **unresolved today**.

### F. Busy transcription (validation-blocked)

If and only if the second capture is **durably saved**:
`Saved for later.`
`Another transcription is running. This one hasn't started yet.`

If no proof of durable source: `Couldn't confirm this capture was saved.` and preserve editable input **only where actually true**; provide retry or local retention without invented queue semantics.

**Do not:** show `Transcribing` when no job started or call a source `Queued` unless a real queue exists.

**Acceptance:** explicit second-source receipt persists through retry/background interruption, and its processing state is separately verifiable. P4 is **BLOCKED in current tested source**.

## 4. Relation to the approved repair envelope — not a permission to implement

The human-carried recommendations are **directional**:
- R2 original video preservation, R3 fail-closed notes/images, and transcript independent attempt identity are higher value than cosmetic changes.
- Keep 250 MB cap with early refusal and original-safe text; show genuine video after repair.
- One action ≠ two unintended receipts; repeated independent save retains separate label/date.
- Only inspect one named failed receipt/backend job **read-only when owner-sourced reach permits**.
- Build 8 build and install remain distinct permissions. Existing phone captures untouched.
- Preserve synthetic tests as regression evidence; require all targeted preservation invariants to pass before product acceptance.

**Technical choice still needs owner/human acceptance:** the worker suggested *small archive-on-replace* to avoid schema change, while the human-carried recommendation prefers a stable capture identity and per-attempt identity. DAWT Design endorses **the observable result of stable, accessible prior versions**, not a particular database model or code diff. If a shortcut merely archives bytes without exposing them safely to people, it does **not** satisfy the full human reading/return contract.

**Design-specific hazards:** a beautiful video frame with an inoperative Play button; two “Transcript ready” items that mask one overwrite; empty-state photography covering a broken index; a success toast on a dropped busy import; a compound “saved twice” summary hiding two separate human contexts.

**Do not launch:** Feed redesign, Quiet Reader integration, automatic labels/projects, universal ledger, all-player rewrite or an additional media-generation pipeline from this fixture.

## 5. How DAWT Design receives the future fixed product

**Only after a separately authorised repaired build:** one source journey on the actual iPhone. A user chooses a real safe video; sees a clear 250 MB decision if applicable; watches the retained original; reads and returns between transcript attempts without losing an old passage; finds deliberate repeated saves under exact human labels; encounters a truthful unreadable/failed state in synthetic-only QA; and has a named, exclusive audio transport if/until that player repair is separately admitted.

Judge against Build 7:
- Did recognisability increase without pretending missing material exists?
- Did the source remain available when processing failed or changed?
- Could the person leave and return without remembering machine mechanics?
- Did any control imply a guarantee not supported by the provenance/receipt?
- Can the person find and compare old transcript versions without learning IDs?

If any answer exposes lost original bytes or overwritten text, **HOLD**, no cosmetic sign-off.

**DAWT Design's deliverable:** the human-visible contract and wording above; **not** the repair code, validation run, source/capture-ID policy or build activation.

**K​​eeper:** *Trust is not a badge. It is the quiet certainty that what you entrusted to the machine can still be found, accurately recognised and honestly experienced.*
