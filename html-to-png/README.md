# HTML to PNG Screenshot Skill

A Claude Code skill that automatically adds "Save as PNG" functionality to HTML files.

## What It Does

This skill modifies HTML files to include:
- A floating "📸 保存为图片" (Save as Image) button
- One-click screenshot functionality using html2canvas
- High-resolution (2x) PNG output
- Full-page capture (no content cutoff)

## When to Use

Trigger this skill when you need to:
- Add screenshot/export functionality to HTML
- Convert HTML content to downloadable PNG images
- Create shareable image versions of web pages
- Add "save as picture" buttons to HTML documents

## Key Features

✅ **Full-page screenshots** - Captures entire HTML document, no height limits
✅ **High resolution** - 2x scale for crisp text on all displays
✅ **User-friendly** - Simple button with loading indicator
✅ **No external dependencies** - Uses CDN-hosted html2canvas library
✅ **Handles complex layouts** - Works with Tailwind, custom CSS, gradients, etc.

## Requirements & Limitations

⚠️ **Images must be base64-encoded** - External images (https://...) won't render in screenshots due to browser CORS restrictions. Convert images to base64 data URLs before using.

⚠️ **Fixed width required** - The skill sets body width to 1200px for consistent screenshots. Adjust if needed.

## Quick Start

1. Install this skill in Claude Code
2. Provide your HTML file path
3. The skill will add all necessary code
4. Open the modified HTML in a browser
5. Click the floating button to save as PNG

## Example Usage

```
You: Add screenshot functionality to my HTML file at ./course-brochure.html

Claude: [Uses this skill to modify the file]
```

## Technical Details

- **Library**: html2canvas v1.4.1 (stable, CDN-hosted)
- **Output format**: PNG (2x resolution)
- **Browser support**: All modern browsers with Canvas API
- **File size**: Depends on content; typically 500KB-5MB for full pages

## File Structure

```
html-to-png/
├── SKILL.md              # Main skill instructions
├── README.md             # This file
├── evals/
│   └── evals.json        # Test cases for the skill
└── scripts/
    └── image-to-base64.js # Optional helper for converting images
```

## Testing

The skill includes 3 test cases covering:
1. Existing HTML with base64 images
2. Simple HTML from scratch
3. HTML with external images (CORS warning)

## Credits

Created using the Skill Creator framework by Anthropic.
