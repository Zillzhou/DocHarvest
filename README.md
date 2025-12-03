# DocHarvest

Export Feishu/Lark documents to Markdown, PDF, and Word formats.

[![Python](https://img.shields.io/badge/python-3.9+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Features

- **🎨 Modern UI**: Material Design interface with smooth animations
- **⚡ Ultra-Fast**: 100-200 documents in 60-90 seconds (Turbo Mode)
- **📦 Multi-format**: Markdown, PDF, Word - export in any combination
- **🔄 Smart Export**: Async I/O with up to 20 concurrent connections
- **🌲 Wiki Batch**: Recursively export entire Wiki with structure preserved
- **💾 Auto-Save**: Configurations saved automatically

## Quick Start

**Install and Run:**
```bash
pip install -r requirements.txt
python src/main.py
```

**Build Executable:**
```bash
cd scripts
build.bat  # Windows
./build.sh # Linux/Mac
```

## Setup

### 1. Create Feishu App

Visit [Feishu Open Platform](https://open.feishu.cn/), create an app, get **App ID** and **App Secret**.

### 2. Configure Permissions

Add these scopes in app settings:
- `docx:document:readonly` - Read documents
- `docs:read` - Read content  
- `wiki:wiki:readonly` - Access Wiki (for batch export)
- `drive:export:readonly` - Export PDF/Word

### 3. Configure App

Copy `config.json.example` to `config.json` and fill in your credentials.

## Usage

**Simple 3-Step Process:**

1. **Configure** - Enter App ID and App Secret
2. **Select** - Paste Wiki link + choose export formats  
3. **Export** - Click "开始导出" and wait

**Default Settings:**
- ✅ Turbo Mode enabled (15 concurrent connections)
- ✅ Optimized for maximum speed
- ✅ Auto-save configuration

**Supported Links:**
```
https://xxx.feishu.cn/wiki/xxx (Wiki - Recommended)
https://xxx.feishu.cn/docx/xxx (Single document)
```

## Performance

| Documents | Time (Turbo) | Speed |
|-----------|--------------|-------|
| 50 docs   | 30-45s       | ~1 doc/sec |
| 100 docs  | 60-90s       | ~1 doc/sec |
| 200 docs  | 2-3 min      | ~1 doc/sec |

*Using PDF-only export with 15 parallel workers*

## Project Structure

```
DocHarvest/
├── src/
│   ├── main.py                # Entry point
│   ├── apple_gui.py           # Apple HIG UI (Material Design)
│   ├── workers.py             # Background threads
│   ├── async_exporter.py      # Async exporter (Turbo Mode)
│   ├── parallel_crawler.py    # Parallel Wiki crawler
│   ├── feishu_api.py          # API client
│   └── wiki_crawler.py        # Wiki batch exporter
├── scripts/                   # Build scripts
├── APPLE_DESIGN.md           # Apple HIG design specs
├── TURBO_MODE.md             # Turbo mode documentation
├── QUICKSTART.md             # Quick start guide
├── requirements.txt
└── config.json.example
```

**Detailed structure**: See [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)

## Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Quick start guide
- **[APPLE_DESIGN.md](APPLE_DESIGN.md)** - Apple HIG design specifications
- **[TURBO_MODE.md](TURBO_MODE.md)** - Ultra-fast export mode (technical)
- **[SPEED_BOOST.md](SPEED_BOOST.md)** - Performance optimization tips
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Complete project structure
- **[CHANGELOG.md](CHANGELOG.md)** - Version history

## License

MIT License - see [LICENSE](LICENSE)

## Acknowledgments

Thanks to Feishu Open Platform for API support.

---

*For personal and educational use only.*
