"""
Design Scraper Engine - MAXIMUM EXTRACTION (Fixed)
Extracts EVERYTHING from a website: colors, fonts, SVGs, images, CSS, layout, flow
Now with network interception for cross-origin resources and ColorThief analysis
"""

import asyncio
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from urllib.parse import urljoin, urlparse
import hashlib

from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup
from PIL import Image
from colorthief import ColorThief
import io
import tempfile

class DesignScraper:
    def __init__(self, url: str, output_dir: str = "downloads"):
        self.url = url
        self.output_dir = Path(output_dir)
        self.domain = urlparse(url).netloc
        self.job_id = hashlib.md5(url.encode()).hexdigest()[:8]
        self.job_dir = self.output_dir / f"design_{self.job_id}"
        
        # Create organized structure
        self.assets_dir = self.job_dir / "assets"
        self.images_dir = self.assets_dir / "images"
        self.svgs_dir = self.assets_dir / "svgs"
        self.fonts_dir = self.assets_dir / "fonts"
        self.css_dir = self.assets_dir / "css"
        
        for d in [self.job_dir, self.assets_dir, self.images_dir, 
                  self.svgs_dir, self.fonts_dir, self.css_dir]:
            d.mkdir(parents=True, exist_ok=True)
        
        # Track captured resources via network interception
        self.captured_resources = {
            'css': [],
            'fonts': [],
            'images': [],
            'js': []
        }
    
    async def scrape_everything(self) -> Dict[str, Any]:
        """Main scraping orchestrator - extracts EVERYTHING"""
        print(f"🎨 Starting MAXIMUM extraction for: {self.url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = await context.new_page()
            
            # Network interception - capture ALL resources
            async def handle_response(response):
                try:
                    content_type = response.headers.get('content-type', '').lower()
                    url = response.url
                    
                    # Capture CSS
                    if 'text/css' in content_type or url.endswith('.css'):
                        try:
                            content = await response.body()
                            self.captured_resources['css'].append({
                                'url': url,
                                'content': content.decode('utf-8', errors='ignore')
                            })
                        except:
                            pass
                    
                    # Capture Fonts
                    elif 'font' in content_type or any(url.endswith(ext) for ext in ['.woff', '.woff2', '.ttf', '.otf', '.eot']):
                        try:
                            content = await response.body()
                            self.captured_resources['fonts'].append({
                                'url': url,
                                'content': content
                            })
                        except:
                            pass
                    
                    # Capture Images
                    elif 'image' in content_type or any(url.endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']):
                        try:
                            content = await response.body()
                            self.captured_resources['images'].append({
                                'url': url,
                                'content': content,
                                'type': content_type
                            })
                        except:
                            pass
                    
                except Exception as e:
                    print(f"⚠️  Failed to capture resource: {e}")
            
            page.on('response', handle_response)
            
            try:
                print("🌐 Loading page and capturing resources...")
                await page.goto(self.url, wait_until='networkidle', timeout=45000)
                await asyncio.sleep(3)  # Let lazy-load/animations finish
                
                print("⚙️  Extracting all design elements...")
                # Extract everything in parallel
                results = await asyncio.gather(
                    self.extract_screenshots(page),
                    self.extract_html_structure(page),
                    self.extract_colors_comprehensive(page),
                    self.extract_typography(page),
                    self.extract_css_and_fonts(),
                    self.extract_svgs(page),
                    self.extract_images_comprehensive(),
                    self.extract_design_flow(page),
                    self.extract_layout_info(page),
                    self.extract_animations(page),
                    return_exceptions=True
                )
                
                # Compile results
                design_data = {
                    "url": self.url,
                    "domain": self.domain,
                    "job_id": self.job_id,
                    "screenshots": results[0] if not isinstance(results[0], Exception) else {},
                    "html_structure": results[1] if not isinstance(results[1], Exception) else {},
                    "colors": results[2] if not isinstance(results[2], Exception) else [],
                    "typography": results[3] if not isinstance(results[3], Exception) else {},
                    "css_styles": results[4] if not isinstance(results[4], Exception) else {},
                    "svgs": results[5] if not isinstance(results[5], Exception) else [],
                    "images": results[6] if not isinstance(results[6], Exception) else [],
                    "design_flow": results[7] if not isinstance(results[7], Exception) else {},
                    "layout": results[8] if not isinstance(results[8], Exception) else {},
                    "animations": results[9] if not isinstance(results[9], Exception) else [],
                }
                
                # Save comprehensive JSON report
                report_path = self.job_dir / "design_report.json"
                with open(report_path, 'w') as f:
                    json.dump(design_data, f, indent=2)
                
                print(f"✅ MAXIMUM extraction complete! Saved to: {self.job_dir}")
                return design_data
                
            finally:
                await browser.close()
    
    async def extract_screenshots(self, page: Page) -> Dict:
        """Capture full page, viewport, and mobile screenshots"""
        print("📸 Capturing screenshots...")
        
        screenshots = {}
        
        # Full page screenshot
        full_path = self.job_dir / "screenshot_full.png"
        await page.screenshot(path=str(full_path), full_page=True)
        screenshots['full_page'] = str(full_path.relative_to(self.output_dir))
        
        # Viewport screenshot
        viewport_path = self.job_dir / "screenshot_viewport.png"
        await page.screenshot(path=str(viewport_path), full_page=False)
        screenshots['viewport'] = str(viewport_path.relative_to(self.output_dir))
        
        # Mobile screenshot
        mobile_path = self.job_dir / "screenshot_mobile.png"
        await page.set_viewport_size({'width': 375, 'height': 667})
        await page.screenshot(path=str(mobile_path), full_page=True)
        await page.set_viewport_size({'width': 1920, 'height': 1080})
        screenshots['mobile'] = str(mobile_path.relative_to(self.output_dir))
        
        return screenshots
    
    async def extract_html_structure(self, page: Page) -> Dict:
        """Extract HTML structure and page hierarchy"""
        print("🏗️  Analyzing HTML structure...")
        
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        # Save raw HTML
        html_path = self.job_dir / "page.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Safe extraction with None checks
        title_tag = soup.find('title')
        title = title_tag.string if title_tag and title_tag.string else ""
        
        meta_desc_tag = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_desc_tag.get('content', '') if meta_desc_tag else ""
        
        structure = {
            "title": title,
            "meta_description": meta_description,
            "headings": {
                f"h{i}": [h.get_text(strip=True) for h in soup.find_all(f'h{i}')] 
                for i in range(1, 7)
            },
            "sections": len(soup.find_all(['section', 'article', 'div'])),
            "links": len(soup.find_all('a')),
            "forms": len(soup.find_all('form')),
            "buttons": len(soup.find_all('button')),
        }
        
        return structure
    
    async def extract_colors_comprehensive(self, page: Page) -> List[Dict]:
        """Extract ALL colors from CSS, computed styles, AND images using ColorThief"""
        print("🎨 Extracting comprehensive color palette...")
        
        color_counts = {}
        
        # 1. Get colors from computed styles
        color_data = await page.evaluate("""
            () => {
                const colors = new Set();
                const elements = document.querySelectorAll('*');
                
                elements.forEach(el => {
                    const styles = window.getComputedStyle(el);
                    const props = ['color', 'backgroundColor', 'borderColor', 'borderTopColor', 
                                   'borderRightColor', 'borderBottomColor', 'borderLeftColor', 
                                   'fill', 'stroke', 'outlineColor'];
                    
                    props.forEach(prop => {
                        const value = styles[prop];
                        if (value && value !== 'none' && value !== 'transparent' && 
                            !value.includes('rgba(0, 0, 0, 0)') && !value.includes('rgba(0,0,0,0)')) {
                            colors.add(value);
                        }
                    });
                });
                
                return Array.from(colors);
            }
        """)
        
        # Parse CSS colors
        for color in color_data:
            try:
                hex_color = self._normalize_color(color)
                if hex_color:
                    color_counts[hex_color] = color_counts.get(hex_color, 0) + 1
            except:
                continue
        
        # 2. Extract colors from images using ColorThief
        print("🖼️  Analyzing image colors with ColorThief...")
        for i, img_resource in enumerate(self.captured_resources['images'][:10]):  # Analyze first 10 images
            try:
                if 'svg' not in img_resource.get('type', ''):
                    # Create temp file for ColorThief
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
                        tmp.write(img_resource['content'])
                        tmp_path = tmp.name
                    
                    try:
                        color_thief = ColorThief(tmp_path)
                        palette = color_thief.get_palette(color_count=5, quality=1)
                        
                        for rgb in palette:
                            hex_color = '#%02x%02x%02x' % rgb
                            color_counts[hex_color] = color_counts.get(hex_color, 0) + 10  # Weight image colors higher
                    finally:
                        os.unlink(tmp_path)
            except:
                continue
        
        # Sort by frequency and format
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        
        colors = []
        for hex_color, count in sorted_colors[:100]:  # Top 100 colors
            try:
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
                colors.append({
                    "hex": hex_color,
                    "rgb": f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})",
                    "usage_count": count,
                    "name": self._get_color_name(hex_color)
                })
            except:
                continue
        
        return colors
    
    def _normalize_color(self, color: str) -> Optional[str]:
        """Convert any color format to hex"""
        try:
            if color.startswith('rgb'):
                rgb = re.findall(r'\d+', color)[:3]
                return '#%02x%02x%02x' % tuple(map(int, rgb))
            elif color.startswith('#'):
                return color.lower()
        except:
            pass
        return None
    
    def _get_color_name(self, hex_color: str) -> str:
        """Get approximate color name"""
        try:
            import webcolors
            return webcolors.hex_to_name(hex_color)
        except:
            return "custom"
    
    async def extract_typography(self, page: Page) -> Dict:
        """Extract font families, sizes, weights, and styles"""
        print("🔤 Analyzing typography...")
        
        font_data = await page.evaluate("""
            () => {
                const fonts = {};
                const elements = document.querySelectorAll('*');
                
                elements.forEach(el => {
                    const styles = window.getComputedStyle(el);
                    const fontFamily = styles.fontFamily;
                    const fontSize = styles.fontSize;
                    const fontWeight = styles.fontWeight;
                    const lineHeight = styles.lineHeight;
                    const letterSpacing = styles.letterSpacing;
                    const textTransform = styles.textTransform;
                    
                    if (fontFamily) {
                        if (!fonts[fontFamily]) {
                            fonts[fontFamily] = {
                                sizes: new Set(),
                                weights: new Set(),
                                lineHeights: new Set(),
                                letterSpacings: new Set(),
                                textTransforms: new Set()
                            };
                        }
                        fonts[fontFamily].sizes.add(fontSize);
                        fonts[fontFamily].weights.add(fontWeight);
                        fonts[fontFamily].lineHeights.add(lineHeight);
                        fonts[fontFamily].letterSpacings.add(letterSpacing);
                        fonts[fontFamily].textTransforms.add(textTransform);
                    }
                });
                
                // Convert Sets to Arrays
                Object.keys(fonts).forEach(font => {
                    fonts[font].sizes = Array.from(fonts[font].sizes);
                    fonts[font].weights = Array.from(fonts[font].weights);
                    fonts[font].lineHeights = Array.from(fonts[font].lineHeights);
                    fonts[font].letterSpacings = Array.from(fonts[font].letterSpacings);
                    fonts[font].textTransforms = Array.from(fonts[font].textTransforms);
                });
                
                return fonts;
            }
        """)
        
        return font_data
    
    async def extract_css_and_fonts(self) -> Dict:
        """Extract ALL CSS and fonts using network-captured resources"""
        print("💅 Saving CSS stylesheets and fonts...")
        
        css_files = []
        
        # Save all network-captured CSS files
        for i, css_resource in enumerate(self.captured_resources['css']):
            filename = Path(urlparse(css_resource['url']).path).name or f"stylesheet_{i}.css"
            css_path = self.css_dir / filename
            
            with open(css_path, 'w', encoding='utf-8') as f:
                f.write(css_resource['content'])
            
            css_files.append({
                "path": str(css_path.relative_to(self.output_dir)),
                "url": css_resource['url'],
                "size": len(css_resource['content'])
            })
        
        # Save all fonts
        font_files = []
        for i, font_resource in enumerate(self.captured_resources['fonts']):
            ext = Path(urlparse(font_resource['url']).path).suffix or '.woff2'
            font_path = self.fonts_dir / f"font_{i}{ext}"
            
            with open(font_path, 'wb') as f:
                f.write(font_resource['content'])
            
            font_files.append({
                "path": str(font_path.relative_to(self.output_dir)),
                "url": font_resource['url'],
                "size": len(font_resource['content'])
            })
        
        return {
            "stylesheets": len(css_files),
            "saved_css_files": css_files,
            "fonts": len(font_files),
            "saved_font_files": font_files
        }
    
    async def extract_svgs(self, page: Page) -> List[Dict]:
        """Extract all SVG elements and save them"""
        print("📐 Extracting SVG elements...")
        
        svgs = await page.evaluate("""
            () => {
                const svgElements = document.querySelectorAll('svg');
                return Array.from(svgElements).map((svg, i) => ({
                    index: i,
                    content: svg.outerHTML,
                    viewBox: svg.getAttribute('viewBox'),
                    width: svg.getAttribute('width'),
                    height: svg.getAttribute('height'),
                    class: svg.getAttribute('class'),
                    id: svg.getAttribute('id')
                }));
            }
        """)
        
        svg_files = []
        for svg_data in svgs:
            svg_path = self.svgs_dir / f"svg_{svg_data['index']}.svg"
            with open(svg_path, 'w') as f:
                f.write(svg_data['content'])
            
            svg_files.append({
                "path": str(svg_path.relative_to(self.output_dir)),
                "viewBox": svg_data.get('viewBox'),
                "dimensions": f"{svg_data.get('width', 'auto')}x{svg_data.get('height', 'auto')}"
            })
        
        return svg_files
    
    async def extract_images_comprehensive(self) -> List[Dict]:
        """Save all network-captured images"""
        print("🖼️  Saving images...")
        
        downloaded_images = []
        for i, img_resource in enumerate(self.captured_resources['images'][:100]):  # Max 100 images
            try:
                # Determine extension
                url = img_resource['url']
                ext = Path(urlparse(url).path).suffix or '.png'
                img_path = self.images_dir / f"image_{i}{ext}"
                
                with open(img_path, 'wb') as f:
                    f.write(img_resource['content'])
                
                downloaded_images.append({
                    "path": str(img_path.relative_to(self.output_dir)),
                    "url": url,
                    "size": len(img_resource['content']),
                    "type": img_resource.get('type', 'unknown')
                })
            except:
                continue
        
        return downloaded_images
    
    async def extract_design_flow(self, page: Page) -> Dict:
        """Analyze navigation, sitemap, and user flows - COMPREHENSIVE"""
        print("🗺️  Mapping complete design flow...")
        
        flow = await page.evaluate("""
            () => {
                const nav = document.querySelector('nav');
                const header = document.querySelector('header');
                const footer = document.querySelector('footer');
                const main = document.querySelector('main');
                
                // Get all links with structure
                const links = Array.from(document.querySelectorAll('a')).map(a => ({
                    text: a.textContent.trim().substring(0, 100),
                    href: a.href,
                    isInternal: a.href.startsWith(window.location.origin),
                    inNav: nav?.contains(a) || false,
                    inFooter: footer?.contains(a) || false
                }));
                
                // Navigation structure
                const navItems = nav ? Array.from(nav.querySelectorAll('a')).map(a => ({
                    text: a.textContent.trim(),
                    href: a.href,
                    hasChildren: a.parentElement?.querySelectorAll('ul, ol').length > 0
                })) : [];
                
                // Page sections
                const sections = Array.from(document.querySelectorAll('section, article')).map(s => ({
                    tag: s.tagName.toLowerCase(),
                    id: s.id,
                    class: s.className,
                    headings: Array.from(s.querySelectorAll('h1, h2, h3, h4, h5, h6')).map(h => h.textContent.trim())
                }));
                
                return {
                    has_nav: !!nav,
                    has_header: !!header,
                    has_footer: !!footer,
                    has_main: !!main,
                    total_links: links.length,
                    internal_links: links.filter(l => l.isInternal).length,
                    external_links: links.filter(l => !l.isInternal).length,
                    nav_links: links.filter(l => l.inNav).length,
                    footer_links: links.filter(l => l.inFooter).length,
                    navigation_structure: navItems.slice(0, 20),
                    page_sections: sections.slice(0, 10),
                    top_internal_links: links.filter(l => l.isInternal).slice(0, 20)
                };
            }
        """)
        
        return flow
    
    async def extract_layout_info(self, page: Page) -> Dict:
        """Extract grid systems, spacing, and layout patterns - COMPREHENSIVE"""
        print("📏 Analyzing layout systems...")
        
        layout = await page.evaluate("""
            () => {
                const body = document.body;
                const bodyStyles = window.getComputedStyle(body);
                
                // Detect CSS Grid/Flexbox usage
                const gridElements = Array.from(document.querySelectorAll('*')).filter(el => {
                    const display = window.getComputedStyle(el).display;
                    return display === 'grid' || display === 'inline-grid';
                });
                
                const flexElements = Array.from(document.querySelectorAll('*')).filter(el => {
                    const display = window.getComputedStyle(el).display;
                    return display === 'flex' || display === 'inline-flex';
                });
                
                // Container patterns
                const containers = Array.from(document.querySelectorAll('[class*="container"], [class*="wrapper"], [class*="content"]'))
                    .map(el => {
                        const styles = window.getComputedStyle(el);
                        return {
                            maxWidth: styles.maxWidth,
                            padding: styles.padding,
                            margin: styles.margin
                        };
                    }).slice(0, 5);
                
                return {
                    body_max_width: bodyStyles.maxWidth,
                    body_padding: bodyStyles.padding,
                    body_margin: bodyStyles.margin,
                    grid_elements: gridElements.length,
                    flex_elements: flexElements.length,
                    container_width: body.offsetWidth,
                    viewport_width: window.innerWidth,
                    viewport_height: window.innerHeight,
                    containers: containers
                };
            }
        """)
        
        return layout
    
    async def extract_animations(self, page: Page) -> List[Dict]:
        """Detect CSS animations and transitions"""
        print("🎬 Detecting animations...")
        
        animations = await page.evaluate("""
            () => {
                const animated = [];
                const elements = document.querySelectorAll('*');
                
                elements.forEach((el, i) => {
                    const styles = window.getComputedStyle(el);
                    const animation = styles.animation;
                    const transition = styles.transition;
                    const transform = styles.transform;
                    
                    if ((animation && animation !== 'none') || 
                        (transition && transition !== 'all 0s ease 0s') ||
                        (transform && transform !== 'none')) {
                        animated.push({
                            element: el.tagName,
                            class: el.className,
                            id: el.id,
                            animation: animation,
                            transition: transition,
                            transform: transform
                        });
                    }
                });
                
                return animated.slice(0, 30);  // Top 30 animated elements
            }
        """)
        
        return animations


# Quick test function
async def quick_test():
    scraper = DesignScraper("https://www.apple.com")
    results = await scraper.scrape_everything()
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    asyncio.run(quick_test())
