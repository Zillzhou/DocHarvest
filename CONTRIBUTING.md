# 贡献指南

感谢你考虑为 DocHarvest 做出贡献！🎉

## 如何贡献

### 报告 Bug

如果你发现了 Bug，请创建一个 Issue 并包含以下信息：

- 详细的问题描述
- 重现步骤
- 预期行为和实际行为
- 你的环境信息（操作系统、Python版本等）
- 相关的日志输出（如果有）

### 提出新功能

如果你有新功能的想法：

1. 先检查 [Issues](https://github.com/yourusername/DocHarvest/issues) 和 [ROADMAP.md](ROADMAP.md) 看是否已经有类似的提议
2. 创建一个新的 Feature Request Issue
3. 清楚地描述这个功能以及它解决的问题
4. 如果可能，提供一些实现思路

### 提交代码

1. **Fork 项目**
   ```bash
   # 在 GitHub 上 Fork 这个仓库
   ```

2. **克隆你的 Fork**
   ```bash
   git clone https://github.com/your-username/DocHarvest.git
   cd DocHarvest
   ```

3. **创建新分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

4. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

5. **进行修改**
   - 遵循现有的代码风格
   - 添加必要的注释
   - 更新相关文档

6. **测试你的修改**
   ```bash
   python main.py
   ```

7. **提交修改**
   ```bash
   git add .
   git commit -m "feat: 添加某某功能"
   # 或
   git commit -m "fix: 修复某某问题"
   ```

   提交信息格式：
   - `feat:` 新功能
   - `fix:` Bug 修复
   - `docs:` 文档更新
   - `style:` 代码格式调整
   - `refactor:` 代码重构
   - `test:` 测试相关
   - `chore:` 构建/工具相关

8. **推送到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **创建 Pull Request**
   - 在 GitHub 上创建 Pull Request
   - 清楚地描述你的修改
   - 链接相关的 Issue（如果有）

## 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://pep8.org/) 规范
- 使用 4 个空格缩进
- 类名使用 PascalCase
- 函数名使用 snake_case
- 添加适当的文档字符串

### 示例

```python
class DocumentExporter:
    """文档导出器类"""
    
    def export_to_markdown(self, content: str, path: str) -> bool:
        """
        导出文档为 Markdown 格式
        
        Args:
            content: 文档内容
            path: 保存路径
            
        Returns:
            是否成功
        """
        try:
            # 实现代码
            return True
        except Exception as e:
            logging.error(f"导出失败: {e}")
            return False
```

## 项目结构

在修改代码前，建议阅读 [ARCHITECTURE.md](ARCHITECTURE.md) 了解项目架构。

## 开发环境设置

### 推荐的 IDE
- VS Code
- PyCharm

### VS Code 推荐插件
- Python
- Pylance
- Python Docstring Generator

## 测试

目前项目主要依靠手动测试。未来我们会添加自动化测试。

测试时请确保：
- [ ] GUI 界面正常显示
- [ ] 单文档爬取功能正常
- [ ] Wiki 批量爬取功能正常
- [ ] 配置保存和加载正常
- [ ] 不同格式的链接都能正常解析

## 文档

如果你的修改涉及到用户可见的功能变化：

- 更新 README.md
- 如果是新功能，考虑更新 ROADMAP.md
- 在 CHANGELOG.md 中记录变更

## 许可证

通过贡献代码，你同意你的贡献将按照 MIT 许可证发布。

## 问题？

如有任何问题，欢迎：
- 创建 Issue
- 发送邮件到开发者邮箱

---

再次感谢你的贡献！❤️

