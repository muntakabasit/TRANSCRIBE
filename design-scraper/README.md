# 🎨 Design Scraper - Maximum Extraction Tool

**Extract EVERYTHING from any website's design**

A comprehensive UI/UX design scraping tool that extracts colors, typography, SVGs, images, CSS, layouts, and design flows from any website. Built with Virgil Abloh/Off-White aesthetic.

---

## ✨ Features

### Maximum Extraction
- 📸 **Screenshots** - Full page, viewport, mobile views
- 🎨 **Color Palette** - All colors with hex codes & usage frequency
- 🔤 **Typography** - Font families, sizes, weights, line-heights
- 📐 **SVG Elements** - All icons, logos, illustrations
- 🖼️ **Images** - Download all PNG, JPG, WebP files
- 💅 **CSS Styles** - All stylesheets, inline styles, computed styles
- 🗺️ **Design Flow** - Navigation, sitemap, page hierarchy
- 📏 **Layout Info** - Grid systems, spacing, Flexbox/Grid usage
- 🎬 **Animations** - CSS animations & transitions

### Organized Output
```
design_{job_id}/
├── screenshot_full.png
├── screenshot_viewport.png
├── screenshot_mobile.png
├── design_report.json
├── page.html
└── assets/
    ├── images/
    ├── svgs/
    ├── css/
    └── fonts/
```

---

## 🚀 How to Use

### 1. Start the Server
```bash
cd design-scraper
uvicorn app:app --host 0.0.0.0 --port 6000
```

### 2. Open the UI
Visit: `http://localhost:6000`

### 3. Scrape a Website
1. Enter a website URL (e.g., `https://www.apple.com`)
2. Click **"EXTRACT DESIGN →"**
3. Wait for extraction (usually 10-30 seconds)
4. View results & download assets

---

## 📊 API Endpoints

### POST `/scrape`
Start a new scraping job
```json
{
  "url": "https://www.example.com"
}
```

**Response:**
```json
{
  "job_id": "a1b2c3d4",
  "status": "queued"
}
```

### GET `/status/{job_id}`
Check job status
```json
{
  "job_id": "a1b2c3d4",
  "url": "https://www.example.com",
  "status": "processing",
  "progress": "Extracting design elements..."
}
```

### GET `/result/{job_id}`
Get full extraction results
```json
{
  "url": "https://www.example.com",
  "colors": [...],
  "typography": {...},
  "svgs": [...],
  "images": [...],
  "screenshots": {...}
}
```

### GET `/download/{job_id}`
Download all assets as ZIP file

### GET `/health`
Health check endpoint

---

## 🎨 What Gets Extracted

### Colors
- All colors from CSS, computed styles, SVGs
- Sorted by usage frequency
- Hex + RGB formats
- Top 50 most-used colors

### Typography
- Font families used
- All font sizes (px, rem, em)
- Font weights (400, 700, 900, etc.)
- Line heights
- Letter spacing

### SVGs
- All `<svg>` elements
- Individual SVG files saved
- ViewBox, width, height preserved

### Images
- All `<img>` elements
- Downloaded locally
- Alt text preserved
- Size information

### CSS
- All stylesheets extracted
- Inline styles captured
- Computed styles analyzed

### Layout
- Grid/Flexbox detection
- Container widths
- Padding/margin systems
- Max-width constraints

### Design Flow
- Navigation structure
- Internal vs external links
- Header/footer detection
- Page hierarchy

### Animations
- CSS animations detected
- Transition properties
- Element-level animation tracking

---

## 🎯 Use Cases

### For Designers
- **Inspiration Mining** - Extract color palettes from favorite sites
- **Competitive Analysis** - Study competitor designs
- **Design Systems** - Reverse-engineer typography scales
- **Mood Boards** - Collect visual elements quickly

### For Developers
- **CSS Reference** - Study how top sites implement features
- **Component Libraries** - Extract reusable patterns
- **Performance Analysis** - See what assets are loaded
- **Accessibility** - Analyze color contrast, font sizes

### For Agencies
- **Client Presentations** - Show design inspirations
- **Competitive Audits** - Compare multiple sites
- **Style Guides** - Build brand guidelines from references
- **Prototyping** - Quick asset extraction for mockups

---

## 🏗️ Technical Stack

- **Backend:** FastAPI (Python 3.11+)
- **Browser Automation:** Playwright with Chromium
- **HTML Parsing:** BeautifulSoup4
- **Image Processing:** Pillow
- **Color Extraction:** ColorThief
- **CSS Parsing:** cssutils

---

## 📝 Example Output

### Color Palette
```json
[
  {"hex": "#000000", "rgb": "rgb(0, 0, 0)", "usage_count": 156},
  {"hex": "#FFFFFF", "rgb": "rgb(255, 255, 255)", "usage_count": 142},
  {"hex": "#1D1D1F", "rgb": "rgb(29, 29, 31)", "usage_count": 89}
]
```

### Typography
```json
{
  "SF Pro Display, -apple-system, BlinkMacSystemFont": {
    "sizes": ["16px", "20px", "32px", "48px"],
    "weights": ["400", "600", "700", "900"],
    "lineHeights": ["1.2", "1.4", "1.5"],
    "letterSpacings": ["-0.02em", "normal"]
  }
}
```

---

## ⚡ Performance

- **Average extraction time:** 10-30 seconds
- **Max concurrent jobs:** Unlimited (async processing)
- **Image limit:** 50 images per site
- **SVG limit:** Unlimited
- **Color limit:** Top 50 colors

---

## 🎨 Design Philosophy

Built with **Virgil Abloh/Off-White** aesthetic:
- Bold typography (Helvetica Neue)
- Quotation marks around headings
- Industrial label styling
- Minimal black-on-white color scheme
- 4px black top stripe
- Square spinners (no curves)
- Uppercase labels with tight letter-spacing

---

## 🔮 Future Enhancements

- [ ] **Figma Plugin** - Export directly to Figma
- [ ] **AI Design Analysis** - Detect design patterns
- [ ] **Component Recognition** - Identify buttons, cards, etc.
- [ ] **Accessibility Scoring** - WCAG compliance checks
- [ ] **Design Diff** - Compare versions over time
- [ ] **Batch Processing** - Scrape multiple URLs at once
- [ ] **Video Capture** - Record interactions, animations
- [ ] **Code Generation** - Generate React/Vue components

---

## 📄 License

MIT License - Built for the creator economy

---

## 🎯 Perfect For

- TikTok/Instagram creators building landing pages
- Designers studying top brands
- Agencies conducting competitive research
- Developers learning modern CSS patterns
- Anyone who loves beautiful design

**Extract everything. Own the aesthetic.** ✨
