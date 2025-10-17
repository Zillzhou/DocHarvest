# 📋 GitHub 上传前检查清单

在将 DocHarvest 上传到 GitHub 之前，请确保完成以下步骤：

## ✅ 必须完成的项目

### 1. 敏感信息检查
- [x] `config.json` 已添加到 `.gitignore`
- [x] 创建了 `config.json.example` 作为模板
- [ ] 确认 `config.json` 中没有真实的 API 密钥
- [ ] 检查所有代码文件中没有硬编码的敏感信息

### 2. 项目命名
- [x] 文件夹已重命名为 `DocHarvest`
- [x] README.md 标题已更新
- [x] GUI 窗口标题已更新
- [x] build.spec 中的 exe 名称已更新
- [x] 所有文档中的项目名称已更新

### 3. 文档完整性
- [x] README.md 包含完整的使用说明
- [x] CONTRIBUTING.md 贡献指南已创建
- [x] LICENSE 文件存在且正确
- [x] CHANGELOG.md 记录版本历史
- [x] ARCHITECTURE.md 项目架构说明
- [ ] 添加 ROADMAP.md（可选，已创建但需检查）

### 4. GitHub 特定文件
- [x] `.gitignore` 配置正确
- [x] GitHub Actions 工作流已创建
- [x] Issue 模板已创建
- [ ] Pull Request 模板已创建（可选）

### 5. 代码质量
- [ ] 所有代码已测试
- [ ] 移除了调试代码和 print 语句
- [ ] 代码符合 PEP 8 规范
- [ ] 添加了必要的注释

## 📝 推荐完成的项目

### 6. README 优化
- [x] 添加了项目徽章（badges）
- [ ] 添加了演示截图或 GIF
- [ ] 更新了 GitHub 仓库链接（将 `Zillzhou` 替换为实际用户名）
- [ ] 如果需要，创建英文版 README_EN.md

### 7. 额外文件
- [ ] 添加项目 Logo/图标
- [ ] 创建 .editorconfig（统一代码风格）
- [ ] 添加 CODE_OF_CONDUCT.md（行为准则）

## 🚀 上传步骤

### 1. 初始化 Git 仓库
```bash
cd DocHarvest
git init
```

### 2. 添加所有文件
```bash
git add .
```

### 3. 检查要提交的文件
```bash
git status
```
**重要**: 确认 `config.json` 没有出现在列表中！

### 4. 首次提交
```bash
git commit -m "Initial commit: DocHarvest v1.0.0"
```

### 5. 在 GitHub 创建仓库
1. 访问 https://github.com/new
2. 仓库名: `DocHarvest`
3. 描述: `A powerful desktop application for exporting Feishu/Lark documents to Markdown`
4. 选择 Public（公开）或 Private（私有）
5. **不要**勾选 "Initialize with README"（我们已经有了）
6. 点击 "Create repository"

### 6. 关联远程仓库并推送
```bash
# 替换为你的 GitHub 用户名
git remote add origin https://github.com/Zillzhou/DocHarvest.git

# 推送到 GitHub
git branch -M main
git push -u origin main
```

### 7. 创建第一个 Release（可选）
1. 在 GitHub 仓库页面，点击 "Releases"
2. 点击 "Create a new release"
3. Tag version: `v1.0.0`
4. Release title: `DocHarvest v1.0.0 - Initial Release`
5. 描述发布内容
6. 如果有打包好的 exe，上传到 Assets
7. 点击 "Publish release"

## ⚠️ 特别提醒

### 敏感信息二次检查
在推送前，务必再次检查：

```bash
# 查看即将提交的文件内容
git diff --cached

# 搜索可能的敏感信息
grep -r "cli_a8626dbd59f2d00c" .
grep -r "DaY17olIfUa0myenjz9YGwmW74OO3New" .
```

如果发现敏感信息：
```bash
# 从暂存区移除
git reset HEAD config.json

# 确认 .gitignore 包含 config.json
cat .gitignore | grep config.json
```

### 如果不小心推送了敏感信息
```bash
# 1. 立即修改密钥！（在飞书后台重新生成）
# 2. 从历史记录中移除（需要 BFG Repo-Cleaner 或 git filter-branch）
# 3. 强制推送（谨慎！）
```

## 📋 需要更新的占位符

上传前，全局搜索并替换以下占位符：

- [ ] `Zillzhou` → 你的 GitHub 用户名
- [ ] `your_app_id_here` → 保持不变（这是给用户的占位符）
- [ ] `your_app_secret_here` → 保持不变（这是给用户的占位符）

## 🎯 上传后的任务

### 仓库设置
- [ ] 在 Settings → About 添加项目描述和标签
- [ ] 添加 Topics: `python`, `feishu`, `lark`, `markdown`, `pyqt5`, `document-export`
- [ ] 如果需要，启用 Issues 和 Discussions
- [ ] 设置分支保护规则（可选）

### 社区推广
- [ ] 在 README 添加实际的演示截图
- [ ] 考虑写一篇使用教程文章
- [ ] 在相关社区分享（知乎、V2EX、掘金等）

## ✨ 完成！

完成上述步骤后，你的项目就可以成功上传到 GitHub 了！

记住：
- 🔒 永远不要提交包含敏感信息的文件
- 📖 保持 README 和文档更新
- 🐛 及时回复 Issues 和 Pull Requests
- ⭐ 鼓励用户给项目加星

---

**祝你的项目获得很多 Star！** 🌟

