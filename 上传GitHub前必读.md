# 🚨 上传 GitHub 前必读

## ✅ 已完成的修改

我已经帮你完成了以下所有修改：

### 1. 🔐 敏感信息保护（最重要！）
- ✅ 在 `.gitignore` 中添加了 `config.json`
- ✅ 创建了 `config.json.example` 作为配置模板
- ⚠️ **你的 `config.json` 仍包含真实密钥，已被 .gitignore 排除**

### 2. 📝 项目命名更新
- ✅ 项目名称：`crawlfeishu` → `DocHarvest`
- ✅ README 标题已更新
- ✅ GUI 窗口标题：`"飞书文档爬取工具"` → `"DocHarvest"`
- ✅ 打包文件名：`飞书文档爬取工具.exe` → `DocHarvest.exe`
- ✅ 所有文档中的项目名称已统一

### 3. 📚 GitHub 标准文件
新增以下文件：
- ✅ `CONTRIBUTING.md` - 贡献指南
- ✅ `ROADMAP.md` - 功能路线图
- ✅ `GITHUB_CHECKLIST.md` - 上传检查清单
- ✅ `.github/workflows/build.yml` - 自动构建工作流
- ✅ `.github/ISSUE_TEMPLATE/bug_report.md` - Bug 报告模板
- ✅ `.github/ISSUE_TEMPLATE/feature_request.md` - 功能请求模板

### 4. 📖 文档优化
- ✅ README.md 添加了 GitHub 徽章
- ✅ README.md 添加了贡献指南链接
- ✅ README.md 更新了配置说明（使用 config.json.example）
- ✅ ARCHITECTURE.md 项目名称已更新

---

## ⚠️ 上传前必须检查的事项

### 🔴 关键步骤（必须完成！）

#### 1. 验证敏感信息已被排除
```bash
# 在项目目录运行
cd g:\kaiyunworkhistory\DocHarvest

# 检查 .gitignore 是否包含 config.json
type .gitignore | findstr config.json

# 初始化 git 后，检查 config.json 是否被忽略
git init
git status

# 应该看不到 config.json 在待提交列表中
```

#### 2. 替换 GitHub 用户名
**全局搜索并替换**：`Zillzhou` → 你的实际 GitHub 用户名

需要修改的文件：
- `README.md`（多处）
- `CONTRIBUTING.md`
- `GITHUB_CHECKLIST.md`
- `ROADMAP.md`

#### 3. 添加项目截图（强烈推荐）
在 README.md 的"功能特性"后面添加：

```markdown
## 📸 界面预览

![主界面](screenshots/main.png)
![Wiki批量爬取](screenshots/wiki-crawl.png)
```

创建 `screenshots` 文件夹并添加截图。

---

## 🚀 上传步骤

