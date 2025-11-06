"""
Design Scraper Engine - Maximum Extraction
Extracts EVERYTHING from a website: colors, fonts, SVGs, images, CSS, layout, flow
"""

import asyncio
import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any
from urllib.parse import urljoin, urlparse
import hashlib

from playwright.async_api import async_playwright, Page
from bs4 import BeautifulSoup
from PIL import Image
from colorthief import ColorThief
import cssutils
import webcolors
import io
import base64

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
    
    async def scrape_everything(self) -> Dict[str, Any]:
        """Main scraping orchestrator - extracts EVERYTHING"""
        print(f"🎨 Starting maximum extraction for: {self.url}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
            page = await context.new_page()
            
            try:
                await page.goto(self.url, wait_until='networkidle', timeout=30000)
                await asyncio.sleep(2)  # Let animations/lazy-load finish
                
                # Extract everything in parallel
                results = await asyncio.gather(
                    self.extract_screenshots(page),
                    self.extract_html_structure(page),
                    self.extract_colors(page),
                    self.extract_typography(page),
                    self.extract_css_styles(page),
                    self.extract_svgs(page),
                    self.extract_images(page),
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
                
                print(f"✅ Extraction complete! Saved to: {self.job_dir}")
                return design_data
                
            finally:
                await browser.close()
    
    async def extract_screenshots(self, page: Page) -> Dict:
        """Capture full page, viewport, and component screenshots"""
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
        print("🏗️ Analyzing HTML structure...")
        
        html = await page.content()
        soup = BeautifulSoup(html, 'html.parser')
        
        # Save raw HTML
        html_path = self.job_dir / "page.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        structure = {
            "title": soup.title.string if soup.title else "",
            "meta_description": soup.find('meta', attrs={'name': 'description'})['content'] 
                               if soup.find('meta', attrs={'name': 'description'}) else "",
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
    
    async def extract_colors(self, page: Page) -> List[Dict]:
        """Extract ALL colors from CSS, images, and computed styles"""
        print("🎨 Extracting color palette...")
        
        colors = []
        color_counts = {}
        
        # Get all computed styles
        color_data = await page.evaluate("""
            () => {
                const colors = new Set();
                const elements = document.querySelectorAll('*');
                
                elements.forEach(el => {
                    const styles = window.getComputedStyle(el);
                    const props = ['color', 'backgroundColor', 'borderColor', 'fill', 'stroke'];
                    
                    props.forEach(prop => {
                        const value = styles[prop];
                        if (value && value !== 'none' && value !== 'transparent' && 
                            !value.includes('rgba(0, 0, 0, 0)')) {
                            colors.add(value);
                        }
                    });
                });
                
                return Array.from(colors);
            }
        """)
        
        # Parse and normalize colors
        for color in color_data:
            try:
                # Convert to hex
                if color.startswith('rgb'):
                    rgb = re.findall(r'\d+', color)[:3]
                    hex_color = '#%02x%02x%02x' % tuple(map(int, rgb))
                elif color.startswith('#'):
                    hex_color = color
                else:
                    continue
                
                color_counts[hex_color] = color_counts.get(hex_color, 0) + 1
            except:
                continue
        
        # Sort by frequency
        sorted_colors = sorted(color_counts.items(), key=lambda x: x[1], reverse=True)
        
        for hex_color, count in sorted_colors[:50]:  # Top 50 colors
            try:
                rgb = tuple(int(hex_color[i:i+2], 16) for i in (1, 3, 5))
                colors.append({
                    "hex": hex_color,
                    "rgb": f"rgb({rgb[0]}, {rgb[1]}, {rgb[2]})",
                    "usage_count": count
                })
            except:
                continue
        
        return colors
    
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
                    
                    if (fontFamily) {
                        if (!fonts[fontFamily]) {
                            fonts[fontFamily] = {
                                sizes: new Set(),
                                weights: new Set(),
                                lineHeights: new Set(),
                                letterSpacings: new Set()
                            };
                        }
                        fonts[fontFamily].sizes.add(fontSize);
                        fonts[fontFamily].weights.add(fontWeight);
                        fonts[fontFamily].lineHeights.add(lineHeight);
                        fonts[fontFamily].letterSpacings.add(letterSpacing);
                    }
                });
                
                // Convert Sets to Arrays
                Object.keys(fonts).forEach(font => {
                    fonts[font].sizes = Array.from(fonts[font].sizes);
                    fonts[font].weights = Array.from(fonts[font].weights);
                    fonts[font].lineHeights = Array.from(fonts[font].lineHeights);
                    fonts[font].letterSpacings = Array.from(fonts[font].letterSpacings);
                });
                
                return fonts;
            }
        """)
        
        return font_data
    
    async def extract_css_styles(self, page: Page) -> Dict:
        """Extract all CSS stylesheets and inline styles"""
        print("💅 Extracting CSS styles...")
        
        # Get all stylesheet links
        stylesheets = await page.evaluate("""
            () => {
                return Array.from(document.styleSheets).map(sheet => {
                    try {
                        return {
                            href: sheet.href,
                            rules: Array.from(sheet.cssRules || []).map(rule => rule.cssText).slice(0, 100)
                        };
                    } catch (e) {
                        return { href: sheet.href, rules: [] };
                    }
                });
            }
        """)
        
        # Save CSS files
        css_files = []
        for i, sheet in enumerate(stylesheets):
            if sheet.get('rules'):
                css_content = '\n'.join(sheet['rules'])
                css_path = self.css_dir / f"stylesheet_{i}.css"
                with open(css_path, 'w') as f:
                    f.write(css_content)
                css_files.append(str(css_path.relative_to(self.output_dir)))
        
        return {
            "stylesheets": len(stylesheets),
            "saved_files": css_files
        }
    
    async def extract_svgs(self, page: Page) -> List[str]:
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
                    height: svg.getAttribute('height')
                }));
            }
        """)
        
        svg_files = []
        for svg_data in svgs:
            svg_path = self.svgs_dir / f"svg_{svg_data['index']}.svg"
            with open(svg_path, 'w') as f:
                f.write(svg_data['content'])
            svg_files.append(str(svg_path.relative_to(self.output_dir)))
        
        return svg_files
    
    async def extract_images(self, page: Page) -> List[Dict]:
        """Download all images (PNG, JPG, WebP)"""
        print("🖼️ Downloading images...")
        
        images = await page.evaluate("""
            () => {
                const imgs = document.querySelectorAll('img');
                return Array.from(imgs).map((img, i) => ({
                    index: i,
                    src: img.src,
                    alt: img.alt,
                    width: img.naturalWidth,
                    height: img.naturalHeight
                }));
            }
        """)
        
        downloaded_images = []
        for img_data in images[:50]:  # Limit to 50 images
            try:
                src = img_data['src']
                if src.startswith('data:'):
                    continue  # Skip data URLs for now
                
                img_response = await page.context.request.get(src)
                if img_response.ok:
                    content = await img_response.body()
                    ext = Path(urlparse(src).path).suffix or '.png'
                    img_path = self.images_dir / f"image_{img_data['index']}{ext}"
                    
                    with open(img_path, 'wb') as f:
                        f.write(content)
                    
                    downloaded_images.append({
                        "path": str(img_path.relative_to(self.output_dir)),
                        "alt": img_data['alt'],
                        "size": f"{img_data['width']}x{img_data['height']}"
                    })
            except:
                continue
        
        return downloaded_images
    
    async def extract_design_flow(self, page: Page) -> Dict:
        """Analyze navigation, sitemap, and user flows"""
        print("🗺️ Mapping design flow...")
        
        flow = await page.evaluate("""
            () => {
                const nav = document.querySelector('nav');
                const header = document.querySelector('header');
                const footer = document.querySelector('footer');
                
                const links = Array.from(document.querySelectorAll('a')).map(a => ({
                    text: a.textContent.trim(),
                    href: a.href,
                    isInternal: a.href.startsWith(window.location.origin)
                }));
                
                return {
                    has_nav: !!nav,
                    has_header: !!header,
                    has_footer: !!footer,
                    internal_links: links.filter(l => l.isInternal).length,
                    external_links: links.filter(l => !l.isInternal).length,
                    navigation_items: nav ? Array.from(nav.querySelectorAll('a')).map(a => a.textContent.trim()) : []
                };
            }
        """)
        
        return flow
    
    async def extract_layout_info(self, page: Page) -> Dict:
        """Extract grid systems, spacing, and layout patterns"""
        print("📏 Analyzing layout...")
        
        layout = await page.evaluate("""
            () => {
                const body = document.body;
                const styles = window.getComputedStyle(body);
                
                // Detect CSS Grid/Flexbox usage
                const gridElements = document.querySelectorAll('[style*="grid"], [class*="grid"]');
                const flexElements = document.querySelectorAll('[style*="flex"], [class*="flex"]');
                
                return {
                    max_width: styles.maxWidth,
                    padding: styles.padding,
                    margin: styles.margin,
                    grid_count: gridElements.length,
                    flex_count: flexElements.length,
                    container_width: body.offsetWidth
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
                    
                    if (animation !== 'none' || transition !== 'all 0s ease 0s') {
                        animated.push({
                            element: el.tagName,
                            class: el.className,
                            animation: animation,
                            transition: transition
                        });
                    }
                });
                
                return animated.slice(0, 20);  // Top 20 animated elements
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
