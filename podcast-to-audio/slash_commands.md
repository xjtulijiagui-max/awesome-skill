# Slash Commands

## /podcast-to-audio

Extract and download podcast audio from episode pages.

**Usage**:
```
/podcast-to-audio <url>
```

**Examples**:
```
/podcast-to-audio https://www.xiaoyuzhoufm.com/episode/69de68cfb977fb2c47f1ee14
/podcast-to-audio https://www.youtube.com/watch?v=n1E9IZfvGMA
```

**What it does**:
- Extracts audio URL from podcast episode page
- Downloads audio file to `./audio` directory
- Saves metadata JSON file alongside audio
- Shows download progress

**Supported platforms**:
- Xiaoyuzhou (小宇宙)
- YouTube
- Any platform with `og:audio` or JSON-LD audio metadata
