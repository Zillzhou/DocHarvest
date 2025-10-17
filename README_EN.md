# DocHarvest 📄

> 🚀 A powerful desktop application for exporting Feishu/Lark documents to Markdown

A Python + PyQt5 based desktop application for fetching document content from Feishu share links and exporting them as Markdown files. Supports single document crawling and Wiki batch crawling, making knowledge management easier!

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/Zillzhou/DocHarvest/releases)
[![Python](https://img.shields.io/badge/python-3.9+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

English | [简体中文](README.md)

> **📌 Recommended Python Version**  
> Python 3.9-3.12 is recommended for best compatibility.

## ✨ Features

- 🎨 **Clean GUI**: Modern UI design based on PyQt5
- 🔐 **Secure Authentication**: Uses Feishu official OAuth 2.0 authentication
- 📥 **Smart Crawling**: Automatically parses Feishu document links and fetches complete content
- 📚 **Wiki Batch Crawling (NEW)**: Automatically crawls all sub-documents in an entire Wiki directory recursively
- 📝 **Markdown Export**: Converts document content to standard Markdown format
- 📁 **Preserve Directory Structure**: Maintains Wiki hierarchy when batch crawling
- 📊 **Real-time Progress**: Displays crawling progress and detailed logs
- 💾 **Auto Save**: Supports custom save paths
- 📋 **Logging**: Complete operation logs for easy debugging

## 🚀 Quick Start

### Method 1: Use Packaged exe File (Recommended)

1. Download the latest version from [Releases](https://github.com/Zillzhou/DocHarvest/releases)
2. Double-click to run `DocHarvest.exe`
3. Configure your Feishu app credentials (see "Getting Feishu API Credentials" below)
4. Enter document link and start crawling

### Method 2: Run from Source Code

#### 1. Requirements

- Python 3.9 or higher
- Windows / macOS / Linux

#### 2. Install Dependencies

```bash
cd DocHarvest

# Install using requirements.txt
pip install -r requirements.txt

# Or install manually
pip install PyQt5 requests
```

#### 3. Configure Application

Copy `config.json.example` to `config.json` and fill in your Feishu app credentials:

```bash
# Windows
copy config.json.example config.json

# Linux/Mac
cp config.json.example config.json
```

Edit `config.json`:

```json
{
  "app_id": "cli_xxxxxxxxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "default_save_path": ""
}
```

> ⚠️ **Note**: `config.json` contains sensitive information and is excluded by `.gitignore` from version control.

#### 4. Run the Program

```bash
python main.py
```

## 🔑 Getting Feishu API Credentials

### Step 1: Create Feishu Application

1. Visit [Feishu Open Platform](https://open.feishu.cn/) (or [Lark Open Platform](https://open.larksuite.com/))
2. Log in and go to "Developer Console"
3. Click "Create Enterprise Self-built App"
4. Fill in application name and description

### Step 2: Configure Permissions

In the application management page, add the following permissions:

- `docx:document:readonly` - View, comment and export documents
- `docs:read` - View documents

### Step 3: Get Credentials

On the "Credentials & Basic Info" page, obtain:
- **App ID**
- **App Secret**

### Step 4: Publish Application

1. In the application management page, click "Version Management & Release"
2. Create a version and publish to enterprise internal
3. Wait for administrator approval

### Step 5: Wiki Permissions (Required for Batch Crawling) 🆕

To use the **Wiki Batch Crawling** feature, you also need to add:

- `wiki:wiki:readonly` - View wiki

## 📖 Usage Guide

### Crawling Mode Selection 🆕

The program supports two crawling modes:

#### 1. Single Document Crawling
- Suitable for crawling a single Feishu document
- Supports links: `/docx/`, `/docs/`, etc.
- Fast, suitable for daily use

#### 2. Wiki Batch Crawling
- 🌟 **Auto Recursive**: Crawl all sub-documents in the entire Wiki directory at once
- 🌟 **Preserve Structure**: Save to folders according to Wiki hierarchy
- 🌟 **Batch Download**: No need to manually click each document
- Suitable for exporting entire knowledge bases

### Interface Guide

```
┌─────────────────────────────────────────┐
│  📄 Feishu Document Crawler             │
├─────────────────────────────────────────┤
│  ⚙️ Configuration                       │
│    App ID:     [________________]       │
│    App Secret: [****************]       │
├─────────────────────────────────────────┤
│  🔗 Document Link                       │
│    [Paste Feishu document share link...] │
├─────────────────────────────────────────┤
│  💾 Save Path                           │
│    [C:\Users\xxx\Desktop] [Browse...]   │
├─────────────────────────────────────────┤
│  [Progress: ▓▓▓▓▓░░░░░ 50%]            │
│  [🚀 Start Crawling]                    │
├─────────────────────────────────────────┤
│  📋 Run Log                             │
│    [10:30:25] 🚀 Initializing client...│
│    [10:30:26] 🔑 Getting access_token...│
│    ...                                  │
└─────────────────────────────────────────┘
```

### Operation Steps

1. **Fill Configuration**: Enter App ID and App Secret in the "Configuration" area
2. **Paste Link**: Paste the Feishu document share link in the "Document Link" input box
3. **Select Path**: Choose the save location for Markdown files (default is Desktop)
4. **Start Crawling**: Click the "Start Crawling" button
5. **View Logs**: Check real-time progress in the "Run Log" area
6. **Complete Export**: After crawling is complete, a prompt will appear and files are auto-saved

### Supported Link Formats

- `https://xxx.feishu.cn/docx/xxxxxx`
- `https://xxx.feishu.cn/docs/xxxxxx`
- `https://xxx.feishu.cn/wiki/xxxxxx`
- `https://xxx.larksuite.com/docx/xxxxxx`

## 🔧 Package to exe

### Windows

Use the provided batch file:

```bash
build.bat
```

Or package manually:

```bash
pyinstaller --clean build.spec
```

### Linux / macOS

```bash
chmod +x build.sh
./build.sh
```

The packaged files are located in the `dist` directory.

## 📁 Project Structure

```
DocHarvest/
├── main.py                    # Main program entry
├── gui.py                     # GUI interface module
├── feishu_api.py              # Feishu API handler module
├── wiki_crawler.py            # Wiki batch crawling module
├── markdown_converter.py      # Markdown conversion module
├── config.json.example        # Configuration file template
├── config.json                # Configuration file (local, not committed)
├── requirements.txt           # Dependency list
├── build.spec                 # PyInstaller configuration
├── build.bat                  # Windows packaging script
├── build.sh                   # Linux/Mac packaging script
├── install.bat                # Dependency installation script (Windows)
├── run.bat                    # Quick start script (Windows)
├── README.md                  # Project documentation
├── CHANGELOG.md               # Change log
├── LICENSE                    # License
├── logs/                      # Log directory (auto-created)
└── dist/                      # Packaging output directory
```

## 🐛 Common Issues

### 1. Failed to Get access_token

**Reason**: Incorrect App ID or App Secret

**Solution**:
- Check if configuration information is correct
- Confirm application is published and approved

### 2. Failed to Get Document Content

**Reason**:
- Insufficient document permissions
- Application permissions not configured
- Invalid document ID

**Solution**:
- Confirm application has document read permissions
- Check if document link is correct
- Confirm you have access to the document

### 3. Unable to Extract Document ID

**Reason**: Unsupported link format

**Solution**:
- Use the document's share link (not the browser address bar link)
- Confirm link is complete, including protocol (https://)

### 4. Program Won't Run After Packaging

**Reason**:
- Missing runtime dependencies
- Path issues

**Solution**:
- Ensure config.json is in the same directory as exe
- Try running from command line to view error messages

## 📝 Development Notes

### Tech Stack

- **GUI Framework**: PyQt5 5.15.9
- **HTTP Requests**: requests 2.31.0
- **Packaging Tool**: PyInstaller 6.3.0
- **Python Version**: 3.9+

### API Endpoints

Feishu Open Platform APIs used:

- **Get tenant_access_token**
  ```
  POST /open-apis/auth/v3/tenant_access_token/internal
  ```

- **Get Document Metadata**
  ```
  GET /open-apis/docx/v1/documents/{document_id}
  ```

- **Get Document Raw Content**
  ```
  GET /open-apis/docx/v1/documents/{document_id}/raw_content
  ```

### Log Location

Log files are generated in the `logs` directory during program execution:
- Filename format: `feishu_crawler_YYYYMMDD.log`
- Log level: INFO

## 🤝 Contributing

We welcome all forms of contributions!

- 🐛 [Report Bug](https://github.com/Zillzhou/DocHarvest/issues/new?template=bug_report.md)
- 💡 [Request Feature](https://github.com/Zillzhou/DocHarvest/issues/new?template=feature_request.md)
- 📖 Improve documentation
- 🔧 Submit code

See [Contributing Guide](CONTRIBUTING.md) for details

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

## ⭐ Star History

If this project helps you, please give it a Star! ⭐

## 🙏 Acknowledgments

- Thanks to Feishu Open Platform for API support
- Thanks to all contributors

---

**⚠️ Disclaimer**

1. This tool is for learning and personal use only
2. Please comply with the Feishu Open Platform terms of use
3. Do not abuse the API or make frequent requests
4. Keep your App Secret safe and do not leak it
5. Exported document content is for personal use only, please respect copyright

