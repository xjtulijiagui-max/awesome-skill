---
name: markitdown
description: Use this skill whenever the user wants to convert any file format to Markdown. Supports PDF, DOCX, PPTX, XLSX, audio, video, images, and more. This is Microsoft's markitdown tool that converts various document formats to clean Markdown text.
license: MIT
---

# MarkItDown - Convert Any File to Markdown

## Overview

MarkItDown is Microsoft's tool that converts various file formats to Markdown. It supports documents, presentations, spreadsheets, audio, video, images, and more.

## Quick Start

### Basic Usage - Convert a File

```bash
# Convert a file and output to terminal
python -m markitdown document.pdf

# Convert and save to file
python -m markitdown document.pdf -o document.md

# Using pipes
cat document.docx | python -m markitdown > output.md
```

## Supported File Formats

| Format | Extensions | Notes |
|--------|-----------|-------|
| **Documents** | .docx, .doc | Word documents |
| **PDF** | .pdf | PDF documents |
| **Presentations** | .pptx, .ppt | PowerPoint presentations |
| **Spreadsheets** | .xlsx, .xls, .csv | Excel files |
| **Audio** | .mp3, .wav, .m4a, .ogg | Uses speech recognition |
| **Video** | .mp4, .avi, .mov, .mkv | Extracts audio then transcribes |
| **Images** | .png, .jpg, .jpeg, .gif, .bmp | Uses OCR for text extraction |
| **HTML** | .html, .htm | Web pages |
| **Text** | .txt, .md, .rst | Plain text files |
| **Other** | .json, .xml | Structured data |

## Command-Line Options

```bash
python -m markitdown [OPTIONS] [filename]

Options:
  -o, --output OUTPUT      Output file name
  -x, --extension EXT      File extension hint
  -m, --mime-type MIME     MIME type hint
  -c, --charset CHARSET    Character set hint (e.g., UTF-8)
  -d, --use-docintel       Use Azure Document Intelligence
  -e, --endpoint ENDPOINT  Azure Document Intelligence endpoint
  -p, --use-plugins        Use 3rd-party plugins
  --list-plugins           List available plugins
  --keep-data-uris         Keep base64-encoded images
  -h, --help               Show help
  -v, --version            Show version
```

## Python API Usage

```python
from markitdown import markitdown

# Convert a file
result = markitdown.convert("document.pdf")
print(result.text_content)

# Convert and save to file
result = markitdown.convert("presentation.pptx")
with open("output.md", "w", encoding="utf-8") as f:
    f.write(result.text_content)

# Convert with options
from markitdown._markitdown import MarkItDown
md = MarkItDown()
result = md.convert("document.docx")
```

## Common Use Cases

### Convert Word Document to Markdown

```bash
python -m markitdown report.docx -o report.md
```

### Extract Text from PDF

```bash
python -m markitdown research_paper.pdf -o paper.md
```

### Convert PowerPoint to Markdown

```bash
python -m markitdown presentation.pptx -o slides.md
```

### Transcribe Audio File

```bash
# This will convert speech to text
python -m markitdown meeting.mp3 -o meeting_transcript.md
```

### Extract Text from Image (OCR)

```bash
# Extract text from scanned document or image
python -m markitdown screenshot.png -o extracted_text.md
```

### Convert Excel to Markdown Table

```bash
python -m markitdown spreadsheet.xlsx -o table.md
```

### Batch Convert Multiple Files

```bash
# Convert all PDFs in a directory
for file in *.pdf; do
    python -m markitdown "$file" -o "${file%.pdf}.md"
done

# Or using find
find . -name "*.docx" -exec python -m markitdown {} -o {}.md \;
```

## Tips and Best Practices

### 1. Output Encoding
Always specify UTF-8 encoding when saving to file:
```bash
python -m markitdown input.pdf -o output.md
# Or redirect with proper encoding
python -m markitdown input.pdf | iconv -f UTF-8 -t UTF-8 > output.md
```

### 2. Large Files
For very large files, consider redirecting output:
```bash
python -m markitdown large_file.pdf > large_output.md
```

### 3. Audio/Video Processing
- Audio transcription requires an internet connection for speech recognition
- Video files extract audio first, then transcribe
- Processing time depends on file length

### 4. Image OCR
- OCR works best with clear, high-resolution images
- Supports multiple languages
- Scanned documents should be at 300 DPI or higher

### 5. PDF Handling
- Text-based PDFs: Fast and accurate
- Scanned PDFs: Uses OCR, slower processing
- Complex layouts: May need manual cleanup

## Error Handling

### File Not Supported
```bash
# If you get an unsupported file error, try specifying the extension
python -m markitdown unknown_file -x .pdf
```

### Encoding Issues
```bash
# Specify charset if needed
python -m markitdown document.txt -c UTF-8
```

### Large File Memory Issues
```bash
# Use streaming for very large files
cat large_file.pdf | python -m markitdown > output.md
```

## Integration Examples

### With Pandas (Excel Files)
```python
import pandas as pd
from markitdown import markitdown

# Convert Excel to Markdown
result = markitdown.convert("data.xlsx")
print(result.text_content)

# Or process with Pandas first
df = pd.read_excel("data.xlsx")
markdown = df.to_markdown(index=False)
with open("output.md", "w") as f:
    f.write(markdown)
```

### Batch Processing Script
```python
from pathlib import Path
from markitdown import markitdown

def convert_directory(input_dir, output_dir):
    """Convert all supported files in a directory"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    for file in input_path.glob("*"):
        if file.is_file():
            try:
                result = markitdown.convert(str(file))
                output_file = output_path / f"{file.stem}.md"
                output_file.write_text(result.text_content, encoding="utf-8")
                print(f"✓ Converted: {file.name}")
            except Exception as e:
                print(f"✗ Failed: {file.name} - {e}")

# Usage
convert_directory("./input", "./output")
```

## Troubleshooting

### Issue: "Couldn't find ffmpeg"
**Solution**: Install ffmpeg for audio/video processing
```bash
# Windows (using chocolatey)
choco install ffmpeg

# macOS
brew install ffmpeg

# Linux
sudo apt-get install ffmpeg
```

### Issue: Poor OCR Results
**Solutions**:
- Ensure images are high resolution (300+ DPI)
- Pre-process images: increase contrast, remove noise
- Try different image formats (PNG vs JPG)

### Issue: Audio Transcription Fails
**Solutions**:
- Check internet connection
- Ensure audio is clear (minimal background noise)
- Try converting to different audio format first

### Issue: PDF Text Extraction is Garbled
**Solutions**:
- PDF might be scanned; markitdown will use OCR
- For complex layouts, manual cleanup may be needed
- Try using `--use-docintel` for better results (requires Azure)

## Performance Tips

1. **Batch Processing**: Process multiple files in parallel
2. **File Size**: Larger files take longer; consider splitting first
3. **Format Choice**: Some formats convert faster than others
4. **Caching**: Cache results to avoid re-conversion

## Next Steps

- Experiment with different file formats
- Integrate into your document processing pipeline
- Combine with other tools for complete workflows
- Check Microsoft's markitdown GitHub for updates

## Links

- GitHub: https://github.com/microsoft/markitdown
- Documentation: https://github.com/microsoft/markitdown/tree/main/docs
- Issues: https://github.com/microsoft/markitdown/issues
