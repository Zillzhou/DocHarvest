# DocHarvest 📄

<div align="center">

**飞书文档批量导出工具**

一键导出飞书 Wiki 和文档至 Markdown、PDF、Word 格式

[![Python](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)](https://github.com/Zillzhou/DocHarvest)

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [使用说明](#-使用说明) • [开发文档](#-项目结构)

</div>

---

## ✨ 功能特性

### 核心功能
- 🎯 **单文档导出** - 支持飞书文档、表格、文稿
- 🌲 **Wiki 批量导出** - 递归导出整个 Wiki，保留目录结构
- 📦 **多格式支持** - Markdown、PDF、Word 任意组合导出
- ⚡ **异步高并发** - 基于 aiohttp 实现真正并发，支持 15+ 并行任务
- 🎨 **现代化 UI** - Apple Human Interface Guidelines 设计风格

### 性能优势
- ⏱️ **极速导出** - 100 篇文档约 60-90 秒完成
- 🔄 **智能重试** - 自动处理网络波动和 API 限流
- 💾 **自动保存** - 配置自动保存，无需重复输入
- 📊 **实时进度** - 清晰的进度显示和日志反馈

---

## 🚀 快速开始

### 方法一：直接运行（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/Zillzhou/DocHarvest.git
cd DocHarvest

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置凭证
cp config.json.example config.json
# 编辑 config.json，填入你的 App ID 和 App Secret

# 4. 启动程序
python src/main.py
# 或使用快捷脚本
run.bat  # Windows
```

### 方法二：打包为可执行文件

```bash
# Windows
cd scripts
build.bat

# Linux / macOS
cd scripts
chmod +x build.sh
./build.sh
```

打包后的可执行文件位于 `dist/` 目录。

---

## 🔑 获取飞书 API 凭证

### 步骤 1：创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 创建企业自建应用
3. 记录 **App ID** 和 **App Secret**

### 步骤 2：配置权限

在应用管理后台，添加以下权限：

| 权限 | 说明 | 必需性 |
|------|------|--------|
| `docx:document:readonly` | 读取文档内容 | ✅ 必需 |
| `docs:read` | 读取旧版文档 | ✅ 必需 |
| `wiki:wiki:readonly` | 访问 Wiki 空间 | ⭐ Wiki 导出必需 |
| `drive:export:readonly` | 导出 PDF/Word | ⭐ PDF/Word 导出必需 |

### 步骤 3：发布应用

1. 在应用管理后台点击 **版本管理与发布**
2. 创建版本并提交审核（企业内部应用无需审核）
3. 发布应用到企业内

### 步骤 4：配置文件

编辑 `config.json`：

```json
{
  "app_id": "cli_xxxxxxxxxxxxxx",
  "app_secret": "xxxxxxxxxxxxxxxxxxxxxx",
  "default_save_path": ""
}
```

---

## 📖 使用说明

### 界面说明

启动程序后，您将看到简洁的 Apple 风格界面：

1. **配置区域** - 填写 App ID、App Secret 和保存路径
2. **链接输入** - 粘贴飞书文档或 Wiki 链接
3. **格式选择** - 勾选需要导出的格式（Markdown/PDF/Word）
4. **导出按钮** - 点击开始导出
5. **进度显示** - 实时显示导出进度和状态

### 支持的链接格式

```
✅ Wiki 空间（推荐）
https://example.feishu.cn/wiki/xxxxx

✅ 单个文档
https://example.feishu.cn/docx/xxxxx

✅ 多维表格
https://example.feishu.cn/base/xxxxx

✅ 文稿（Doc）
https://example.feishu.cn/docs/xxxxx
```

### 导出模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **单文档导出** | 导出单个文档 | 快速导出单个文件 |
| **Wiki 批量导出** | 递归导出整个 Wiki 树 | 导出完整知识库 |

---

## 🔧 性能指标

### 实测数据

| 文档数量 | 导出时间 | 平均速度 | 并发数 |
|---------|----------|----------|--------|
| 50 篇   | 30-45 秒 | ~1 篇/秒 | 15 |
| 100 篇  | 60-90 秒 | ~1 篇/秒 | 15 |
| 200 篇  | 2-3 分钟 | ~1 篇/秒 | 15 |

*以上数据基于纯 PDF 导出模式，实际速度受网络环境影响*

### 性能优化建议

1. **网络环境** - 使用稳定的网络连接
2. **导出格式** - 优先选择 PDF 或 Markdown（速度快于 Word）
3. **并发数** - 默认 15 个并发，可在代码中调整
4. **目标目录** - 使用 SSD 存储提升写入速度

---

## 📁 项目结构

```
DocHarvest/
├── src/                          # 源代码目录
│   ├── main.py                   # 程序入口
│   ├── apple_gui.py              # Apple HIG 风格 GUI
│   ├── feishu_api.py             # 飞书 API 封装
│   ├── async_exporter.py         # 异步导出器（高并发）
│   ├── feishu_native_exporter.py # 原生 PDF/Word 导出
│   ├── wiki_crawler.py           # Wiki 爬虫（递归）
│   ├── parallel_crawler.py       # 并行爬虫控制器
│   ├── document_converter.py     # Markdown 转换器
│   ├── markdown_converter.py     # Markdown 处理
│   └── workers.py                # 后台工作线程
├── scripts/                      # 构建脚本
│   ├── build.bat                 # Windows 打包脚本
│   ├── build.sh                  # Linux/macOS 打包脚本
│   ├── build.spec                # PyInstaller 配置
│   ├── install.bat               # 依赖安装（Windows）
│   └── run.bat                   # 快速启动（Windows）
├── logs/                         # 日志目录（自动生成）
├── config.json.example           # 配置文件模板
├── requirements.txt              # Python 依赖
├── run.bat                       # 快速启动脚本
├── README.md                     # 本文档
└── LICENSE                       # MIT 许可证
```

### 核心模块说明

| 模块 | 功能 |
|------|------|
| `apple_gui.py` | PyQt5 界面，实现 Apple HIG 设计规范 |
| `async_exporter.py` | 基于 aiohttp 的异步导出器，支持高并发 |
| `wiki_crawler.py` | 递归爬取 Wiki 树形结构 |
| `parallel_crawler.py` | 并行任务调度和进度管理 |
| `feishu_native_exporter.py` | 调用飞书官方 API 导出 PDF/Word |

---

## 🐛 常见问题

### 1. 获取 access_token 失败

**原因**: App ID 或 App Secret 错误

**解决**: 
- 检查 `config.json` 中的凭证是否正确
- 确认应用已发布并启用

### 2. 导出 PDF/Word 失败

**原因**: 缺少 `drive:export:readonly` 权限

**解决**: 
- 在飞书开放平台添加该权限
- 重新发布应用

### 3. Wiki 导出失败

**原因**: 缺少 `wiki:wiki:readonly` 权限

**解决**: 
- 添加 Wiki 相关权限
- 确保应用有访问目标 Wiki 的权限

### 4. 程序启动报错

**原因**: 缺少 Python 依赖

**解决**:
```bash
pip install -r requirements.txt
```

---

## 💻 技术栈

- **GUI 框架**: PyQt5
- **异步 I/O**: aiohttp, asyncio
- **HTTP 客户端**: requests
- **打包工具**: PyInstaller
- **设计规范**: Apple Human Interface Guidelines

---

## 📝 开发说明

### 本地开发

```bash
# 克隆项目
git clone https://github.com/Zillzhou/DocHarvest.git
cd DocHarvest

# 安装开发依赖
pip install -r requirements.txt

# 运行程序
python src/main.py
```

### 日志位置

- **运行日志**: `logs/feishu_crawler_YYYYMMDD.log`
- **错误日志**: 同上，ERROR 级别
- **控制台输出**: 实时显示关键信息

### 飞书 API 文档

- [官方文档](https://open.feishu.cn/document)
- [认证指南](https://open.feishu.cn/document/ukTMukTMukTM/uMTNz4yM1MjLzUzM)
- [文档 API](https://open.feishu.cn/document/ukTMukTMukTM/uYDM2YjL2AjN24iNwYjN)

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

本项目基于 [MIT License](LICENSE) 开源。

---

## 🙏 致谢

感谢 [飞书开放平台](https://open.feishu.cn/) 提供强大的 API 支持。

---

<div align="center">

**⭐ 如果这个项目对你有帮助，请给个 Star！**

Made with ❤️ by [Zillzhou](https://github.com/Zillzhou)

</div>
