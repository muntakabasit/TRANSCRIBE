# DAWT DESIGN — TRANSCRIBE BUILD 7 / HUMAN–MACHINE EXPERIENCE AUDIT 001

**Date:** 26 October 2026 · **Auditing responsibility:** DAWT Design (human-centred interaction, typographic / perceptual / visual / experiential design).  
**Receiving:** Transcribe owning project, existing [Personal Signal Feed / Library-first Issue #8](https://github.com/muntakabasit/TRANSCRIBE/issues/8).  
**Standing:** **FIRSTHAND READ-ONLY SWIFT / SIMULATOR-SCREEN INSPECTION + SOURCE-ATTRIBUTED HUMAN FIELD REPORT + INDEPENDENT DESIGN ASSESSMENT.** Not physical iPhone UX acceptance, user research with a participant, implementation approval, accepted product specification, or code change.  
**Audience:** original Transcribe owner, Claude/Ofa Jack when independently admitted, DAWT Design and Studio, human artistic/product judge.

## 0. The central finding

**The app is no longer principally a transcription form, but its relationships still behave like separate transcription-era operations.**

It can preserve an encounter, resolve a URL, import media, transcribe speech, extract sound, display images, retain human labels and organise/return to reading. Several important capabilities are genuinely built. Yet the human has to reconstruct an invisible model of which parts belong to the same encounter and which operations have actually succeeded.

The desired contract is not “one pretty screen”: **ONE ENCOUNTER · GENUINE REPRESENTATIONS · AVAILABLE ACTIONS · VISIBLE CONSEQUENCE · RECOVERABLE RETURN**.

The essential human–machine relationship question is: **“What did I give you? What did you really preserve or make? What can I do with it now? Can I return without losing anything?”**

The deepest flaw currently is not colour, density or icons: **the interface's identity is organised more strongly around technical operations than around the person's preserved encounter.** Cosmetic restyling alone would conceal this mismatch.

### Decision ceiling / safety

**P0: Existing transcript version replacement risk.** The Build 7 extracted-audio “Transcribe audio” path selects the existing transcription ID when the item already contains a transcript; the storage writer atomically writes a dated JSON with that ID and replaces the in-memory item sharing the ID. **The code demonstrates a possible earlier-version replacement path; it does not prove a historical record was already lost.** Preventing that consequence matters more than any screen polish.

**Human priority as of today:** LIBRARY + UNIFIED CAPTURE; FEED held. Do not activate a source recommendation/media-generation system or social account connectors from this audit.

## 1. Exactly what I examined and did not examine

### Direct current Build 7 source, read only on the connected MacBook

Installed Build 7's preserved source tree:
\`/Users/abdulbasitmuntaka/DAWT_Transcriber/reports/TRANSCRIBE_CAPTURE_LIBRARY_SWEEP_20261026_001/ios/DAWT-Transcribe/\`

Read: \`Views/HomeView.swift\`, \`Views/LibraryWorkspaceView.swift\`, \`Views/CaptureWorkspaceView.swift\`, \`Views/EncounterMediaView.swift\`, \`Views/EncounterFeedView.swift\`, \`Views/EncounterSearchView.swift\`, \`Views/EncounterActions.swift\`, \`Views/SourceAudioWorkspace.swift\`, \`Views/LibraryMediaPreview.swift\`, \`Services/EncounterLibrary.swift\`, \`Services/EncounterPlayback.swift\`, \`Models/EncounterSearch.swift\`, \`Storage/EncounterStateStore.swift\`, \`Storage/LibraryOrganisationStore.swift\` and \`Storage/TranscriptionStore.swift\`. Inspected the \`saveVerifiedShareResult\` implementation in \`Services/ShareJobCoordinator.swift\` read-only.

**Reproducibility pins:**
- HomeView SHA-256 \`bf31583eadbc522b3913fb6f23e36c36ad2fa61a6c2e2c77c0186f7b7cad8d2b\`
- LibraryWorkspaceView SHA-256 \`2ad944ee4af625de66bffead7c2d5be46b2f542c7d198d60bd7f3dd0d23039dc\`
- CaptureWorkspaceView SHA-256 \`ecd88180a00515b4c59852b0f2ffbadb31290450fe075f0835340ac9f634dfcf\`
- SourceAudioWorkspace SHA-256 \`87a16d03f7d3c1193dce0abced12d381c31fe2ede141e4f510280530e5f74c06\`
- EncounterPlayback SHA-256 \`ddd1ea3d358410e99f3896217ee80b4fea266b3d9f90174be2e5def1d9ed0402\`
- EncounterLibrary SHA-256 \`b59cd213e386c619c50e95145b8d6d56052eb7728048adde57c26460ac2a36b7\`
- EncounterSearch SHA-256 \`ac2f7e668d7bdfe6686333df69605a5046f46cf7ff353a3d5244730f05ac75df\`

### Direct Build 7 rendered screenshot inspection

Examined \`current-simulator.png\`, all three \`screen-final/*.png\` screens and the \`screenshots-reviewed/*.png\` design-test screens under the same report root. They visibly represent:
- **Capture:** warm off-white large serif “Bring something into Transcribe”, first link block, copied-link and label/destination controls, muted primary Transcribe until link entry, long additional-actions link, and other input rows.
- **Library:** pronounced editorial serif heading, right-aligned small search and organisation glyphs, horizontal filter strip, a large **CONTINUE** specimen, “Your material”, source-status lines, lower three-tab navigation and an additional search field that appears at the bottom of the simulator under the navigation region.
- **Link options:** a native cool-grey sheet with “Add context”, Extract audio / Save link / Transcribe / Download video or image, and explanatory capability text. Buttons disabled in screenshot with empty link.
- **Search/keyboard:** bottom search entry with soft/rounded styling; actual very long pasted search string visible in synthetic simulator fixture.

**Important:** these are **simulator / authored fixture images**, not proof that the same composition is the exact current physical iPhone frame or that its fixture text is user's content. The “unrelated passage”, “studio deck” and GUYMAN Test labels shown are specimen placeholders, not evidence of the human's original records.

### Source reports read, attributed rather than treated as independent observations

- \`RETURN.md\`: signed Build 7 installed in place and launched after user-authorised installation, 86 unit/integration tests plus several separate native UI suites; pre-launch 2,045/2,045 app-owned files preserved byte-identically. Human aesthetic/phone-field acceptance remains pending.
- \`MEDIA_HARMONISATION_AUDIT_001.md\`: owner's source/data audit; 704 decoded transcripts / 313 shared captures in examined **pre-install backup**, not live phone totals; version collision, media/reader divergence, source-specific failure, audio-session identity and copy issues. This report was separately source-checked in part, rather than regarded as a new second set of user observations.
- [Human priority / source audit](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6409559939): Library and unified Capture before Feed.
- [Owner media safety reception](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6415112835): original issue plus source-verification severity and no verified historic loss.
- [Human-carried 43-label inspection and DAWT Design return](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6413649511): free human labels and zero assigned destinations; this Design audit does not reread original phone CaptureContext records.
- [Quiet Reader source vs rendition donor](https://github.com/muntakabasit/TRANSCRIBE/issues/8#issuecomment-6414744737): conceptual boundary, not an existing Transcribe read-aloud implementation.

**Not independently performed:** physical-phone taps or voice interaction, playback listening, dynamic-type/VoiceOver audit, actual provider failure re-run, GPS/contact/photo inspection, uninterrupted media playback, network trace, user test with participants, screenshot-perfect shipped appearance, source-file repair, UI testing, backend restart or live code change. No private source/media records copied to GitHub.

### Current focus and execution

MacBook \`BelawuOS/state/CURRENT_STATE.yaml\` read 26 Oct currently reports \`active_project: Transcribe\` but \`active_task: unknown\`, \`state_truth: unknown\`, and \`next_action_source: not_established\`. This **does not confer new implementation/admission authority**.

## 2. What the team genuinely achieved — do not regress

1. **Explicit user-aligned top-level places:** Library, Capture, held Feed exist as distinct SwiftUI sections in \`HomeView.swift\` (rather than all routes wired into a legacy Feed). Library is default.
2. **Content-led effort is real:** \`LibraryMediaPreview\` can display local image/video poster frames and explicitly chosen Photos references; \`EncounterLibrary.title\` favours real label or text over UUID.
3. **Preservation before processing exists in intake:** link and media work have tested durable routes; source-only and transcription intent can remain separate.
4. **Recall mechanics are meaningful:** \`EncounterSearch\` searches labels, source details and passage content; the reader stores a last-opened item and passage position; Libraries support reversible tags/collections and actual-date ordering.
5. **Backups/field discipline improved:** Build 7 install has preservation records; simulator UI and technical tests have been run.
6. **Source honesty appears in code:** Photos permission is not treated as “save entire camera roll”; unavailable remote link preview is labelled rather than silently replaced with invented bytes.
7. **Existing visual craft has direction:** restrained off-white, ink, editorial serif and useful negative space. Do not erase this because other surfaces need improvement.

These are real abilities, although some remain untested under actual interrupted human encounters.

## 3. Human–machine relationship model — what a great experience must carry

**A. CAPTURE / ARRIVAL:** Person encounters material elsewhere and chooses to preserve it. Machine's duty is to keep the intent and actual source, not to force project classification or explain its backend before intake.

**B. ACKNOWLEDGEMENT:** Source saved, request accepted, job processing, transcript produced, media retained, transcription unavailable and transfer failed are different truths. The machine must say *what happened* before it tells the person what operation to try next.

**C. MATERIAL CONTACT:** The person returns to the original's best available form—watch a video, hear original audio, read actual words, view an image. A technical status/UUID/url must not outrank the material itself.

**D. MULTIPLE REPRESENTATIONS:** Link, retained bytes, extracted original audio, derived transcript, human annotation and potential AI narration are related but **not interchangeable**. Their source/provenance and state remain legible.

**E. HUMAN CONTRIBUTION:** Label, note, suggested link, organisation or question can be left in natural language and may remain incomplete. Thought ≠ task; label ≠ project destination; saving ≠ endorsement; duration ≠ preference.

**F. LEAVE / RETURN:** The machine retains an exact recoverable place when actually stored, distinguishes reading passage from video/audio playhead, and does not hijack or silently restart processing after a person leaves.

**G. FAILURE / RECOVERY:** No usable audio *in fetched media* is not a claim about the original social post or separately downloaded file. Preserve the encounter, compare attempt provenance, present one responsible next action, keep diagnostics inspectable rather than dominant.

**H. TRUST / NO INVISIBLE CONSEQUENCE:** New processing attempts must not overwrite older human-retrievable results; photos access is not capture consent; a “For” entry is not delivery; two audio sources must not unexpectedly speak over each other.

These are product obligations, not aesthetic tokens or hypothetical architecture that supersedes Transcribe's current stores.

## 4. Expert heuristic scorecard (qualitative, NOT usability-test measurement)

Scale: **0 = seriously undermines relationship; 5 = strong/field-grounded.** Ratings are **DAWT Design provisional expert judgements** from source and simulator, not quantitative participant scores.

| Dimension | Provisional rating /5 | Rationale |
|---|---:|---|
| Source custody intention | 3.5 | Strong preserved intake/backup effort; transcript-version collision prevents high trust |
| Human orientation | 2.5 | Library/Capture now named, but nested route/toolbar ambiguity |
| Content recognisability | 3 | Genuine previews/excerpts where available; fallbacks and technical statuses still dominate some rows |
| Operation/consequence clarity | 1.5 | “Save / transcribe / extract / listen” imply overlapping or hidden differences |
| Cross-media coherence | 1.5 | Reader vs viewer destination bifurcation; unrelated players |
| Return and continuity | 3 | Reading and media positions exist; not unified or field-proven under interruption |
| Recovering after failure | 2 | Source kept, but backend language and divergent link/file paths put diagnostic burden on human |
| Human vocabulary and identity | 2.5 | Exact labels preserved; search not yet naturally tolerant; project “For” can mislead |
| Perceptual hierarchy and graphic craft | 3 | Credible editorial direction; chrome/search/status and some contrast/density problems |
| Accessibility robustness | UNKNOWN | Dynamic Type/VoiceOver/high-zoom evidence insufficient; fixed token sizes and font treatments raise test pressure |
| Media/voice provenance | 2 | Source audio exists, generated reading not; “Listening” bar lacks identity |
| Overall human relationship | **2.5 candidate** | Good rebuilt foundation, but still asks user to interpret system structure |

Do **not** convert scores into acceptance numbers or a rank against unrelated apps. The purpose is to target pressure, not simulate user research.

## 5. Findings register — evidence, harm, correction and ownership

### HM-01 — P0 / SAFETY: existing transcript can be replaced by re-transcription

**Source-verified:** \`Views/SourceAudioWorkspace.swift\` chooses \`old.id\` if \`item.content\` is a transcript; \`ShareJobCoordinator.swift:201–211\` writes \`{id}.json\` (atomic per write) and replaces in-memory same-ID result. Atomicity does not preserve history of prior bytes. **No historical loss established.**

**Human harm:** Reprocessing can silently take away a valuable earlier rendering of someone's encounter, violating recoverability. **No amount of UI treatment compensates.**

**Required owner/engineering disposition:** Do not encourage reuse of “Transcribe audio” on an existing transcript until version/attempt design is safely admitted; preserve old transcript independently, source identity and attempt linkage, prove same-file and interruption/failure paths. This audit **does not write a patch or authorise a build**.

### HM-02 — P1 / STRUCTURAL: the same capture opens different worlds

**Observed in source:** \`LibraryItemDestination\` and \`EncounterSearchView\` open \`EncounterReaderView\` whenever passages exist; without passages they enter \`EncounterItemView\` with \`SourceAudioWorkspace\`. Reader route drops immediate media/view/extraction affordances, while the source-audio sheet can still exist separately.

**Human harm:** A successful transcription can make the original *appear to move or disappear* from the human's immediate experience. The system's own representation precedence decides what a capture is.

**Design correction:** One recognisable capture context first; **Read / Watch / Listen to original / View image / Open original** are source-conditional capabilities of that same context. A reader may take the whole screen after entering Read, but an intelligible return to the same source must be simple. Search enters with the same route and correct passage anchor.

**Owner:** Transcribe product + engineering for actual navigation; DAWT Design for hierarchy/transition.

### HM-03 — P1 / SEMANTIC: playback icons conceal distinct meanings

**Observed in source:** waveform plays local recordings; headphone icon may mean “Listen without video”; ellipsis offers extraction/share; “Source audio” toolbar opens a sheet; generic reader/Watch actions differ.

**Human harm:** Person must translate icons into backend processing/media distinctions. “Headphones” could reasonably mean listen to original, extracted copy, TTS reading or media-without-picture—those are not equivalent.

**Design correction:** Visible verbs attached to what **exists**, not icon guessing:
- **Watch** (real video bytes);
- **Listen to original** (authentic audio/extracted original soundtrack);
- **Read transcript** (machine-recognised source-grounded text);
- **Open original** (external locator);
- **Extract audio** (a new derived file, separately named);
- **Read aloud** only if a separately implemented, attributed, quality-checked generated reading exists in future.

No mandatory five-button wall when only one form exists. Modes arrive contextually; destructive/consequential actions are not mislabeled as passive listening.

### HM-04 — P1 / TRUST: “Listening” is anonymous and multiple players are independent

**Source:** \`LibraryWorkspaceView.swift:112–120\` mini rail shows only “Listening”, one play/pause and close; \`EncounterPlayback.swift\` stores sourceKey internally and writes the Now Playing title “Transcribe”, not the clip identity. \`LocalMediaEncounter\` and \`PhotosInlineEncounter\` instantiate \`VideoPlayer\` independently; \`EncounterContributionView\` can create another \`EncounterPlayback\`.

**Human harm:** It is hard to tell *what* is speaking, and there is a plausible risk of overlapping audio. Independent sessions also increase the burden of remembering which player preserves which playhead. **Actual overlapping playback was not reproduced here.**

**Design correction:** One identifiable audible focus at a time. A compact transport with human-readable actual source label/title, **Original audio / Video / Generated reading** identity, position and explicit destination; pause old audio on new start. Video, extracted audio, transcript reading and later TTS keep separate positions and distinct custody. Persisted positions must not be asserted to sync unless real alignment exists.

### HM-05 — P1 / ERROR: technical progress strings invade source experience

**Source:** \`LibraryWorkspaceView.swift:157–162\` uses \`jobs.progress[receipt.id]?.message\` and capture failureMessage directly as row status, with \`.lineLimit(3)\`. The owner-supplied IMG_4199 phone screenshot reportedly displays such a prominent failed-link diagnostic; Design did **not** reread that phone image itself.

**Human harm:** Instead of seeing the material or its real status, the user faces processing language they must diagnose. Error proximity changes meaning: “no usable audio” for the fetched response can wrongly feel like a judgement that the actual video is silent.

**Design correction:** Main row may say **Transcript ready**, **Request saved**, **Still processing**, **Couldn't transcribe this source**, **Saved link only**. On opening it, show exactly where failure occurred *when known* plus clear recovery: **Try the link again / Choose a downloaded file / Open original / See technical details**. Do not rewrite missing diagnostic fact as reassuring success.

### HM-06 — P1 / MEMORY: search is findable, but duplicate and incomplete in behaviour

**Observed:** Library has native \`.searchable\` *and* top “Find a passage” toolbar sheet; simulator displays prominent separate bottom search field under the tab area. \`EncounterSearch.find\` tokenises case/diacritics and reorders tokens, but requires substrings; misspellings/compounds such as \`Guyman\` vs \`Guy man\` or \`taut\` vs \`taught\` are not genuine fuzzy matches.

**Human harm:** User must decide which of two “searches” retrieves what, while still remembering precise enough spellings. This contradicts actual CaptureContext usage: reported **43 human labels, 34 distinct strings, zero assigned destinations**, with natural variants.

**Design correction:** One primary *Find my material* behaviour with direct phrase/passage returns. Use exact matches first; “possible matches” for reversible variants, without changing original labels, merging captures or inventing project routing. Make exact source result and matched word salient. Search entry belongs where it helps browsing (Apple HIG options: inline, top/bottom toolbar, dedicated search entry)—not simultaneous competing affordances.

### HM-07 — P1 / INTENT: Capture privileges link-processing taxonomy

**Observed:** Real Capture UI has large “Bring something into Transcribe” editorial headline, first panel labelled “A link to something you found”, a primary Transcribe button, a long secondary “Save source, download media or extract audio” link, and “Other ways to capture” below fold. Extra link-options sheet has four technical verbs and a caveat about direct media versus social links.

**Human harm:** User must know which option corresponds to *saving something they found*, *getting words*, *retaining the actual video*, *keeping audio*, or *not losing a thought*. A “download media” link may create expectations that provider-resolved public TikTok/Instagram posts are supported where only direct media bytes work. A headline occupying half the top screen delays the person's immediately relevant action.

**Design correction:** Main Capture should afford **Paste a link**, **Record**, **Choose media**, **Write a note** without extra taxonomy. After a link is recognised, present the *supported* next intention clearly: **Get transcript**; secondary **Save link only**; **Keep media** only when actual supported capability is proven. If unsupported, explain precisely; preserve source first. Avoid automatic clipboard reading; do not force project selection.

### HM-08 — P1 / RETURN: existing positions are real but not unified

**Source:** \`EncounterReaderView\` stores \`passageByItem\` with ScrollViewReader and lastOpenedID; \`MediaReturnStore\` stores sourceKey→seconds, updated via time observer / scene phase. At least two independent route families enter the reader. A last-opened item is not necessarily the last actively read passage, and text passage ≠ video timeline.

**Human harm:** Interruption and reentry may look arbitrary; same source can open at different levels depending on how approached. Human anticipates “return to that thought” while app chooses a technical saved token.

**Design correction:** A clearly labelled **Continue** only where exact actual retained position exists, distinct for text / audio / video. Source-level return never erases modality-specific place. Test background, force quit, offline, search→reader→original→back, and VoiceOver focus return. Keep current proven stores and don't make a new global bookmark engine without real need.

### HM-09 — P2 / VISUAL: promising editorial identity, but insufficient hierarchy

**Screens:** warm \`#F9F7F4\` off-white, ink serif, generous whitespace, soft low-chroma cards and compact black tool icons. “Library” is attractive but filters, “CONTINUE”, “Your material”, top tools and bottom bar split focus. The first material row remains predominantly typographic or status-led when actual media isn't available.

**Potential upside:** clear source-led editorial tone rather than generic dashboard. **Not an invitation** to impose the same atmosphere on Quiet Reader, Ofa Jack or DAWT websites.

**Pressure:** choose one hierarchy per human activity:
- Browsing: real content → human label → true source status.
- Reading: words own viewport → optional source/reply controls.
- Listening: actual voice/source identity → transport.
- Watching: real picture owns frame → short contextual actions.
- Failure: what was preserved → what failed → useful next step.

Only surface the controls the current moment earns.

### HM-10 — P2 / TYPOGRAPHY: insufficient small-text/accessibility proof

**Source token contrast calculations (static candidate colours, NOT full UI accessibility audit):**
- \`#888888\` small timestamp text on \`#F9F7F4\` background ≈ **3.32:1**.
- \`#666666\` on same ≈ **5.37:1**.
- \`#E8B44C\` on \`#F9F7F4\` ≈ **1.77:1** (accent used for buttons, not assumed to be foreground text).
WCAG 2.2's 4.5:1 normal-text reference is a useful **cross-platform review yardstick**, not a declaration that an entire native app is WCAG certified or noncompliant from a token. **Actual rendered colours may differ**, and large type/icon-specific tests vary.

**Source:** \`DAWTDesign.Typography\` defines 11–20pt fixed-size helper fonts; some views use dynamic \`.title3\` and native \`.caption\`. Mix demands real Dynamic Type/high contrast/VoiceOver testing. Source forces \`.preferredColorScheme(.light)\` on HomeView; dark appearance cannot simply be assumed available. Buttons like “Respond / Connect / Make / More” on a compact media toolbar cost width and attention.

**Design correction:** test iPhone with large text, bold text, reduced motion, VoiceOver, high contrast, actual thumb reach and caption placement. Verify tap/label sizes, not just glyph size. Make project/label text wrap rather than truncate away the distinguishing words.

### HM-11 — P2 / AUTHORSHIP: “For” and derived groups can overstate intended destination

**Source:** \`CaptureWorkspaceView\` has “Add label or destination”, fields “Label (optional)” and “For (optional)” with a small note saying nothing is sent. Details have a separate person/project/workspace field; the 43-label report says zero assigned destination fields.

**Human harm:** “For” can reasonably be interpreted as sending when it currently means a private reminder. Project-like labels do not prove project identity, destination or explicit delivery. Forcing a taxonomy would make genuine capture harder.

**Design correction:** exact original label and natural language remain first-class. “Possible related work” must be secondary and explicitly non-actionable. A genuine “Send for review” action requires separately governed recipient identity, scope and verified receipt—not a metadata suggestion.

### HM-12 — P2 / MODE: Feed is intentionally empty yet visible as an aspirational tab

**Source:** HomeView offers a sparkles “Feed” tab with “A space for later.” The latest human priority explicitly holds Feed while Library/Capture are repaired.

**Human harm:** The unimplemented destination may divert attention or promise a capability that doesn't exist. It can be acceptable as a roadmap marker but not as a primary source of inspiration or finished surface.

**Design correction:** Keep Feed technically held, preserve existing experimental code without false content. Make the visible held state honest and unobtrusive; its later expression must not compete with Library or require scroll-time optimisation.

### HM-13 — P2 / SOCIAL RELATION: Respond, Connect and Make may crowd the actual source

**Source:** \`EncounterActionBar\` puts Respond and Connect, plus Transcribe or Make and More, under an opened source. The Compose/Connect action opens a note/form; Make opens a retained MotionEncounter fixture (not a general AI generator).

**Human harm:** It can appear as though the machine expects the person to transform, classify or respond to every encounter—even when the person only wanted to read/listen/leave. This is subtle pressure, not a proven user reaction.

**Design correction:** Primary human actions **Inspect / Return / Leave** remain frictionless. “Respond”, “Compare”, “Make” are invitational secondary acts, after source contact; *No response* is a normal positive outcome. Don't mistake UI action count for usefulness.

### HM-14 — P2 / CUSTODY SEMANTICS: library projection may suppress distinct attempts

**Source:** \`EncounterLibrary.preferredTranscripts\` chooses a preferred complete transcript for matching URL and hides other attempt rows in its top-level projection. Underlying records are reported preserved by the build. \`EncounterLibrary\` separately correlates retained captures and transcriptions using exact IDs/source filenames and linked URLs.

**Human harm:** A “one source, one row” presentation is useful, but could make a failed retry, distinct attempt or wrong equivalence hard to inspect. URL identity isn't always original-media byte identity or consented equality. **This is a presentation/correlation pressure, not proof of lost records.**

**Design correction:** One recognisable source entry where identity is established, with **Attempts / Versions / Original** inspectable in source detail. Keep raw failed attempts and diagnostic source references; no silent merge on vague titles or common labels. Never make a new transcript overwrite previous identity.

### HM-15 — P2 / UNCERTAINTY: apparent successful states are more confident than evidence

**Source:** Build 7 has tests and installation proof; owner audit still reports failed-link/file success and unproven source resolution. \`EncounterPlayback\` Now Playing calls every source “Transcribe”; status/reader paths can present “Transcript saved” without surfacing fidelity or media availability nuance.

**Human harm:** When an attractive UI implies *everything worked*, the person can mistake a preserved URL or imperfect transcript for a complete captured video and verified words.

**Design correction:** Distinguish **original accessible** / **bytes retained** / **transcribed** / **checked** / **human-corrected**. A completed transcript is not guaranteed exact speech. Build state, source truth, reading availability and quality standing remain separate.

## 6. Interaction re-contract — how the final product should work, without premature new features

### A. Library — one place to recognise a captured encounter

The first screen should prioritise **Find your material**, then truthful **Continue where you were** only if recoverable, then actual source encounters. A row's **primary element is genuine material**:
- real poster/frame when retained;
- saved words/excerpt when generated from the source transcript;
- real voice/recording type when audio available;
- original user-written note when that is the source;
- honest link/status when only a URL is saved.

The exact user label is an authored cue, not a technical category. Date and platform below. No giant UUID, repeated long server failures or speculative autogenerated quote.

**No obligation to use cards.** Photographs may use image-led tiles; listening items may have a clear sound/transport affordance; longer text may look like a reading excerpt. Preserve consistent source identity without forcing visual sameness.

### B. Single capture encounter — capability selection, not competing routes

\`\`\`text
CAPTURED MATERIAL
True human label, original source, original/capture dates where known

[AUTHENTIC VISUAL OR AUDIO / ORIGINAL WORDS]
[Read transcript]  [Watch]  [Listen to original]
Only available controls shown, all source-specific.

Under secondary “More / Source details”:
Open original · Original media custody · Retry · Extract audio
Version / attempt history · Organise · Share · Add note

Always:
Return to Library / previous saved place
\`\`\`

**Important caveat:** this is an **experience hierarchy proposal**, not a one-component engineering prescription. Different specialist full-screen players/readers may remain as long as source return and provenance are explicit.

### C. Capture — start with intention and preserve before consequence

The primary question is **“What are you bringing in?”** not “which processing pipeline?”.

\`\`\`text
CAPTURE
[Paste / use a link] → Get transcript [when supported]
                     → Save link only [secondary deliberate choice]
[Record something]
[Choose media]
[Write a note]

After successful intake:
“Source saved” · “Transcription requested” (if true)
Open in Library · optional original human label

If unrecognised:
“Saved link. This source can't be transcribed here yet.”
Open original · Choose a file · See why
\`\`\`

No clipboard monitoring, no forced folder form, no fake access to whole Photos library.

### D. Reader / listening / viewing — media determines form

**Reader:** original recognised words, adequate column/line spacing, source return, quiet contextual selection/share, exact passage. **Original video:** prominent picture, real audio, clear full-screen and back; **Original audio:** named clip, one playhead, visible transport, no invented TTS. **Link only:** actual link and clear “not downloaded” status. **Source error:** preserved anchor, one useful recovery, technical details only on request.

A source can have several legitimate representations, but does not become several unconnected histories.

### E. Consequence language: minimal machine truth

| Machine reality | Preferred person-facing wording | False claim to avoid |
|---|---|---|
| URL stored, no media resolved | **Link saved · Original media not kept** | “Video saved” |
| Durable request accepted, completion unknown | **Transcription requested · Checking progress** | “Transcript ready” |
| Authenticated request refused | **Source saved · Couldn't start transcription** + why | “Failed to capture everything” |
| True saved transcript | **Transcript available** | “Exact original speech verified” |
| Successful media extraction | **Original audio extracted and kept** | “Generated reading ready” |
| Only Photos reference | **From Photos · Access may be required** | “Stored a private copy” |
| Recorded label mentions a project | **Your label: ‘…’** | “Delivered to [project]” |
| Original version safe, new attempt pending | **Previous transcript kept · Reprocessing** | “Replacing transcript” |
| Unknown send/save state | **Couldn't confirm · Original/draft kept** | “Success” |

Do not make language bland: precise limitations create trust. Plain text can carry enormous confidence when it is accurate.

## 7. Premium visual practice — not ‘generic AI design’

**DAWT premium quality = perceptual precision, restrained craft, recoverability and emotional tact.** The current warm editorial screen direction is a candidate, but should be *recomposed around human tasks*.

- **Arrival:** clear hierarchy, exact value; not an overlong manifesto heading before input.
- **Media encounter:** typography/colour/motion recede to let original people, image and sound dominate. In a documentary, no ornamental frame hides a face; in a text source, stable type and margins outrank cards.
- **Transitions:** orient place and show consequence; motion must not pretend a download, transcript or playback is done.
- **Voice:** original human speech preserves source, accent, hesitations, mistakes and uncertainty; synthetic narration clearly separate, later and conditional.
- **Colour:** one warm palette across native controls, contextual hierarchy. Do not assume gold accents fix grey-status hierarchy. Contrast and state must be communicated without colour-only dependence.
- **Density:** let source determine whether full-bleed media, layered editorial text or quiet audio transport is appropriate. No permanent control wall.
- **Accessibility:** actual voice and typed alternatives; screen reader order; large type, reduced-motion, low-storage/offline and permission-denial alternatives; large labels shouldn't be clipped or disappear behind bars.

**Reject** cosmetic “premium” mockups if they fail to convey source availability, lose the search/reading return, hide failure, obscure original speech or create false readiness.

## 8. One-fixture real-world test — discriminate the design

**Start from a fresh reversible snapshot of the existing installed Build 7 and a consented, known test source. No personally sensitive sources need publishing.**

1. **Source-truth fixture:** same video submitted as external link (reported failure) and downloaded import (reported success), with owner-approved local input access. Inspect exact provider acquisition/job/media/audio-tracks and identities. User sees useful honest status and a way to recover.
2. **Version preservation fixture:** existing transcript + extracted audio retried, with before/after hashes and separate stable versions, failure/interrupt/duplicate retry. This is P0 and **must precede any user re-transcribe demonstration on irreplaceable records**.
3. **One encounter/multiple forms:** one actual authorised retained video with its audio and transcript. Enter from Library and phrase search. Confirm Watch / Listen original / Read / Open original on same source context and return exactly to prior place.
4. **Playback exclusivity:** start video; start source audio; switch back; lock device; receive phone interruption. Never two audible sources and no anonymous Listening bar. Observe actual media positions after reopening.
5. **Natural label retrieval:** find multiple **distinct** sources labelled with variations (Guyman/Guy man; Shadow taught/taut) without any hidden relabelling, merging or project assignment. Verify approximate match explicit if offered.
6. **Unavailability:** URL-only, failed processing, denied Photos, selected Photos reference, image-only and audio-only. No fake media, phantom source, lost record or misleading default player.
7. **Human contribution / refusal:** capture without label; add a full-sentence label; view source and leave without note/task; explicitly organise; attempt deliberate “For” without claiming delivery.
8. **Physical comfort:** iPhone 13, keyboard during share, one-handed reach, Dynamic Type up to maximum, VoiceOver, reduced motion, offline/cellular, interrupted playback, longer than ten-minute transcript.
9. **Finish:** user can say *I found what I was looking for* and leave. A source that isn't useful to revisit is not a failure of their attention.

### Discriminating observation prompts (not a ritual forced onto user)

- After opening, **what did the person notice first**? A book/source, or administration and buttons?
- Could they **recognise their saved item** without remembering exact spelling or platform URL?
- Could they accurately tell **what Transcribe did versus what remained unprocessed**?
- Were they surprised by new work happening or a previous result changing?
- Could they leave, resume and retrieve the original position?
- Were failure and limitation comprehensible without understanding HTTP, audio tracks or UUIDs?
- Did media play/stop and source identity remain obvious without investigating menus?
- Was a button present that had no human reason to be there?
- Did aesthetics support original content rather than compete with it?
- Were **unknown** and **not ready** shown where evidence was actually unknown?

### Pass/hold criteria

**PASS only when:** original source and prior transcriptions are safe; one-source identity is clear across entry points; one active audio experience; source/read/listen availability true; understandable recovery; no forced classification; exact return verified on-device; accessibility regressions tested.

**HOLD if:** transcript version can still be replaced; audio identity ambiguous; original inaccessible despite optimistic success; fallback falsely implies video retained; “For” looks like delivery; source return mismatches; phone makes the person re-transcribe an already completed capture.

## 9. Repair and design sequence — minimum real work, no premature overhaul

**P0 / Guard human history (owner + authorised engineering):** version preservation/attempt identity, source-equivalence evidence, same failed-URL vs imported-media diagnosis. Readonly field reproduction, then separately approved regression fix. Protect protected backups. This is a build gate; not a visual-design task.

**P1 / Contract and first visual encounter (Transcribe + DAWT Design):** one actual retained source storyboard across Library / source / reader / video / audio / search. Evaluate label, meaning, status, transport. Use *real safe fixture media*, not “AI design cards”. **Choose whether a single source overview or consistent back-to-source anchor better serves the person**; don't pre-commit to a giant modal.

**P2 / Condense operations and error presentation:** context-conditional actions, Capture intent anatomy, one search behavior, concise row status with deep technical details; preserve all tested engine paths and share-sheet editing.

**P3 / Native visual craft and field verification:** typography, density, contrast, optical alignment, transitions, Discoverability, Dynamic Type, VoiceOver and interruption. Verify on actual device in real use and compare against unchanged Build 7 baseline.

**Later / Feed and generated media:** intentionally held. Not a prerequisite for excellent Library/Capture. Quiet Reader and DAWT Design are possible research donors, not enabled integrations.

## 10. Independent external principles (reference, not proof of this app)

- Apple's [Human Interface Guidelines — Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars): top-level sections and navigation state, not action buttons.
- Apple's [Human Interface Guidelines — Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields): choose entry contextually rather than duplicate every search placement.
- Nielsen Norman Group's [Ten usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/): feedback/status, real-world language, control/exit, consistency, error prevention, recognition, recovery, unnecessary information.
- Nielsen Norman Group's [Recognition and recall](https://www.nngroup.com/articles/recognition-and-recall/): the interface should present enough cues to recognise, not rely on reconstructing exact remembered words.
- [W3C WCAG 2.2](https://www.w3.org/TR/wcag/): contrast and reflow/target-size benchmarks; mobile native equivalents require platform-specific tests.

External heuristics do not substitute for real human encounters and native app testing. They are pressure lenses, not proof of product failure.

## 11. Source and permission/standing conclusion

**DAWT DESIGN contribution today:** documented independent visual and source-code audit; prioritised human consequences; distinguished established source behaviour vs hypothesised failure; defined one-capture/one-audible-focus/actual-source representation design principles and exact field acceptance. No visual image-generation commissioned, no screen implementation, no new model or AI Feed proposed for execution.

**What I cannot certify today:** exact physical iPhone 13 state at 11:41, all provider retries, actual simultaneous playback reproduction, absence of lost old transcripts, voice output accuracy, full accessibility compliance, human acceptance or any agreed implementation admission.

**Responsible recipients:** Transcribe owner decides the product/fixture; Ofa Jack/Claude under independent gated spec implements repairs; DAWT Design develops and judges coherent visual interaction; Belawu retains crossing/governance; Abdul accepts artistic/human quality.

### Disposition

**SOURCE-AUDITED / HUMAN-MACHINE RELATION NOT YET COHERENT / PREMIUM VISUAL DIRECTION NOT YET EARNED / P0 SOURCE-VERSION SAFETY FIRST / HUMAN FIELD JUDGEMENT OUTSTANDING.**

**Keeper:** **The machine must remember its own machinery so the human doesn't have to. The original encounter belongs to the person; every transformation must remain recognisable, reversible and truthful.**
