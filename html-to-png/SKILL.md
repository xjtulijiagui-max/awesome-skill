---
name: html-to-png
description: Automatically add "Save as PNG" screenshot functionality to HTML files. Use this skill whenever the user mentions: adding screenshot functionality to HTML, converting HTML to images, saving web pages as pictures, creating downloadable screenshots from HTML, adding export-to-image buttons, generating PNG from HTML content, or when they need to capture long scrolling HTML pages as complete images. Also trigger when users mention html2canvas, full-page screenshots, or need to share HTML content as image files.
---

# HTML to PNG Screenshot Skill

This skill adds one-click "Save as PNG" functionality to HTML files, allowing users to download entire HTML pages as high-resolution images with a single button click.

## When to Use This Skill

Trigger this skill when users ask to:
- Add screenshot/export functionality to an HTML file
- Convert HTML content to PNG images
- Create downloadable images from web pages
- Add "save as picture" buttons to HTML documents
- Generate high-resolution screenshots from HTML
- Capture long/scrolling HTML pages as complete images

## Core Implementation Strategy

You'll be adding three key components to the HTML file:

1. **html2canvas library** - The engine that captures HTML as canvas
2. **Fixed-width container** - Ensures consistent screenshot dimensions
3. **Screenshot button and function** - UI and logic to trigger the capture

## Step-by-Step Implementation

### Step 1: Add html2canvas Library

Add this script tag to the `<head>` section, **before the closing `</head>` tag**:

```html
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
```

**Why version 1.4.1 specifically?** Later versions may have API changes. This version is battle-tested and stable. Using `latest` is risky as it can break without warning.

### Step 2: Fix Body Width (Critical for Consistency)

Add or modify CSS to fix the body width. This prevents screenshots from varying based on browser window size.

```css
body {
    width: 1200px;       /* Fixed canvas width - adjust if needed */
    margin: 0 auto;
    overflow-x: hidden;
}
```

If the HTML has a main content wrapper, add a container class:

```css
.screenshot-container {
    width: 1200px;
    margin: 0;
    padding: 0;
    overflow: hidden;
}
```

Wrap the main content in this container:
```html
<div class="screenshot-container">
    <!-- All existing content goes here -->
</div>
```

**Why fixed width?** Without this, screenshots will have different dimensions depending on the user's browser size, leading to inconsistent results.

### Step 3: Handle Images (CORS Issue - Critical)

**Important:** html2canvas cannot capture external images due to CORS restrictions. All images must be embedded as base64 data URLs.

**Check for external images:**
```html
<!-- This will FAIL - external URL -->
<img src="https://example.com/image.jpg" />

<!-- This WORKS - base64 embedded -->
<img src="data:image/png;base64,iVBORw0KGgo..." />
```

**What to do:**
- If images are already base64: Great, no action needed
- If images are external URLs: Warn the user that they need to convert images to base64 first
- For local files: Offer to convert them using a Node.js script

**Why is this necessary?** Browsers block canvas from accessing cross-origin images for security reasons. html2canvas will either fail or produce blank spaces where external images should be.

### Step 4: Add the Screenshot Button

Add this fixed-position button just before the closing `</body>` tag:

```html
<div id="screenshot-btn" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
    <button onclick="captureScreenshot()" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 15px 30px; border-radius: 50px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
        📸 保存为图片
    </button>
</div>
```

**Why fixed position?** The button stays in a consistent screen location and can be hidden before capturing so it doesn't appear in the screenshot.

### Step 5: Add the Capture Function

Add this script just before the closing `</body>` tag, after the button:

```html
<script>
async function captureScreenshot() {
    const btn = document.getElementById('screenshot-btn');
    btn.style.display = 'none'; // Hide button before capture

    // Show loading indicator
    const loading = document.createElement('div');
    loading.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.8); color: white; padding: 30px 50px; border-radius: 20px; z-index: 10000; font-size: 18px;';
    loading.textContent = '正在生成图片，请稍候...';
    document.body.appendChild(loading);

    try {
        // Detect background color from body
        const computedStyle = window.getComputedStyle(document.body);
        const bgColor = computedStyle.backgroundColor;

        const canvas = await html2canvas(document.body, {
            scale: 2,                    // 2x for high-resolution (Retina displays)
            useCORS: true,               // Attempt to load cross-origin images
            allowTaint: true,            // Don't fail if tainted images exist
            backgroundColor: bgColor,    // Use actual page background
            logging: false               // Disable console logs
        });

        // Convert to blob and download
        canvas.toBlob(function(blob) {
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'screenshot.png';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            loading.textContent = '✓ 图片已保存！';
            setTimeout(() => {
                loading.remove();
                btn.style.display = '';
            }, 2000);
        }, 'image/png');

    } catch (error) {
        loading.textContent = '✗ 截图失败: ' + error.message;
        setTimeout(() => {
            loading.remove();
            btn.style.display = '';
        }, 3000);
    }
}
</script>
```

