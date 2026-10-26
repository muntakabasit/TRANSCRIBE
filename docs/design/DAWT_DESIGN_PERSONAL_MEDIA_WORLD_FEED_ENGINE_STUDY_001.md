# DAWT DESIGN → TRANSCRIBE — PERSONAL MEDIA WORLD / FEED ENGINE STUDY 001

**Date:** 26 October 2026
**Author / local responsibility:** DAWT Design (composition, typography, visual perception, interaction, motion, experiential study)
**Receiving project:** Transcribe, [PERSONAL SIGNAL FEED Issue #8](https://github.com/muntakabasit/TRANSCRIBE/issues/8)
**Human origin:** User supplied an example transcript of four layout devices ("One center product", "split type", "circle crop", "frame over photo"), linked that kind of donor and Quiet Reader's source→voice experience to a personal AI media feed, and asked about ingestion schema, ranking, and generated feed cards with optional Reddit/Substack/GitHub/social media.
**Standing:** **SOURCE-BASED DESIGN SPECIMEN / NOT AN ADOPTED ARCHITECTURE, CONNECTED ACCOUNT, MODEL SERVICE, IMPLEMENTATION ADMISSION OR ACCEPTED UI.** No personal media bytes or account tokens transferred.

## 1. Recover the original undertaking, not a generic recommender

The [original owner issue #8](https://github.com/muntakabasit/TRANSCRIBE/issues/8) distinguishes source custody and rediscovery; it rejects infinite scroll, attention metrics, identity inference, fabricated relations and broad private-history embedding. [DAWT Design's first-person personal-media-world pressure](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6275794810) rejects CARD→CARD→CARD and proposes orienting by REDISCOVER / CONNECT / CONTINUE / COMPARE / PLAY / BROWSE. [DAWT Design voice/original distinction](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6276049392) keeps original human audio separate from generated reading or commentary. [26 October Ofa Jack human correction](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6405861231) explicitly proposes moving current Feed's chronological record-list strengths into Library and turning Feed into a creative source-grounded AI media experience.

**Do not conflate:**
- CAPTURE: preserve a person's exact original encountered material, URL, time, status, provenance.
- LIBRARY: complete usable record of owned/saved originals and honest missing/restricted/failed states.
- FEED: a **finite, composed encounter** with selected real material that may offer comparison, rediscovery, sound, video, animation, design study, or simply the original itself.
- DESIGN: can study visual relationships and author/edit a source-preserving composition for an admitted undertaking; cannot decide which private project receives material or which source deserves accepted truth.
- Flow-KM: if retrieval/continuity is applicable, its role remains memory/retrieval, not feed-governance or permission. Yaro/capture cannot silently rank/promote. Belawu governs crossings; owner and human decide consequence.

The pasted initial proposal's 10–20 daily AI summary cards + blanket embeddings are **not our first fixture**. Rich media generation must earn its cost and trust by genuinely changing an encounter.

## 2. The smallest useful ingestion schema (CONCEPTUAL, NOT LIVE CODE)

**Keep five distinct objects, never one giant source/card record.** Illustrative field names:

```text
SOURCE (immutable encounter anchor)
  source_id
  origin_kind: human_saved | explicitly_imported | permitted_external_discovery
  modality: transcript | image | clip | audio | page | repo | note
  original_locator: local_ref / URL / platform_item_id
  original_content_hash? (when actual bytes held)
  source_author?; source_date?; captured_at
  access: locally_available | remotely_reachable | url_only | denied | missing
  rights: inspect | quote | transform_privately | publish (separate permissions)
  owner_scope / permission_ref
  source_text_segments? {original_words, start_ms?, end_ms?}
  user_annotation_ref?
  version / removal_or_disconnect_state

OBSERVATION (attributed, reversible interpretation)
  observation_id, source_ids[]
  kind: original_quote | human_note | visual_mechanism | model_hypothesis
  statement, evidence_spans_or_regions[], uncertainty
  asserted_by: human | model | original_author
  model_version?; verified_by_human?

RELATIONSHIP (NOT THE SAME THING AS SIMILARITY)
  relation_id, source_ids[]
  proposed_connection
  standing: source_proven | human_noticed | machine_suggested | disputed
  reason, counterpoint?, allowed_transfers[], rejected_reason?

MEDIA_PROJECTION (generated representation, not historical source)
  projection_id, source_ids[], observation_ids[], relation_ids[]
  medium: original | split_view | image_essay | motion_study | audio_discussion | other
  storyboard: scene_order + source_pointers + duration + caption/voice provenance
  voice_origin: original_human | ai_narrator | none
  generation_status: proposal | draft | made | checked | rejected
  model_or_tool_id?, cost_estimate?, export_ref?, checksum?
  attribution / rights_review / human_review
  reversible_to_original: true

FEED_ENCOUNTER (session view, never custody)
  encounter_id, user_chosen_orientation, eligible_source_scope
  selected_projection_ids, selection_reasons[], visibility_status
  feedback: keep | open_original | compare | not_useful | finish
  start_place? / return_place?
```

**Trust boundaries:** Original source raw material stays in source custody. A visual description is a derivative. An embedding is an optional retrieval index of a permitted representation, NOT a replacement for a source nor a licence to retrieve all history. A link saved is not evidence its video bytes or transcript exist. A source title's similarity to a project does not route that source to the project. Generated frames are NEVER labelled original screenshots, historical speech or footage.

**Right-to-disconnect/deletion:** Social-source pull is scoped, source identities and derivative references retained appropriately without keeping withdrawn inaccessible copies contrary to platform rules. Keep different flags for “can inspect”, “can transform privately” and “can redistribute”; generative transformation and publication are separate.

## 3. Ranking: temporary orientation + safe candidate selection

**Do not optimise watch time, compulsive return, likes, streaks or implicit personality.**

First choose one temporary human orientation:
- REDISCOVER: encounter one earlier source anew;
- CONNECT: inspect a suggested cross-source relationship;
- COMPARE: test differences/contradictions;
- PLAY / LISTEN: spend time inside original media or an attributed generated interpretation;
- MAKE / DESIGN STUDY: create a bounded composition from authorised material;
- JUST BROWSE: see original media without compulsory AI.

Then:
1. **Eligibility gate (non-negotiable):** source selected/authorised; original retrievable or limitation shown; relevant media rights and privacy scope; no disallowed social-data access; source and generated commentary marked distinctly.
2. **Candidate generation:** source-first returns; human-marked pair; explainable near/distant connection; one feasible storyboard; optional external counterpoint if explicitly admitted.
3. **Transparent bounded score**, not purported objective importance. Example weights for a user-requested MAKE/DESIGN-STUDY session, each axis 0–4:
   `3 × task_fit + 2 × source_strength + 2 × presentation_gain + 1 × meaningful_surprise − 2 × redundancy − 1 × production_cost`.
   Rationale must name actual source excerpts or visual regions and say why **this medium** adds value. **No fabrication of relevance where evidence is missing.**
4. **Composition diversity:** One original-led encounter; at most one relation/comparison; at most one generative piece if it genuinely earns place. Three sources can form one multi-part encounter, not necessarily three cards.
5. **Finite ending:** open original / annotate / keep / discuss / close. “Nothing new worth showing” is valid. A dismissed item remains in Library.
6. **Feedback has narrow meaning:** `not useful` is explicit feedback on one presentation/connection, not rejection of the source; `linger` is not evidence of preference; `keep` is not consent to publish or assign work.

**Human review tests:** did we accurately preserve sources? Did juxtaposition reveal anything? Did a motion treatment genuinely help? Did cost improve insight? Could the user distinguish commentary from their own original voice? Could they leave cleanly?

## 4. First generated feed experience — ACTUAL TRANSCRIPT SOURCE, PROPOSED STORYBOARD

**INPUT A / user-provided text (actually visible in this conversation):** four described design approaches: centred product, split typography, circle crop, frame over photograph. The source quotation stays preserved with its own phrasing; no original audio asset is claimed available.

**INPUT B / gallery screenshots:** discussed by human; exact uploaded visual assets, source identities and third-party reuse permissions **not re-attached/verified for this artifact**. Treat as candidates, NOT already ingested.

**INPUT C / GitHub & outside essays:** possible donor. No exact permitted repo/post/URL in this encounter, no verified quote or current-rights licence. Do not invent specific linked articles, social engagement or source claims.

### The rich Feed experience (not stacked summary cards)

**Opening:** One dominant real user-supplied visual or simple authored typography specimen. Heading: `WHAT MAKES A LAYOUT FEEL MODERN?` Subtitle: `Four mechanisms described in one saved transcript.` Clear provenance tag `FROM YOUR SAVED WORDS`.

**Movement 1 / SPLIT TYPE (8–12 seconds, illustration-only):**
- Original transcript words remain available.
- Two large typographic words separate spatially.
- A **clearly labelled editorial demonstration graphic**, *not an invented original gallery image*, enters the gap.
- Optional generated narration explicitly `AI EXPLANATION`, NOT `ORIGINAL AUDIO`; plain text remains available.
- Human can pause, scrub or show original.

**Movement 2 / FOUR MECHANISMS (side-by-side):** comparative compositions, using the SAME approved input content and the SAME real source image when available. Any cropping must preserve people and critical content; if no suitable actual image, that comparison is held.

**Movement 3 / CHALLENGE:** `Which mechanism would help a single product? Which would fail for a community film?` This is an attributed design hypothesis, not established user preference or a proven rule.

**Outcome:** `OPEN THE TRANSCRIPT` · `COMPARE` · `KEEP THIS STUDY` · `I'M FINISHED`. **Do not** automatically create a task in DAWT Design, Quiet Reader, Ofa Jack or AutoCut. The human may explicitly elect to carry a bounded selected study across a receiving boundary later.

**Sample user-visible truth labels:**
- **ORIGINAL TRANSCRIPT** — historical/source text;
- **DESIGN STUDY** — authored interpretation;
- **GENERATED VISUAL** — synthetic/illustrative rendition;
- **AI COMMENTARY** — new source-derived narration;
- **SOURCE UNAVAILABLE** — URL or screenshot held without the actual media;
- **RELATED?** — an uncertain, rejectable link.

## 5. Provider connectors — graduated scope, not “all accounts already logged in”

- Manual Share / curated sources, original-authorised local assets and GitHub read access first.
- Public Substack publication RSS can be browsed via publication `/feed` where provided; it does not yield private newsletters or saved reading history.
- Reddit Data API requires appropriate approval/terms/limits for intended use, and removed/deleted content handling; embeddings/AI modelling rights must not be presumed.
- TikTok Display API `video.list` describes the authorised user's public posted videos, not their full saved/liked/For You browsing history.
- Other social accounts require per-provider APIs, consented data export or deliberate manual shares. A logged-in app does not supply Transcribe with raw sessions, credentials, subscription feeds or redistribution rights.

Official source context: https://developers.tiktok.com/docs/en/display-api-overview ; https://support.reddithelp.com/hc/en-us/articles/14945211791892-Developer-Platform-Accessing-Reddit-Data ; https://support.substack.com/hc/en-us/articles/360038239391-Is-there-an-RSS-feed-for-my-publication

## 6. The first real experiment (candidate; no implementation authority)

**3–5 actually selected and available original sources; only two/three presentation forms:**
- **A / RE-ENCOUNTER:** original source in a full-bleed/source-first layout;
- **B / INTERPRET:** one rigorous design illustration/motion prototype on the *same* original source set;
- **C / CONNECT:** optional one explainable link to a separate permitted source (human can reject).

Compare against current Library metadata view without modifying it. Measure source return, meaning gained, visual quality, accurate quotation, rights/voice attribution, joy without compulsion, creation cost, readability/assistive access, and satisfaction with closing. Reject if generated media becomes invented filler or hides the source. The original Transcribe capture/share fixture and human-reported issues must not be disturbed.

**Production boundary:** DAWT Design contributes source-grounded editorial hierarchy, media-form/interaction specimens and critique. Transcribe owner defines product capability and Library/Feed boundary; Yaro/Flow-KM/Belawu preserve their distinct ingestion/retrieval/decision duties; Ofa Jack executes only separately admitted work. **No capture, provider login, model generation, source export, app code, runtime or governance state changed in this contribution.**

**Keeper:** *The library holds what happened. The feed may make it newly perceptible. A beautiful invention must never pretend to be the source.*
