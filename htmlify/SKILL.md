# HTMLify Skill - Convert Text/Markdown to Beautiful HTML

You are converting text or markdown content to beautifully styled HTML pages.

## Design Standards

Apply these design principles to every HTML page you create:

### Visual Style
- **Apple-style design** with clean, modern aesthetics
- **Particle effects** for dynamic backgrounds (subtle, non-distracting)
- **Dark theme** as the default color scheme
- **White text on code blocks** for maximum readability
- **Card-style layout** for content organization
- **Responsive design** that works on all screen sizes

### Layout Structure
- **Left navigation sidebar** for multi-section content
  - Fixed position on desktop
  - Collapsible on mobile
  - Smooth scroll to sections
- **Main content area** with proper spacing and hierarchy
- **Maximum width container** (typically 1200-1400px) for readability

### Typography
- Font family: `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
- Clear hierarchy with proper heading sizes
- Readable line length (50-75 characters per line)
- Adequate line height (1.5-1.7 for body text)

### Color Scheme
```css
/* Dark theme colors */
--bg-primary: #0a192f;
--bg-secondary: #112240;
--bg-card: #1a2744;
--text-primary: #e6f1ff;
--text-secondary: #8892b0;
--accent: #64ffda;
--border: rgba(255, 255, 255, 0.1);
```

### Code Blocks
- Dark background with syntax highlighting
- White or light-colored text
- Monospace font family
- Proper padding and border-radius

### Interactive Elements
- Smooth transitions and hover effects
- Subtle animations (0.2-0.3s duration)
- Card hover effects (elevation, shadow)
- Button states with visual feedback

## Workflow

1. **Read the input file** - Use Read tool to get the source content
2. **Analyze the structure** - Identify sections, headings, code blocks, lists
3. **Convert to HTML** - Transform markdown/text to semantic HTML
4. **Apply styling** - Add CSS that follows the design standards above
5. **Verify output** - Check readability, responsiveness, and visual polish
6. **Return result** - Provide the HTML file path and preview

## Output Format

Generate a single, self-contained HTML file with:
- `<!DOCTYPE html>` declaration
- `<head>` with meta tags, title, and embedded CSS
- `<body>` with semantic HTML structure
- Optional: Minimal JavaScript for navigation/particles

## Quality Checklist

Before returning the result, verify:
- [ ] Dark theme applied consistently
- [ ] Code blocks have white/light text
- [ ] Left navigation included (for multi-section content)
- [ ] Responsive design works on mobile
- [ ] Particle effects are subtle and non-distracting
- [ ] Typography hierarchy is clear
- [ ] All interactive elements have hover states
- [ ] Content is readable and visually polished

## Example Usage

```
User: Convert my-notes.md to HTML
Assistant: I'll convert your markdown notes to a beautifully styled HTML page with Apple-style design and dark theme.
```

## Notes

- Always preserve the original content structure and meaning
- Add visual enhancements without compromising readability
- Use CDN links for external libraries when needed (e.g., syntax highlighting)
- Keep the HTML file self-contained when possible
- Test responsive behavior if previewing in browser
