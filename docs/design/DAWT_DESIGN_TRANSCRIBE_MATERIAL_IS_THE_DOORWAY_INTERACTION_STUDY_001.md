# DAWT DESIGN — TRANSCRIBE / MATERIAL IS THE DOORWAY — INTERACTION STUDY 001

**Date:** 26 October 2026  
**Original author / responsibility:** DAWT Design — human–machine perception, hierarchy, interaction, typography, material form, accessible affordance and motion.  
**Human source:** User's direct current formulation: “We're asking words and menus to do too much. A thumbnail, waveform, play button or transcript excerpt could make the material—and what you can do with it—recognisable immediately.” Human gave exact proposed material grammar for Video / Audio / Transcript / Images / Collection.  
**Owning recipient:** Transcribe Library-first and unified Capture, [existing Issue #8](https://github.com/muntakabasit/TRANSCRIBE/issues/8).  
**Parent audit:** [DAWT Design Build 7 Human–Machine Experience Audit 001](https://github.com/muntakabasit/TRANSCRIBE/blob/main/docs/design/DAWT_DESIGN_TRANSCRIBE_BUILD7_HUMAN_MACHINE_EXPERIENCE_AUDIT_001.md).  
**Standing:** BOUNDED NEW USER-GROUNDED DESIGN REFINEMENT / **NOT** adopted interface specification, code/Build 8 authority, human field acceptance, generated images or media ingest. Independent Claude source audit is separately commissioned and must finish its cold pass before cross-comparison with this or other Design direction.

## 1. The shift: from record chrome to material affordance

**Working design statement: THE MATERIAL ITSELF IS THE DOORWAY INTO ITS REAL AVAILABLE EXPERIENCES.**

The Library currently has recognisable attempts at content-first design. But “content preview” and “direct action” are not necessarily the same. The source-reviewed Build 7 [LibraryWorkspaceView.swift] (installed isolated source) puts **LibraryMediaPreview(item:)** inside a **NavigationLink**, and **LibraryItemDestination** chooses **EncounterReaderView** whenever any passages exist, otherwise **EncounterItemView** and extracted-audio options. The source-review result is structural: for an item whose source is a video but whose transcript exists, **tapping its thumbnail region follows the row's reader destination**, rather than directly starting Watch. This is a designed interaction mismatch; it is not yet a physical phone mis-tap reproduced with a user.

**The point is NOT "delete text".** The point is an economy of meaning:
- Real material carries recognition.
- Interaction target carries likely next action.
- One short, truthful label distinguishes genuinely different media actions.
- Secondary controls hold organising, sharing, extraction, attempts, details and repair.
- The person can leave without making a note, connecting, making or classifying anything.

**No false affordances:** only a saved URL does **not** warrant a ▶ button implying retained video; a thumbnail from link metadata is a preview, not proof of downloaded playable media. No generic counterfeit waveform, fabricated content excerpt, fake stacked image count or synthetic first frame.

## 2. Five material types and their real contracts

| Material | Source-grounded foreground | What the person expects from a direct gesture | Honest absence / fallback | Nearby secondary action |
|---|---|---|---|---|
| **Retained video** | Real source frame, correct aspect, visible ▶ overlay, duration only if actual duration known | Tap real video frame → **Watch** actual retained video, with original sound and return | URL-only/Photos unavailable: visually distinguish preview from playable media; label “Open original” or access needed, never play overlay when can't play | Read transcript, Listen to original, Share, Source |
| **Recorded / retained audio** | Actual verified waveform if generated from original bytes; duration; clear ▶/pause/seek position; a distinctive human label | Tap ▶ → **Listen to original**, one identified active transport | If bytes missing: “Audio not available” without made-up waveform or fake duration; can open original if URL permits | Read transcript, Share, Extract only if needed, Details |
| **Transcript** | Real contiguous passage from actual saved text, typographic rhythm and visible continuation when truncated | Tap passage → **Read** with real passage anchor / precise return | Failed or merely requested: no fake quote, state says “Transcript unavailable” or “Processing” with truthful next move | Original recording, Open source, Versions, Share |
| **Images** | Real image itself, protected crop/subject, native orientation; stack/number only where multiple actual attachments exist | Tap image → **View** with zoom and swipe if multiple verified images | Link preview ≠ retained image; Photos reference unavailable has access/retry cue, not generic photo that looks stored | Share, Source, Add note |
| **Collection** | Small, purposeful arrangement of **real, user-placed contents**; never fake generated samples or inferred category | Tap arrangement → enter the actual collection and its constituent materials | Empty collection: purposeful empty label, not decorative stock collage | Rename/organise, manage items |

**Important caveat:** A source is not exclusively one type. One saved capture might legitimately offer original video, original audio, transcript, image/cover and a human note. The visible material should foreground the most useful actual representation **in that moment**, while adjacent short modality affordances permit other real ways to encounter the same source. No fake single-format source identity.

## 3. The “one source / several actions” interaction grammar

**A. At Library overview:** Choose the primary visual presence from available actual bytes/words, respecting human label. If the source really is a playable video, the picture and ▶ are an explicitly actionable target. If transcript passages exist, the excerpt is an independent **Read** target. These two targets may coexist on one item without a confusing nested-row tap. The design problem is gesture regions and source hierarchy, not a universal rule that every entire card opens the same view.

**B. At source encounter:** Let the current medium own the space. Watch → video frame + scrub/return; Listen → named source + playback; Read → words + exact return; View → image + fit/zoom. Contextual transition back to the source and previous place is always recoverable.

**C. When media is unavailable:** The most prominent thing is what **is** present: original saved link, label, screenshot reference, transcript (if real), or an intelligible saved request. Do not collapse this into a grey empty tile or invent a thumbnail. One clear recovery option, details behind disclosure.

**D. On changing modes:** Other modes are visible only when feasible, not via a globally repeated icon menu. The human should distinguish **Original audio** from **Generated reading** if/when future TTS exists. The latter **does not currently ship**, so it must not appear as available in Build 7. Playback modes need actual audio ownership; merely styling them together doesn't prevent simultaneous sound.

**E. On return:** One authentic source identity; keep mode-specific positions (source video playhead, extracted original audio time, reader passage). A tap on a passage opens that passage; a tap on video starts/resumes the real video. Switching should not silently reset either or rewrite a prior transcript.

## 4. Proposed low-chrome Library arrangement — one candidate, not freeze

```text
LIBRARY
Find my material              [search] [organise]

CONTINUE — only if a stored exact source/place exists
[real last-opened excerpt or source picture]  Continue

YOUR MATERIAL
┌────────────────────────────────────┐
│  [REAL VIDEO FRAME]           [▶]  │  <-- WATCH, if bytes exist
│  Human-saved label                 │
│  [REAL transcript sentence…]      │  <-- READ exact passage if present
│  Original audio  ▷   · 00:XX      │  <-- LISTEN, only if present
│  Small source/availability marker │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  ~~~ verified audio waveform ~~ ▶ │  <-- LISTEN
│  Original label · genuine duration │
└────────────────────────────────────┘

┌────────────────────────────────────┐
│  A real opening passage from       │  <-- READ
│  a transcript, not a title         │
│  manufactured by the system…       │
│  Original label                    │
└────────────────────────────────────┘

A collection may appear as a small verified-media arrangement.
```

**No need to force all material into rectangular cards.** The above only describes region ownership; use editorial spacing/real film aspect/true text width and selected native media controls appropriate to each material. Avoid unstable UI height shifts as delayed previews load (the earlier Design encounter had a real narrow-width geometry failure). Reduce multiple unrelated search icons/boxes to one coherent retrieval path.

## 5. The distinction between decoration, preview and action

A **visual preview** is content but not automatically an affordance. A **real affordance** must disclose the action it actually performs, and its hit target must be what the person expects:
- A frame with overlay ▶ should play **retained** video, not unexpectedly open a transcript because the whole row inherited a reader NavigationLink.
- A text passage should lead to that text location, not open a generic source details sheet.
- A waveform/▶ should visibly start listening and identify what plays, not generate/extract audio behind the scenes.
- A small image stack count should correspond to actual recoverable images, not number of source URLs or plausible thumbnails.
- A collection collage should be made from real **explicitly grouped** assets, not automatically attributed project labels.

**Avoid hidden-gesture dependence.** A short adjacent “Read”, “Original audio” or “Open source” is justified when a touch target or mode could be misunderstood. VoiceOver/keyboard have the same access and semantic controls, even if the visual treatment relies mainly on material. Hover isn't an iPhone affordance. Long press can expose secondary actions but must never be the only way to reach essential functionality.

## 6. Current Build 7 opportunities / risk register

**Existing sources already implement partial ingredients:**
- `Views/LibraryMediaPreview.swift`: local genuine image thumbnail, first video frame via AVAssetImageGenerator, selected Photos preview.
- `Views/LibraryWorkspaceView.swift`: scroll/list/grid and content previews; title uses label or actual passage; but one encompassing itemLink and reader-first destination.
- `Views/EncounterMediaView.swift`: video, audio and image rendering; distinct controls exist, but icon/transport semantics overlap.
- `Views/EncounterFeedView.swift`: text passage reader and saved position.
- `Models/EncounterSearch.swift`: exact/partial phrase retrieval, not robust approximate labels.
- `Views/CaptureWorkspaceView.swift`: link-first operations, rather than genuine source-first result states.

**What is NOT shown to exist:** a waveform renderer bound to verified retained audio bytes, a trusted multi-image collection/stack preview composer, a single all-player audio ownership service or true combined video/read target within one Library row. These are candidate parts to validate, **not claims already built or blanket justification for architecture refactoring**.

**P0 independent constraint:** current `SourceAudioWorkspace.swift` extracted-audio retranscription can reuse an existing ID and write same transcript path; [original audit](DAWT_DESIGN_TRANSCRIBE_BUILD7_HUMAN_MACHINE_EXPERIENCE_AUDIT_001.md). **Do not implement a new easy-to-tap “retranscribe” surface before version preservation is fixed and verified.** No historical data loss is asserted.

**Independent audit discipline:** [Human commission for separate cold Claude audit](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6415523191) is current. This Design addendum must be kept as a distinguishable source for **after** Claude's original blind findings, not used to direct or manufacture its independent observations.

## 7. One deeply discriminating first visual comparison

Do NOT redesign every Library item at once. Under owner admission, choose one real safe video capture for which source bytes, its original audio, transcript, source URL and permissions are actually verified. Compose **A** the unchanged Build 7 row and **B** a proposed source-led single-item presentation using the **same** material.

The user must be able to:
1. Recognise the original video **before reading a label**, but without fake play readiness.
2. Tap frame and Watch; tap real transcript excerpt and Read exact passage, **without a menu and without the wrong route**.
3. Tap a clearly identified **Original audio** play surface; see which source plays and ensure a different video/audio cannot continue simultaneously.
4. Return via the same original source to independently persisted media/text positions.
5. Open source detail and prove preserved versions and honest URL/source availability.
6. Increase Dynamic Type/VoiceOver and still distinguish targets by purpose, with accessible labels and hit areas.
7. See a URL-only variant: no false play/stack/waveform, only source and truthful recovery.

Record time to first successful intended action, route reversals, wrong-tap count, comprehension of source availability, and a natural user statement of what happened. Do not claim faster/better without a genuine encounter and baseline comparison.

**Failure of B** includes obscuring original media, making accessibility harder, presenting generated placeholders as source evidence, losing reader positions, exposing old overwriting risk more directly, or replacing the existing functioning share/capture system.

## 8. Bounded next work and authority

**DAWT Design:** owns this design mechanism proposal, authored visual hierarchy/gesture logic and comparative critique. **Transcribe:** decides accepted Library interaction and sources/permission. **Ofa Jack/Claude:** implementation only under separate current approved build/task admission. **Belawu:** authority at crossings. **Human:** decides what is clear, authentic and worth using.

**Current human priority** remains Library and Capture, Feed held. No app source, signed build, phone data, source attempts, screenshots, personal recordings, social account connectors or runtime focus changed by this document.

**KEEPER:** **The material should carry its own invitation. The system must make that invitation truthful, reachable and recoverable.**
