# DAWT APP MANIFESTO
## Design As World Therapy

---

## **Purpose**

DAWT apps are sovereign tools built on the principle that **design is therapy**. They process data locally, respect user privacy, and prioritize long-term usability over short-term trends.

Every DAWT app follows these core principles:

---

## **1. Sovereignty**

- **Local-first processing** - No cloud dependencies for core functionality
- **Data ownership** - Users control their data, not platforms
- **No lock-in** - Standard export formats (JSON, CSV, Markdown)
- **Offline resilience** - Apps work without internet connection

**Example:** DAWT-Transcribe uses local Whisper/mT5 models instead of cloud APIs.

---

## **2. Design Language (Virgil Abloh/Off-White Aesthetic)**

Visual consistency creates trust. Every DAWT app follows industrial minimalism:

- **Typography:** Bold Helvetica Neue, uppercase labels, tight letter-spacing
- **Quotation marks:** "TRANSCRIBE" - decorative quotes around key headings
- **Industrial labels:** "AUDIO INPUT" cutout labels on bordered boxes
- **Color scheme:** Minimal black-on-white with 4px black stripe at top
- **Buttons:** Black background with arrow (→) indicators
- **No curves:** Square spinners, sharp edges, geometric precision

**Why?** Visual discipline creates emotional clarity.

---

## **3. Excel DNA Principles**

DAWT apps are built to last decades, not months:

- **Backward compatibility** - Old files work with new versions
- **Version metadata** - Every export includes format version and compatibility info
- **Graceful degradation** - Features fail gracefully, never crash
- **Self-documenting** - Outputs include metadata explaining structure
- **Standard formats** - CSV, JSON, Markdown - readable in 2050

**Example:** Every JSON export includes `meta.version`, `meta.compatible_since`.

---

## **4. Interoperability**

No silos. Every DAWT app speaks to others:

- **Standard exports:** JSON, CSV, XLSX, Markdown, SRT
- **Re-import capability:** Round-trip editing without data loss
- **Timestamped data:** Everything includes creation timestamps
- **Chainable workflows:** Output of one app is input to another

**Example:** Transcribe → AutoCut → Video Editor

---

## **5. Resilience**

Production-ready from day one:

- **Error handling** - Clear error messages, never crash silently
- **Health checks** - `/health` endpoints for monitoring
- **Logging** - Structured logs with request IDs
- **Retry logic** - Automatic retries for transient failures
- **Resource limits** - Video length limits, rate limiting

---

## **6. Privacy & Security**

User trust is non-negotiable:

- **No tracking** - No analytics, no telemetry
- **No external calls** - Models run locally
- **HTTPS only** - Encrypted connections
- **No data retention** - Users control deletion
- **Transparent permissions** - Mobile apps request only necessary permissions

---

## **7. Documentation**

Every DAWT app includes:

- **README.md** - What it does, how to use it
- **DAWT_MANIFESTO.md** - Why it exists (this file)
- **Inline comments** - Code explains itself
- **API docs** - FastAPI auto-generated docs
- **Version history** - Changelog tracking major changes

---

## **Philosophy in Practice**

### **What DAWT Apps Are:**
- Tools that respect your time
- Software that outlives trends
- Design that creates calm
- Technology that serves creativity

### **What DAWT Apps Are NOT:**
- Surveillance platforms
- Subscription traps
- Black boxes
- Disposable MVPs

---

## **The DAWT Test**

Ask these questions about any app:

1. **Can it run offline?** (Sovereignty)
2. **Does it follow the visual language?** (Design consistency)
3. **Will files work in 10 years?** (Excel DNA)
4. **Can it export standard formats?** (Interoperability)
5. **Does it handle errors gracefully?** (Resilience)
6. **Does it respect privacy?** (Security)
7. **Is the philosophy documented?** (Transparency)

If all 7 answers are yes, it's a proper DAWT app.

---

## **Active DAWT Apps**

1. **DAWT-Transcribe** (Port 5000)
   - Sovereign audio transcription
   - 11 African/European languages
   - Local Whisper + mT5 models
   - Export: JSON, Markdown, CSV, XLSX

2. **Design Scraper** (Port 6000)
   - Maximum UI/UX extraction
   - ColorThief image analysis
   - Network interception for cross-origin assets
   - Export: ZIP, JSON

3. **DAWT Mobile** (Port 8000)
   - React Native (Expo)
   - Audio recording, file upload, URL transcription
   - Same Virgil Abloh aesthetic
   - iOS/Android support

---

## **Technical Stack**

### **Backend**
- **Python:** FastAPI, Whisper, mT5, PostgreSQL
- **Node.js:** React Native, Expo

### **Design**
- **Fonts:** Helvetica Neue, Inter, Futura
- **Colors:** #000000, #FFFFFF, #666666
- **Layout:** 4px grid system, industrial borders

### **Infrastructure**
- **Deployment:** Replit Autoscale
- **Database:** PostgreSQL (Neon)
- **Mobile:** Expo Go (iOS/Android)

---

## **Future Vision**

DAWT is not a company or product—it's a **design philosophy**.

As more tools adopt these principles, they form a **sovereign creative operating system**:
- Local-first
- Privacy-respecting
- Design-consistent
- Interoperable
- Built to last

**The goal:** Software that serves creativity without extracting value from creators.

---

**Version:** 1.0  
**Created:** November 7, 2025  
**Author:** Abdul Basit Muntaka  
**License:** Philosophy is free. Implementation respects your sovereignty.
