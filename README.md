# DocHarvest 📄

> 🚀 A powerful desktop application for exporting Feishu/Lark documents to Markdown

一个基于 Python + PyQt5 的桌面应用程序，用于从飞书分享链接中获取文档内容并导出为 Markdown 文件。支持单文档爬取和 Wiki 批量爬取，让知识管理更轻松！

[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/yourusername/DocHarvest/releases)
[![Python](https://img.shields.io/badge/python-3.9+-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[English](README_EN.md) | 简体中文

> **📌 推荐 Python 版本**  
> 推荐使用 Python 3.9-3.12 以获得最佳兼容性。

## ✨ 功能特性

- 🎨 **简洁的图形界面**：基于 PyQt5 开发，现代化 UI 设计
- 🔐 **安全认证**：使用飞书官方 OAuth 2.0 认证
- 📥 **智能爬取**：自动解析飞书文档链接，获取完整内容
- 📚 **Wiki批量爬取（NEW）**：自动递归获取整个Wiki目录下的所有子文档
- 📝 **Markdown 导出**：将文档内容转换为标准 Markdown 格式
- 📁 **目录结构保留**：批量爬取时保留Wiki的层级结构
- 📊 **实时进度**：显示爬取进度和详细日志
- 💾 **自动保存**：支持自定义保存路径
- 📋 **日志记录**：完整的操作日志，方便调试

## 🚀 快速开始

### 方法一：使用打包好的 exe 文件（推荐）

1. 从 [Releases](https://github.com/yourusername/DocHarvest/releases) 下载最新版本
2. 双击运行 `DocHarvest.exe`
3. 配置你的飞书应用信息（见下方"获取飞书 API 凭证"）
4. 输入文档链接，开始爬取

### 方法二：从源码运行

#### 1. 环境要求

- Python 3.9 或更高版本
- Windows / macOS / Linux

#### 2. 安装依赖

```bash
cd DocHarvest

# 使用 requirements.txt 安装
pip install -r requirements.txt

# 或者手动安装
pip install PyQt5 requests
```

#### 3. 配置应用

复制 `config.json.example` 为 `config.json`，然后填入你的飞书应用凭证：

```bash
# Windows
copy config.json.example config.json

# Linux/Mac
cp config.json.example config.json
```

编辑 `config.json`：

```json
{
  "app_id": "cli_xxxxxxxxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  "default_save_path": ""
}
```

> ⚠️ **注意**: `config.json` 包含敏感信息，已被 `.gitignore` 排除，不会被提交到版本控制。

#### 4. 运行程序

```bash
python main.py
```

## 🔑 获取飞书 API 凭证

### 步骤 1：创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 登录并进入"开发者后台"
3. 点击"创建企业自建应用"
4. 填写应用名称和描述

### 步骤 2：配置权限

在应用管理页面，添加以下权限：

- `docx:document:readonly` - 查看、评论和导出文档
- `docs:read` - 查看文档

### 步骤 3：获取凭证

在"凭证与基础信息"页面，获取：
- **App ID**
- **App Secret**

### 步骤 4：发布应用

1. 在应用管理页面，点击"版本管理与发布"
2. 创建版本并发布到企业内部
3. 等待管理员审核通过

### 步骤 5：Wiki权限（批量爬取需要）🆕

如果要使用**Wiki批量爬取**功能，还需要添加：

- `wiki:wiki:readonly` - 查看知识库

## 📖 使用说明

### 爬取模式选择🆕

程序支持两种爬取模式：

#### 1. 单文档爬取
- 适用于爬取单个飞书文档
- 支持链接：`/docx/`、`/docs/` 等
- 快速，适合日常使用

#### 2. Wiki批量爬取 
- 🌟 **自动递归**：一次性爬取整个Wiki目录下的所有子文档
- 🌟 **保留结构**：按照Wiki的层级关系保存到文件夹
- 🌟 **批量下载**：无需手动点击每个文档
- 适合导出整个知识库

### 界面说明

```
┌─────────────────────────────────────────┐
│  📄 飞书文档爬取工具                     │
├─────────────────────────────────────────┤
│  ⚙️ 配置信息                            │
│    App ID:     [________________]       │
│    App Secret: [****************]       │
├─────────────────────────────────────────┤
│  🔗 文档链接                            │
│    [请粘贴飞书文档分享链接...]          │
├─────────────────────────────────────────┤
│  💾 保存路径                            │
│    [C:\Users\xxx\Desktop] [浏览...]     │
├─────────────────────────────────────────┤
│  [进度条: ▓▓▓▓▓░░░░░ 50%]              │
│  [🚀 开始爬取]                          │
├─────────────────────────────────────────┤
│  📋 运行日志                            │
│    [10:30:25] 🚀 初始化飞书API客户端... │
│    [10:30:26] 🔑 正在获取access_token...│
│    ...                                  │
└─────────────────────────────────────────┘
```

### 操作步骤

1. **填写配置**：在"配置信息"区域输入 App ID 和 App Secret
2. **粘贴链接**：在"文档链接"输入框中粘贴飞书文档的分享链接
3. **选择路径**：选择 Markdown 文件的保存位置（默认桌面）
4. **开始爬取**：点击"开始爬取"按钮
5. **查看日志**：在"运行日志"区域查看实时进度
6. **完成导出**：爬取完成后会弹出提示，文件自动保存

### 支持的链接格式

- `https://xxx.feishu.cn/docx/xxxxxx`
- `https://xxx.feishu.cn/docs/xxxxxx`
- `https://xxx.feishu.cn/wiki/xxxxxx`
- `https://xxx.larksuite.com/docx/xxxxxx`

## 🔧 打包成 exe

### Windows

使用提供的批处理文件：

```bash
build.bat
```

或手动打包：

```bash
pyinstaller --clean build.spec
```

### Linux / macOS

```bash
chmod +x build.sh
./build.sh
```

打包后的文件位于 `dist` 目录。

## 📁 项目结构

```
DocHarvest/
├── main.py                    # 主程序入口
├── gui.py                     # GUI界面模块
├── feishu_api.py              # 飞书API处理模块
├── wiki_crawler.py            # Wiki批量爬取模块
├── markdown_converter.py      # Markdown转换模块
├── config.json.example        # 配置文件模板
├── config.json                # 配置文件（本地，不提交）
├── requirements.txt           # 依赖清单
├── build.spec                 # PyInstaller配置
├── build.bat                  # Windows打包脚本
├── build.sh                   # Linux/Mac打包脚本
├── install.bat                # 依赖安装脚本（Windows）
├── run.bat                    # 快速启动脚本（Windows）
├── README.md                  # 项目文档
├── CHANGELOG.md               # 更新日志
├── LICENSE                    # 许可证
├── logs/                      # 日志目录（自动创建）
└── dist/                      # 打包输出目录
```

## 🐛 常见问题

### 1. 获取 access_token 失败

**原因**：App ID 或 App Secret 错误

**解决**：
- 检查配置信息是否正确
- 确认应用已发布并审核通过

### 2. 获取文档内容失败

**原因**：
- 文档权限不足
- 应用权限未配置
- 文档 ID 无效

**解决**：
- 确认应用有文档读取权限
- 检查文档链接是否正确
- 确认你有该文档的访问权限

### 3. 无法提取文档 ID

**原因**：链接格式不支持

**解决**：
- 使用文档的分享链接（不是浏览器地址栏的链接）
- 确认链接完整，包含协议（https://）

### 4. 打包后程序无法运行

**原因**：
- 缺少运行时依赖
- 路径问题

**解决**：
- 确保 config.json 在 exe 同目录
- 尝试在命令行运行，查看错误信息

## 📝 开发说明

### 技术栈

- **GUI 框架**：PyQt5 5.15.9
- **HTTP 请求**：requests 2.31.0
- **打包工具**：PyInstaller 6.3.0
- **Python 版本**：3.9+

### API 接口

使用的飞书开放平台 API：

- **获取 tenant_access_token**
  ```
  POST /open-apis/auth/v3/tenant_access_token/internal
  ```

- **获取文档元数据**
  ```
  GET /open-apis/docx/v1/documents/{document_id}
  ```

- **获取文档原始内容**
  ```
  GET /open-apis/docx/v1/documents/{document_id}/raw_content
  ```

### 日志位置

程序运行时会在 `logs` 目录生成日志文件：
- 文件名格式：`feishu_crawler_YYYYMMDD.log`
- 日志级别：INFO

## 🤝 贡献

我们欢迎所有形式的贡献！

- 🐛 [报告 Bug](https://github.com/yourusername/DocHarvest/issues/new?template=bug_report.md)
- 💡 [提出新功能](https://github.com/yourusername/DocHarvest/issues/new?template=feature_request.md)
- 📖 改进文档
- 🔧 提交代码

详见 [贡献指南](CONTRIBUTING.md)

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## ⭐ Star History

如果这个项目对你有帮助，请给它一个 Star！⭐

## 🙏 致谢

- 感谢飞书开放平台提供的 API 支持
- 感谢所有贡献者的付出

---

**⚠️ 注意事项**

1. 本工具仅供学习和个人使用
2. 请遵守飞书开放平台的使用条款
3. 不要滥用 API，避免频繁请求
4. 妥善保管你的 App Secret，不要泄露
5. 导出的文档内容仅供个人使用，请尊重版权

