# DAWT DESIGN — TRANSCRIBE / LIBRARY × CAPTURE × SOURCE ENCOUNTER — INTERFACE CONTRACT 001

**Date:** 26 October 2026  
**Role:** DAWT Design — human–machine interaction, visual/material/perceptual design, typography, accessible discoverability and experience verification.  
**Originating human direction:** “Next is a focused technical repair pass, while DAWT Design develops the interface,” with specific protected media / reliable transcription / unified playback scope, and Build 7 Library/Media audit.  
**Recipient:** Transcribe owning project; [existing Issue #8](https://github.com/muntakabasit/TRANSCRIBE/issues/8).  
**Standing:** **HANDOFF-READY CANDIDATE UI CONTRACT / NOT APPROVED, CODED, RENDERED, DEPLOYED OR DEVICE-TESTED.** Original source material and technical implementation remain with their owners. No authority to change current Build 7, admitted work, human captures or unrelated products.

## 1. Source and governing bounds

**Preserve human-intended priority:** Library first; coherent Capture second; creative Feed and Quiet Reader integration held. DAWT Design shapes the human experience in parallel with, **not as commander of**, the Transcribe technical repair. No app code or rebuild from this document.

**Primary design evidence**:
- [DAWT Design Build 7 Human–Machine Experience Audit 001](./DAWT_DESIGN_TRANSCRIBE_BUILD7_HUMAN_MACHINE_EXPERIENCE_AUDIT_001.md) (read-only Swift and simulator screenshots).
- [Material Is the Doorway Interaction Study 001](./DAWT_DESIGN_TRANSCRIBE_MATERIAL_IS_THE_DOORWAY_INTERACTION_STUDY_001.md) (human's own material/recognisability instruction).
- [Lived Labels Encounter 001](./DAWT_DESIGN_TRANSCRIBE_LIBRARY_LIVED_LABELS_ENCOUNTER_001.md) (43 labelled records, 34 unique exact labels, 0 assigned destinations, as **human-carried original phone inspection**).
- [Independent Claude Build 7 Audit, separate source-authored report](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6415979029). **Read-only, zero test-reproduced defects**; it adds source-supported risks in preserving original imported video, corrupt store handling, id reuse, wrong capture provenance, silent errors and tab-lifetime playback. [RAT's independent bounded source reconciliation](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6415952788) confirms specific mechanisms; **no evidence any historical record was actually lost**.
- Current [human prioritisation](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6409559939): Library + Capture, Feed HOLD.
- The current build has working pieces: preserved share inbox, source/reference honesty, native previews for accessible media, reversible organisation, partial search and exact passage return. **Keep them.**

**Do not adopt** Claude's proposed “one encounter ledger”, global queue or tab removal as discovered architecture; those are candidate implementation choices for the owning engineering judgment. Design specifies observable **human requirements**, not new storage tables, service boundaries, worker decisions or code changes.

## 2. The experience invariant

> **The material itself should be the doorway—but it must not claim an action that the machine cannot perform.**

The five continuous questions are:
1. **What is this?** A real photo, video, original voice, actual words, human note or saved link.
2. **What has Transcribe really kept?** Link only? Actual media bytes? Photos reference? Exact transcript? Generated derivative?
3. **What can I do with it now?** The material itself leads to **Watch**, **Listen to original**, **Read**, **View** or **Open original**, only when each has a verified target.
4. **What would making something else change?** Get transcript, keep media, extract audio or retry are **consequential operations**, separate from passive viewing.
5. **Can I return without damage?** Exact capture/source identity and independent media/text positions; previous transcript versions never hidden by optimistic language.

**One preserved encounter may have multiple independently available representations.** No mandatory “choose mode” dashboard, and no global wall of every action on each item.

## 3. Concrete visual approach — Quiet Documentary / Material Archive (candidate)

This is a **Transcribe-specific** composition—not a DAWT master template nor a Quiet Reader skin.

- **Visual intelligence:** editorial clarity plus genuine human media. Faces and video stills may own the width; sound owns horizontal duration; reading owns type and space; notes retain their imperfect human voice. Do not make all five kinds look like identical rectangular cards.
- **Atmosphere:** build on the existing warm off-white/near-ink base and typographic ambition, but eliminate large ornamental hero copy when it delays the material. Real media should provide most of the expressive colour. No fixed accent should visually compete with source photography.
- **Hierarchy:** 1 dominant material encounter at a time; 1 primary intention; no competing search doors; secondary source operations behind a discoverable contextual disclosure.
- **Geometry, as *study values* not code mandate:** at approximately 390pt wide, content can have roughly 16–20pt side air; a real retained 16:9 video uses its natural aspect; copy excerpts should be limited to two–five readable lines with an unambiguous Read target; compact audio target should be comfortable to touch. Do not bind to hard-coded pixel dimensions; account for iPhone safe areas, large accessibility text and media orientation.
- **Typography:** large editorial heading for *Library* if useful at first arrival, smaller after scrolling; readable passage text with native font scaling; a restrained sans for metadata and actions. Contrast and colour must survive Dynamic Type, high contrast and light/dark preferences. Source design audit found the candidate `#888888` small-text token on `#F9F7F4` at approximately 3.32:1; do not treat that as acceptable normal-copy contrast.
- **Motion:** only for orientation and state changes, not to imply false progress or encourage scrolling. Revealed controls may gently enter, but no motion should move a reading anchor or conceal an error. Honour Reduce Motion.
- **Language:** ordinary exact verbs; “Original audio” instead of anonymous headphone icon; “Saved link” instead of “Video saved” when bytes are missing; “Transcript available” instead of “Verified transcript”.

## 4. Screen A — LIBRARY / where the human returns

**Initial view should answer, without scrolling through a manifesto:** “Can I find and open the material I remember?”

```
┌───────────────────────────────────────┐
│ LIBRARY                         [⋯]   │
│ [Find words, media, your labels…   ⌕] │
│                                       │
│ Continue — only when actual place    │
│ [genuine last excerpt or visual]      │
│                                       │
│ Your material                         │
│ ┌───────────────────────────────────┐ │
│ │  ACTUAL VERIFIED VIDEO FRAME      │ │  TAP IMAGE + PLAY → WATCH
│ │                   [ ▶ ]           │ │
│ └───────────────────────────────────┘ │
│ Human label · real source/date         │
│ “Genuine saved transcript passage…”   │  TAP EXCERPT → READ
│ Original audio [▶]   01:42            │  TAP AUDIO → LISTEN
│                                       │
│ [real audio waveform / play, if held] │
│ Human label · recorded duration       │
│                                       │
│ Actual image / actual held words ...  │
└───────────────────────────────────────┘
```

**Rules:** All source representations on an item are separate, correctly hit-tested direct targets; don't wrap everything in one reader-first NavigationLink. A thumbnail may open Watch, while a real passage on *the same item* opens its reading anchor. The item has one source identity, not three unrelated rows.

**Search:** one clear field for titles, actual words, natural human labels, and source terms. Exact matches first; clearly marked possible matches for “Guy man”/“Guyman” and “Shadow taut”/“Shadow taught”, without renaming original labels or pretending they were assigned to a project. Existing search code is not yet robust fuzzy search; this is candidate acceptance work.

**Continue:** Show only when a stable saved book/passage/time actually exists. A previous audio/video playhead and the previous read passage are distinct. “Recently opened” alone must not be labelled “Continue listening at 03:42.”

**Availability:** Real video with bytes may show ▶; a saved URL preview must instead show “Open original” and truthful “Media not saved” indication. A Photos reference doesn't promise permanent local copy. Audio waveform requires actual peaks derived from actual stored audio—not a decorative universal wave shape. Image stack badge must count actual accessible images.

**Organisation:** real collection tiles contain the owner's real, explicitly collected media. An empty collection stays honest. No AI guess that a label like `Ofa Rick` is a destination or confirmed category.

**Secondary actions:** one reachable “More”/source detail affordance per item for versions, original link, organise, share, status and technical attempts. No compulsory Respond/Connect/Make row.

## 5. Screen B — CAPTURE / an understandable beginning and truthful receipt

**Capture home starts with the human's medium, not server terminology.**

```
CAPTURE
Bring something here.

[ Paste a link                          ]
[ Record something ] [ Choose media    ]
[ Write a note                         ]

After deliberate link entry:
Actual source identity/status (if identifiable)
[ Get transcript ]       [ Save link only ]
[ Keep source media ] ONLY if proven supported
```

**Controls are candidate anatomy**; actual approved intake capabilities/permission may constrain labels. Do not show “Download media” as broadly working on arbitrary social URLs.

**Submission states** (each must be supported by owner/repair evidence):
- **Draft only:** `Not saved yet` — preserve field content and original media reference.
- **Saved-source receipt:** `Link saved` or `Video kept` **only after the corresponding durable proof**. If only a URL was stored, do not claim the video is present.
- **Work requested:** `Transcription requested` — separate from completed result.
- **Work still underway:** `Transcribing` with known truthful progress; “Checking status” if uncertain. Don't display a fabricated percentage.
- **Output available:** `Transcript available` with clear Open in Library.
- **Failure:** `Link saved. Couldn’t get audio from that source.` only where server evidence supports that exact cause; otherwise `Couldn’t transcribe from this link`, with **Choose a downloaded file** / **Try again** / **Open original** and technical details behind disclosure.
- **Unknown state:** `Couldn’t confirm the result. Your source/draft is preserved.` only if actually preserved; never erase text on ambiguous completion.
- **Reprocess:** until owner proves transcript versions preserved, don't expose a frictionless action that can overwrite an earlier result.

**Imported video bug boundary:** Claude/RAT static audit shows the present video file path converts video to temporary `.m4a` **before** preservation. The UI must not represent that audio derivative as a retained original video. Once engineering proves proper original-byte preservation, the Library's Watch affordance becomes eligible. This is a dependency, not a Design permission to repair.

**Labels:** optional, natural free text, potentially a full thought, and never interpreted as sending material to another project. Provenance records must truthfully distinguish direct Capture from Share Extension.

## 6. Screen C — SOURCE / an authentic, connected experience

```
← Library       [Human label / source title]       [⋯]
Real preserved source, matched to its true identity

IF VIDEO AVAILABLE:
  [actual retained video, full comfortable ratio]  ▶
  [Read transcript] [Listen to original] where available

IF AUDIO AVAILABLE:
  [source name] Original audio — duration & transport
  [Read transcript] where available

IF TEXT AVAILABLE:
  [actual words as a dignified reading passage]
  [Watch] [Listen to original] only when verified

IF IMAGE AVAILABLE:
  [actual image / true stack] tap/zoom/swipe

IF LINK-ONLY:
  “Saved link · media not kept”
  [Open original] [Choose local file] where appropriate

Details (behind ⋯):
  Source and history; real attempts/versions; user's note/label;
  inspect quality; share/organise; explicit *new* processing where safe.
```

**Do not make a permanent five-button material selector**. When in Watch, video comes forward and words recede; in Read, words occupy the screen; in Listen, a named original recording owns transport. Every mode returns to the *same* source without losing its own independent position.

**Audio ownership contract:** A single **human-identifiable currently audible item** with source title/label, “Original video audio”, “Original recording”, “Extracted original audio” or future “Generated reading” (future capability held). Only one audible owner at once, automatic pausing before new transport, route/phone interruption handling, meaningful resume. This is a human outcome contract, not a mandate to build a novel playback framework instead of adapting AVPlayer/state already present. “Listening” without source identity is forbidden.

**Transcript integrity:** Each distinct transcript attempt/version retains its stable identity and provenance; the interface can show “Current transcript” but cannot delete the previous original by switching “current”. A pending retry may not replace the visible previous words until verified as a new version. An image/field-note index read/decode failure must not become a “successful empty Library” UI that invites rewriting the store.

## 7. Interaction state matrix for actual iPhone design QA

| Fixture | Main material | Primary action | Support state | Not permitted |
|---|---|---|---|---|
| Verified retained video + transcript + original sound | Actual frame with ▶, genuine words and distinct audio | Watch direct / Read passage / Listen original | Separate positions, one playing owner | Frame tap opens reader by default; competing audio |
| Imported video with original bytes absent (current code risk) | Actual preserved *audio* / source description and capability limits | Listen if actual bytes held; otherwise source-link action | “Video not kept” | Fake playable video thumbnail |
| Link-only social source | Actual original link preview if available with explicit badge | Open original | Save proof and specific retry | “Video saved”, download implied |
| Existing transcript, new job attempted | Old visible version | Read original result | Processing as a **new version** | Silent overwrite/retranscribe mutation |
| Failed URL, working local-file candidate | Preserved URL and actual prior attempt status | Open original / Choose downloaded file | Precise source-specific recovery, not guessed backend cause | “No sound in this video” if remote fetch alone failed |
| Audio / video switching | Real identified media source | Play/stop/resume | One audio owner, interruption safe | Anonymous Listening rail / ghost audio |
| Human note + image index unreadable | Honest “We couldn’t open saved items” | Non-destructive recover / contact support where available | Never auto-initialise over unreadable prior bytes | Empty Library presented as fresh success |
| Long user label | Original exact label | Find / inspect source | Wrapping text, accessible search | Forced folder, fake project assignment |

## 8. Designed comparison to judge, not another conceptual redesign cycle

**Baseline A:** Actual Build 7 on phone/simulator with a small owner-approved, non-sensitive real source, preserving current stores. Record what genuine picture/text/audio are visible, which target Watch/Read/Listen actually opens, and what is preserved.

**Candidate B:** One design-reviewed Library item and one Source encounter using **the same real data** and the above interaction semantics. No generated fake thumbnail or imported social-personal media. Show an honest URL-only variant. Produce one Capture receipt state with an independently confirmed result.

**Observation questions:** Could the human recognise item before reading a title? Can a person tap the visual and perform intended action without navigating through backend terms? Can they tell link saved from media saved, original audio from generated voice? Do they accurately understand outcome of a failure? Could they return to the same source/reading passage and playhead? Can they do it with VoiceOver, large type, interrupted recording and reduced-motion?

**Fail conditions:** lost original bytes, prior transcript replacement, playback ambiguity, false readiness, source-overwriting recoveries, unreadable tiny labels, duplicate search doors, action overlays obscuring human faces, lack of original-source exit.

**Human judgement:** A/B against current Build 7 must decide whether the new experience genuinely reduces compensatory mental work while preserving source and voice.

## 9. Receiving / build dependency table

| DAWT Design design deliverable | Technical evidence needed before accepted implementation | Owner |
|---|---|---|
| Playable video frame acts as Watch doorway | Original imported video bytes retained and re-openable | Transcribe technical owner |
| Actual waveform + named Original-audio transport | Verified retained audio, real duration/waveform data where offered; global player ownership | Transcribe technical owner |
| Transcript passage acts as Read doorway | Stable transcript versions and passage IDs / exact return across retries | Transcribe technical owner |
| Source provenance/status labels | Receipt and source-type/status API/records grounded in actual outcome | Transcribe technical owner |
| Source-first note/photo Library surfaces | Fail-closed field-note/image index storage and real image access | Transcribe technical owner |
| Unified Capture success/failure visual states | Failed-link/file repair evidence, durable outcomes, safe retry identity | Transcribe technical owner |
| Final premium UI acceptance | Same-source real-device comparison incl. VoiceOver, Dynamic Type, interruptions | Human + owning project + DAWT Design |

**No destructive optimistic migration.** If a technical capability is not yet repaired, design the honest bounded fallback now, not a misleading button.

## 10. Decision requests, exactly bounded

For **Transcribe owner** (not DAWT Design to freeze):
- Confirm whether a source encounter may contain multiple distinct submissions from the same URL, rather than equating URL with identity automatically.
- Decide whether hidden Feed remains a held tab or is not displayed in the next user review. Either is a product decision, not proof of an implementation defect.
- Define genuine edit/remove/archive of preserved records; do not adopt destructive deletion as an icon-only flourish.
- Authorise one *real safe source* for the A/B comparison under an explicit UI-test scope.

For **DAWT Design** after technical return: finalise one screen for Library, one for source encounter, and one for Capture; compare with the actual installed phone in normal light and high-contrast/large text. Critically reject its own proposals where the existing interaction is simpler.

**Not carried over:** creation of Feed, generative content, social account integration, Quiet Reader read-aloud, project worker assignment or automatic publishing.

**Keeper:** **The material should be recognisable before explanation. Its controls must tell the truth. Its original must never be sacrificed to make the interface look successful.**
