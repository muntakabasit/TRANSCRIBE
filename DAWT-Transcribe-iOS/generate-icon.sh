#!/bin/bash

# DAWT-Transcribe App Icon Generator
# Creates a 1024x1024 app icon with microphone/waveform design

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT_DIR="$SCRIPT_DIR/DAWT-Transcribe/DAWT-Transcribe/Assets.xcassets/AppIcon.appiconset"

echo "🎨 Generating DAWT-Transcribe App Icon..."
echo "📁 Output: $OUTPUT_DIR"

# Check if ImageMagick is installed
if ! command -v magick &> /dev/null && ! command -v convert &> /dev/null; then
    echo "❌ ImageMagick not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install imagemagick
    else
        echo "❌ Homebrew not found. Please install ImageMagick manually:"
        echo "   brew install imagemagick"
        exit 1
    fi
fi

# Use 'magick' command (ImageMagick 7) or fall back to 'convert' (ImageMagick 6)
if command -v magick &> /dev/null; then
    CONVERT_CMD="magick"
else
    CONVERT_CMD="convert"
fi

echo "✅ Using ImageMagick: $CONVERT_CMD"

# Create 1024x1024 app icon with modern gradient design
echo "🎨 Creating 1024x1024 master icon..."

$CONVERT_CMD -size 1024x1024 \
    gradient:'#4A90E2-#7B68EE' \
    -virtual-pixel none \
    \( +clone -distort SRT '0,0 1,1 0' -blur 0x40 \) \
    -compose blend -define compose:args=50 -composite \
    \( -size 1024x1024 xc:none \
       -fill white \
       -draw "roundrectangle 0,0 1023,1023 180,180" \
    \) -compose DstIn -composite \
    "$OUTPUT_DIR/icon-1024.png"

# Add microphone/audio wave design
echo "🎤 Adding microphone icon..."

$CONVERT_CMD "$OUTPUT_DIR/icon-1024.png" \
    \( -size 512x512 xc:none \
       -fill "rgba(255,255,255,0.95)" \
       -draw "circle 256,180 256,120" \
       -draw "roundrectangle 200,180 312,340 20,20" \
       -draw "path 'M 256,340 L 256,390'" \
       -draw "roundrectangle 216,380 296,400 10,10" \
       -draw "ellipse 256,300 100,100 200,340" \
       -strokewidth 12 \
       -stroke "rgba(255,255,255,0.95)" \
       -fill none \
       -draw "arc 156,200 356,400 200,340" \
    \) -gravity center -composite \
    \( -size 1024x1024 xc:none \
       -fill "rgba(255,255,255,0.4)" \
       -draw "path 'M 256,650 Q 356,680 456,650'" \
       -draw "path 'M 256,700 Q 406,750 556,700'" \
       -draw "path 'M 256,750 Q 456,820 656,750'" \
       -strokewidth 8 \
       -stroke "rgba(255,255,255,0.4)" \
    \) -gravity center -composite \
    "$OUTPUT_DIR/icon-1024.png"

echo "✅ Master icon created: icon-1024.png"

# Update Contents.json to reference the icon
cat > "$OUTPUT_DIR/Contents.json" << 'EOF'
{
  "images" : [
    {
      "filename" : "icon-1024.png",
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
EOF

echo "✅ Contents.json updated"
echo ""
echo "🎉 App icon generated successfully!"
echo "📱 Open Xcode → Assets.xcassets → AppIcon to verify"
echo ""
echo "Next steps:"
echo "1. Open Xcode and verify the icon appears"
echo "2. Build and run the app to test"
echo "3. If you want a custom design, replace icon-1024.png with your own 1024x1024 image"
