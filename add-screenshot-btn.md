# Add Screenshot Button Skill

## Description

Add a "Save as Image" button to HTML files using html2canvas. Automatically handles cross-origin issues by inlining SVG images.

## Usage

```xml
<user>
给这个HTML添加截图功能: path/to/file.html
</user>
```

## Implementation

### Step 1: Read the target HTML file

Read the file to understand its structure, especially:
- Whether it already has html2canvas
- Whether it contains external SVG images
- The main content container to capture

### Step 2: Add html2canvas library

Add the CDN script before closing `</head>` tag:

```html
<script src="https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js"></script>
```

If the `<style>` block ends right before `</head>`, add the script after it.

### Step 3: Add screenshot button

Add a fixed-position button that triggers the screenshot function:

```html
<button class="screenshot-btn" onclick="captureScreenshot()"
    style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;
           background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
           color: white; border: none; padding: 15px 30px; border-radius: 50px;
           font-size: 16px; font-weight: bold; cursor: pointer;
           box-shadow: 0 10px 30px rgba(0,0,0,0.3); transition: all 0.3s;">
    📸 保存为图片
</button>
```

### Step 4: Inline external SVG images (Critical!)

Find `<img>` tags that reference `.svg` files and replace them with inline SVG:

1. Read the referenced SVG file
2. Replace `<img src="xxx.svg">` with the actual SVG content
3. Remove `crossorigin` attributes as they're not needed for inline SVG

### Step 5: Add captureScreenshot JavaScript function

Add this script before closing `</body>` tag:

```javascript
<script>
async function captureScreenshot() {
    const btn = document.querySelector('.screenshot-btn');
    const originalDisplay = btn.style.display;
    btn.style.display = 'none';

    const loading = document.createElement('div');
    loading.id = 'loading';
    loading.style.cssText = 'position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%); background: rgba(0,0,0,0.8); color: white; padding: 30px 50px; border-radius: 20px; z-index: 10000; font-size: 18px;';
    loading.textContent = '正在生成图片，请稍候...';
    document.body.appendChild(loading);

    try {
        const element = document.querySelector('.poster') || document.body;
        const canvas = await html2canvas(element, {
            scale: 2,
            useCORS: true,
            allowTaint: true,
            backgroundColor: null,
            logging: false,
            foreignObjectRendering: false
        });

        canvas.toBlob(function(blob) {
            if (!blob) {
                throw new Error('Failed to create blob');
            }

            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'screenshot.png';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);

            loading.textContent = '✓ 图片已保存！';
            loading.style.background = 'rgba(0, 128, 0, 0.8)';

            setTimeout(() => {
                loading.remove();
                btn.style.display = originalDisplay;
            }, 2000);
        }, 'image/png');

    } catch (error) {
        console.error('Screenshot error:', error);
        loading.textContent = '✗ 截图失败: ' + error.message;
        loading.style.background = 'rgba(255, 0, 0, 0.8)';

        setTimeout(() => {
            loading.remove();
            btn.style.display = originalDisplay;
        }, 3000);
    }
}
</script>
```

### Step 6: Update print media query (if exists)

If there's a `@media print` rule that hides buttons, update it to also hide the screenshot button:

```css
@media print {
    .print-btn, .screenshot-btn {
        display: none;
    }
}
```

## Error Handling

- If `Tainted canvas` error: Make sure all SVG images are inlined
- If `toBlob` fails: Check that canvas width/height are reasonable
- If screenshot is blank: Try setting explicit `backgroundColor` in html2canvas options

## Customization

- **Button position**: Change `bottom` and `right` in button style
- **Download filename**: Change `a.download = 'screenshot.png'`
- **Capture element**: Change `document.querySelector('.poster')` to target specific element
- **Background color**: Set `backgroundColor` option (hex color or `null` for transparent)