### 方法一：使用 GitHub Desktop（推荐新手）
1. 下载安装 [GitHub Desktop](https://desktop.github.com/)
2. 打开 GitHub Desktop
3. File → Add Local Repository → 选择 `DocHarvest` 文件夹
4. 点击 "Publish repository"
5. 填写仓库信息，选择 Public 或 Private
6. 点击发布

### 方法二：使用命令行
```bash
# 1. 进入项目目录
cd g:\kaiyunworkhistory\DocHarvest

# 2. 初始化 Git（如果还没有）
git init

# 3. 添加所有文件
git add .

# 4. 检查要提交的文件（重要！）
git status
# ⚠️ 确认 config.json 没有在列表中！

# 5. 首次提交
git commit -m "Initial commit: DocHarvest v1.0.0"

# 6. 在 GitHub 上创建仓库（通过网页）
# https://github.com/new
# 仓库名：DocHarvest
# 描述：A powerful desktop application for exporting Feishu/Lark documents to Markdown
# 公开或私有：按需选择
# 不要勾选"Initialize with README"

# 7. 关联远程仓库（替换为你的用户名）
git remote add origin https://github.com/你的用户名/DocHarvest.git

# 8. 推送到 GitHub
git branch -M main
git push -u origin main
```

---

## 📋 完整文件清单

### 核心代码（5个）
```
✅ main.py                   - 程序入口
✅ gui.py                    - GUI 界面
✅ feishu_api.py             - API 封装
✅ wiki_crawler.py           - Wiki 爬取
✅ markdown_converter.py     - 格式转换
✅ __init__.py              - 包初始化
```

### 配置文件（3个）
```
✅ config.json.example       - 配置模板（会上传）
❌ config.json              - 真实配置（不会上传，在 .gitignore 中）
✅ requirements.txt          - Python 依赖
```

### 构建脚本（5个）
```
✅ build.spec               - PyInstaller 配置
✅ build.bat                - Windows 打包
✅ build.sh                 - Linux/Mac 打包
✅ install.bat              - 依赖安装
✅ run.bat                  - 快速启动
```

### 文档文件（8个）
```
✅ README.md                - 项目说明
✅ ARCHITECTURE.md          - 架构文档
✅ ROADMAP.md               - 功能路线图
✅ CONTRIBUTING.md          - 贡献指南
✅ CHANGELOG.md             - 更新日志
✅ LICENSE                  - MIT 许可证
✅ GITHUB_CHECKLIST.md      - 上传检查清单
✅ 上传GitHub前必读.md      - 本文件
```

### GitHub 配置（4个）
```
✅ .gitignore                           - Git 忽略配置
✅ .github/workflows/build.yml          - 自动构建
✅ .github/ISSUE_TEMPLATE/bug_report.md - Bug 模板
✅ .github/ISSUE_TEMPLATE/feature_request.md - 功能请求模板
```

### 运行时目录（不上传）
```
❌ __pycache__/             - Python 缓存
❌ logs/                    - 日志文件
❌ dist/                    - 打包输出（如果有）
❌ build/                   - 构建临时文件（如果有）
```

---

## 🎯 上传后的任务

### 1. 仓库设置
1. 进入仓库 Settings
2. 在 "About" 部分：
   - 添加描述：`A powerful desktop application for exporting Feishu/Lark documents to Markdown`
   - 添加网站（如果有）
   - 添加 Topics：`python`, `feishu`, `lark`, `markdown`, `pyqt5`, `document-export`, `wiki`

### 2. 启用功能
- ✅ Issues（默认开启）
- ✅ Discussions（可选，适合讨论功能）
- ✅ Wiki（可选，可以写详细教程）

### 3. 创建第一个 Release
1. 点击右侧 "Releases"
2. "Create a new release"
3. Tag: `v1.0.0`
4. Title: `DocHarvest v1.0.0 - Initial Release`
5. 描述版本内容
6. 如果有打包好的 exe，拖拽上传
7. "Publish release"

### 4. 添加徽章（可选）
在 README.md 顶部添加更多徽章：

```markdown
[![GitHub stars](https://img.shields.io/github/stars/你的用户名/DocHarvest?style=social)](https://github.com/你的用户名/DocHarvest/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/你的用户名/DocHarvest?style=social)](https://github.com/你的用户名/DocHarvest/network)
[![GitHub issues](https://img.shields.io/github/issues/你的用户名/DocHarvest)](https://github.com/你的用户名/DocHarvest/issues)
```

---

## ⚡ 快速检查命令

```bash
# 检查敏感信息
findstr /S /I "cli_a8626dbd59f2d00c" *.*
findstr /S /I "DaY17olIfUa0myenjz9YGwmW74OO3New" *.*

# 应该只在 config.json 中找到（该文件已被 .gitignore 排除）
```

---

## 🆘 常见问题

### Q: 不小心上传了敏感信息怎么办？
A: 
1. **立即**在飞书后台重新生成 App Secret
2. 删除 GitHub 仓库中的提交记录（需要使用 git filter-branch 或 BFG）
3. 或者直接删除仓库重新上传

### Q: .gitignore 不生效？
A: 
```bash
# 清除 Git 缓存
git rm -r --cached .
git add .
git commit -m "Update .gitignore"
```

### Q: 需要修改用户名的地方太多了？
A: 使用 VS Code 的全局替换功能：
1. Ctrl + Shift + H
2. 搜索：`Zillzhou`
3. 替换为：你的 GitHub 用户名
4. 点击 "Replace All"

---

## 📞 获取帮助

如果遇到问题：
1. 查看 [GITHUB_CHECKLIST.md](GITHUB_CHECKLIST.md) 详细步骤
2. 查看 GitHub 官方文档
3. 搜索相关错误信息

---

## ✨ 准备好了吗？

完成上述检查后：
- [ ] 已验证 config.json 被 .gitignore 排除
- [ ] 已替换所有 `Zillzhou` 为实际用户名
- [ ] 已添加项目截图（推荐）
- [ ] 已阅读上传步骤

**祝你的项目顺利上传，获得很多 Star！** ⭐⭐⭐

---

**最后更新**: 2024-10-17

