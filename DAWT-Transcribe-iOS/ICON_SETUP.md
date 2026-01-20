# DAWT-Transcribe App Icon Setup

## Quick Start (Automated)

Run the icon generator script:

```bash
cd /Users/abdulbasitmuntaka/DAWT_Transcriber/DAWT-Transcribe-iOS
./generate-icon.sh
```

This will:
- ✅ Create a 1024x1024 app icon with microphone/waveform design
- ✅ Save it to `Assets.xcassets/AppIcon.appiconset/icon-1024.png`
- ✅ Update `Contents.json` to reference the icon
- ✅ Ready for Xcode build

---

## Modern iOS App Icon Requirements

Since iOS 13+, you only need **ONE size**: **1024x1024px**

Xcode automatically generates all other sizes from this master icon.

### Required Specifications:
- **Format**: PNG (no transparency/alpha channel)
- **Size**: 1024×1024 pixels
- **Color Space**: sRGB or Display P3
- **Shape**: Square (Xcode adds rounded corners automatically)

---

## Option 1: Use Generated Icon (Recommended)

The `generate-icon.sh` script creates a professional blue gradient icon with:
- Microphone symbol
- Audio waveforms
- Modern iOS design

Just run the script and you're done!

---

## Option 2: Use Your Own Custom Icon

If you have a custom 1024x1024 icon:

### Step 1: Prepare Your Icon
```bash
# Resize to exact 1024x1024 if needed (using macOS sips)
sips -z 1024 1024 your-icon.png --out icon-1024.png

# Remove alpha channel if present
sips -s format png --setProperty formatOptions normal icon-1024.png
```

### Step 2: Add to Xcode
```bash
# Copy to AppIcon asset catalog
cp icon-1024.png DAWT-Transcribe/DAWT-Transcribe/Assets.xcassets/AppIcon.appiconset/icon-1024.png
```

### Step 3: Verify Contents.json
The `AppIcon.appiconset/Contents.json` should look like this:

```json
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
```

---

## Option 3: Use SF Symbols (Quick & Apple-Native)

Create a simple icon using SF Symbols:

```bash
# Create a blue background with SF Symbol
# (Requires manual creation in design tool or Keynote)

# Steps:
# 1. Open Keynote or Preview
# 2. Create 1024x1024 canvas
# 3. Add gradient background
# 4. Add SF Symbol: "mic.fill" or "waveform"
# 5. Export as PNG at 1024x1024
# 6. Save as icon-1024.png
```

---

## Verify Installation in Xcode

1. **Open Xcode**
   ```bash
   open DAWT-Transcribe/DAWT-Transcribe.xcodeproj
   ```

2. **Navigate to Assets**
   - Left sidebar → `DAWT-Transcribe` folder
   - Click `Assets.xcassets`
   - Click `AppIcon`

3. **Check Icon**
   - You should see your icon in the "iOS App Store" slot (1024x1024)
   - Xcode will show a preview of how it looks on different devices

4. **Build and Test**
   ```
   Product → Clean Build Folder (Cmd+Shift+K)
   Product → Build (Cmd+B)
   Product → Run (Cmd+R)
   ```

5. **Verify on Device**
   - Check Home Screen
   - Check Settings app icon
   - Check App Switcher

---

## Troubleshooting

### Icon Not Showing Up
1. Clean build folder: `Product → Clean Build Folder`
2. Delete DerivedData: `Xcode → Preferences → Locations → DerivedData → Delete`
3. Restart Xcode
4. Rebuild project

### Alpha Channel Error
If you see "The app icon set has an unassigned child":
```bash
# Remove alpha channel
sips -s format png --setProperty formatOptions normal icon-1024.png
```

### Wrong Size Error
```bash
# Check current size
sips -g pixelWidth -g pixelHeight icon-1024.png

# Resize if needed
sips -z 1024 1024 icon-1024.png
```

---

## Design Tips

### Good App Icon Characteristics:
- ✅ Simple and recognizable at small sizes
- ✅ Unique and memorable
- ✅ Works in light and dark mode
- ✅ No text (text is hard to read at small sizes)
- ✅ High contrast
- ✅ Consistent with app purpose

### For DAWT-Transcribe:
- Primary symbol: Microphone 🎤
- Secondary elements: Audio waveforms, sound waves
- Color scheme: Blue/Purple gradient (professional, tech-forward)
- Style: Modern, clean, iOS-native look

---

## Next Steps

After icon is installed:

1. ✅ Build in Xcode (should succeed without warnings)
2. ✅ Test on physical device
3. ✅ Take App Store screenshots with the icon visible
4. ✅ Ready for TestFlight/App Store submission

---

## Resources

- [Apple Human Interface Guidelines - App Icons](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- [SF Symbols App](https://developer.apple.com/sf-symbols/)
- [App Icon Generator](https://appicon.co) - Online tool if you prefer