**Key parameter explanations:**
- `scale: 2` - Outputs at 2x resolution for crisp text on high-DPI displays
- `useCORS: true` - Attempts to load cross-origin images (though base64 is still recommended)
- `allowTaint: true` - Continues even if some images can't be loaded
- `backgroundColor` - Prevents transparent backgrounds from turning black in PNG
- **Do NOT set** `width`, `height`, `windowWidth`, or `windowHeight` - let html2canvas auto-calculate the full page height

### Step 6: Output the Modified File

Save the modified HTML with a clear filename, such as:
- `original-with-screenshot.html`
- `original-exportable.html`

## Common Issues and Solutions

| Symptom | Cause | Solution |
|---------|-------|----------|
| Screenshot is only one screen height, content is cut off | Setting `height` parameter in html2canvas options | Remove any `height` parameter; let the library auto-calculate |
| Images appear as blank/white boxes | External images (CORS blocked) | Convert all images to base64 data URLs |
| Background appears black instead of actual color | `backgroundColor` not set | Detect and set `backgroundColor` from computed style |
| Button appears in the screenshot | Button not hidden during capture | Ensure `btn.style.display = 'none'` is called before html2canvas |
| Text shows as boxes/gibberish | Custom fonts not loaded before capture | Wait for fonts: `document.fonts.ready.then(() => { ... })` |

## Complete Template Example

If starting from scratch, use this template structure:

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Page Title</title>
    <!-- Fonts (optional) -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;700&display=swap" rel="stylesheet">
    <!-- Tailwind or other CSS frameworks (optional) -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- html2canvas - MUST be in head before closing tag -->
    <script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
    <style>
        * { font-family: 'Noto Sans SC', sans-serif; }
        body {
            width: 1200px;
            margin: 0 auto;
            background: #YOUR_BACKGROUND_COLOR;
        }
        .screenshot-container {
            width: 1200px;
            margin: 0;
            padding: 0;
            overflow: hidden;
        }
    </style>
</head>
<body>

    <!-- Content wrapper -->
    <div class="screenshot-container">
        <!-- All your content here -->
        <!-- All images must be base64 encoded -->
    </div>

    <!-- Screenshot button -->
    <div id="screenshot-btn" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;">
        <button onclick="captureScreenshot()" style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 15px 30px; border-radius: 50px; font-size: 16px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.3);">
            📸 保存为图片
        </button>
    </div>

    <script>
    async function captureScreenshot() {
        const btn = document.getElementById('screenshot-btn');
        btn.style.display = 'none';
        const loading = document.createElement('div');
        loading.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.8); color: white; padding: 30px 50px; border-radius: 20px; z-index: 10000; font-size: 18px;';
        loading.textContent = '正在生成图片，请稍候...';
        document.body.appendChild(loading);
        try {
            const computedStyle = window.getComputedStyle(document.body);
            const canvas = await html2canvas(document.body, {
                scale: 2,
                useCORS: true,
                allowTaint: true,
                backgroundColor: computedStyle.backgroundColor,
                logging: false,
            });
            canvas.toBlob(blob => {
                const a = Object.assign(document.createElement('a'), {
                    href: URL.createObjectURL(blob),
                    download: 'screenshot.png'
                });
                document.body.appendChild(a);
                a.click();
                a.remove();
                loading.textContent = '✓ 图片已保存！';
                setTimeout(() => { loading.remove(); btn.style.display = ''; }, 2000);
            }, 'image/png');
        } catch (e) {
            loading.textContent = '✗ 截图失败: ' + e.message;
            setTimeout(() => { loading.remove(); btn.style.display = ''; }, 3000);
        }
    }
    </script>
</body>
</html>
```

## Advanced: Converting External Images to Base64

If the HTML has external images that need to be converted, you can use this Node.js approach:

```javascript
const fs = require('fs');
const path = require('path');

function imageToBase64(imagePath) {
    const ext = path.extname(imagePath).slice(1);
    const data = fs.readFileSync(imagePath);
    return `data:image/${ext};base64,${data.toString('base64')}`;
}
```

However, for complex cases, recommend the user handle image conversion separately, as this skill focuses on adding the screenshot functionality itself.

## Testing the Implementation

After adding the functionality:
1. Open the HTML file in a browser
2. Verify the screenshot button appears in the bottom-right corner
3. Click the button and wait for the "正在生成图片，请稍候..." message
4. Check that the PNG downloads successfully
5. Open the PNG and verify:
   - All content is captured (no cutoff)
   - Images render correctly (not blank)
   - Background color is correct
   - Text is crisp (2x scale)
   - The screenshot button does NOT appear in the image

## Summary

When implementing this skill:
1. Add html2canvas@1.4.1 to `<head>`
2. Fix body width to prevent layout shifts
3. Ensure all images are base64-encoded
4. Add fixed-position screenshot button
5. Add captureScreenshot() function with proper error handling
6. Test thoroughly before delivering to user

The key insight is that html2canvas needs specific configuration to work reliably: fixed widths, base64 images, and proper background color handling are essential for success.
