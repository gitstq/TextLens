<p align="center">
  <strong>TextLens</strong> — 轻量级文本分析与可视化 CLI 工具
</p>

<p align="center">
  <a href="https://github.com/gitstq/TextLens"><img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="Version"></a>
  <a href="https://github.com/gitstq/TextLens"><img src="https://img.shields.io/badge/python-3.8%2B-green.svg" alt="Python"></a>
  <a href="https://github.com/gitstq/TextLens"><img src="https://img.shields.io/badge/license-MIT-orange.svg" alt="License"></a>
  <a href="https://github.com/gitstq/TextLens"><img src="https://img.shields.io/badge/dependencies-0-success.svg" alt="Zero Dependencies"></a>
  <a href="https://github.com/gitstq/TextLens"><img src="https://img.shields.io/badge/tests-96%20passed-brightgreen.svg" alt="Tests"></a>
</p>

<p align="center">
  <a href="#简体中文">简体中文</a> | <a href="#繁體中文">繁體中文</a> | <a href="#english">English</a>
</p>

---

<a id="简体中文"></a>

# 🎉 项目介绍

**TextLens** 是一款轻量级的文本分析与可视化命令行工具，旨在为开发者、写作者和数据分析师提供**即时、直观、零门槛**的文本洞察能力。

### 解决什么问题？

在日常开发与写作中，我们经常需要快速了解一段文本的特征——情感倾向如何、可读性怎样、词频分布如何、是否存在被动语态……然而，现有的文本分析工具往往存在以下痛点：

- **依赖沉重**：需要安装 NLTK、spaCy 等大型 NLP 库，动辄数百 MB
- **配置繁琐**：需要下载语言模型、词典等额外资源
- **功能分散**：情感分析、可读性评估、词频统计分散在不同工具中
- **可视化缺失**：分析结果只有枯燥的数字，缺乏直观的终端可视化

### TextLens 的不同之处

- **零外部依赖**：纯 Python 标准库实现，`pip install` 即用，无需下载任何模型或数据文件
- **功能全面**：情感分析、可读性评估、文本统计、词频分析、模式检测，一站式搞定
- **终端可视化**：内置丰富的终端图表（柱状图、仪表盘、迷你折线图等），让数据一目了然
- **灵活输出**：支持 Dashboard、纯文本、JSON、Markdown、CSV 等多种输出格式
- **管道友好**：支持文件处理、stdin 输入、目录批量处理，轻松融入工作流

---

# ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🎭 **情感分析** | 正面/负面/中性分类，附带置信度评分，支持否定词与程度副词处理 |
| 📊 **可读性分析** | Flesch Reading Ease、Gunning Fog Index、Coleman-Liau Index，自动评估年级水平 |
| 📈 **文本统计** | 字数、句数、字符数、段落数、阅读时长、词汇多样性（TTR） |
| 🔤 **词频分析** | Top N 高频词、N-gram 分析、停用词过滤 |
| 🔍 **模式检测** | 疑问/感叹句计数、被动语态检测、句子复杂度分析 |
| 🖥️ **终端可视化** | 柱状图、水平条形图、进度条、仪表盘、迷你折线图、完整 Dashboard |
| 📋 **多格式输出** | Dashboard、纯文本、JSON、Markdown、CSV |
| 🔗 **管道处理** | 文件处理、stdin 支持、目录批量处理 |

---

# 🚀 快速开始

## 环境要求

- **Python** 3.8 及以上版本
- **零**外部依赖（纯标准库）

## 安装

```bash
# 从 PyPI 安装（推荐）
pip install textlens

# 或从源码安装
git clone https://github.com/gitstq/TextLens.git
cd TextLens
pip install .
```

## 基本使用

```bash
# 直接分析文本
textlens "TextLens 让文本分析变得简单高效！"

# 分析文件
textlens -f document.txt

# 快速情感分析
textlens -m sentiment "I love this product!"

# 完整 Dashboard 可视化
textlens -f report.txt --format dashboard
```

## Python API 快速体验

```python
from textpulse.analyzer import TextLensEngine

engine = TextLensEngine()

# 一键获取完整分析结果
result = engine.analyze("TextLens 让文本分析变得简单高效！")
print(engine.quick_summary(result))
```

---

# 📖 详细使用指南

## CLI 完整选项

```bash
# 分析模式
textlens -m sentiment "文本"        # 仅情感分析
textlens -m readability "文本"      # 仅可读性分析
textlens -m stats "文本"            # 仅文本统计
textlens -m frequency "文本"        # 仅词频分析
textlens -m pattern "文本"          # 仅模式检测
textlens -m compare -f a.txt -f b.txt  # 对比分析

# 输出格式
textlens -f doc.txt --format json       # JSON 输出
textlens -f doc.txt --format markdown   # Markdown 输出
textlens -f doc.txt --format csv        # CSV 输出
textlens -f doc.txt --format dashboard  # Dashboard 可视化
textlens -f doc.txt --format text       # 纯文本输出

# 输入方式
textlens -f document.txt               # 分析文件
cat article.txt | textlens --stdin     # 从 stdin 读取
textlens --dir ./docs --ext .txt,.md   # 批量处理目录

# 组合使用
textlens -m readability -f essay.txt --format json
textlens -m sentiment -f review.txt --format dashboard
```

## Python API 详解

```python
from textpulse.analyzer import TextLensEngine, SentimentAnalyzer
from textpulse.visualizer import TextLensDashboard

# ===== 完整分析 =====
engine = TextLensEngine()
result = engine.analyze("要分析的文本内容...")
print(TextLensDashboard.render_dashboard(result))

# ===== 快速摘要 =====
print(engine.quick_summary("要分析的文本内容..."))

# ===== 情感分析 =====
analyzer = SentimentAnalyzer()
sentiment = analyzer.analyze("I love this amazing product!")
print(f"得分: {sentiment.score}, 标签: {sentiment.label}")

# ===== 可读性分析 =====
result = engine.analyze("一段用于测试可读性的文本...")
print(f"Flesch 指数: {result.readability.flesch_score}")
print(f"年级水平: {result.readability.grade_level}")
```

## 分析模式说明

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `sentiment` | 情感分析 | 用户评论、反馈、社交媒体文本 |
| `readability` | 可读性分析 | 文章、论文、技术文档 |
| `stats` | 文本统计 | 快速了解文本基本特征 |
| `frequency` | 词频分析 | SEO 优化、关键词提取 |
| `pattern` | 模式检测 | 写作风格分析、文本质量检查 |
| `compare` | 对比分析 | A/B 测试、版本对比 |

---

# 💡 设计思路与迭代规划

## 为什么选择纯 Python？

1. **零摩擦安装**：`pip install textlens` 一条命令搞定，无需下载 GB 级别的模型文件
2. **跨平台兼容**：不依赖 C 扩展或系统库，在任何 Python 环境中都能运行
3. **安全可控**：不引入第三方代码，适合对安全性有要求的环境
4. **轻量快速**：启动时间极短，适合在管道和脚本中高频调用

## 设计决策

- **CLI 优先**：命令行是开发者的自然工作环境，所有功能均可通过 CLI 访问
- **结构化输出**：支持 JSON/CSV 输出，方便与其他工具和脚本集成
- **渐进式分析**：支持单模块分析和全量分析，按需获取信息

## 未来规划

- [ ] 多语言支持（中文情感分析、中文可读性指标）
- [ ] HTML 报告生成
- [ ] 配置文件支持（自定义停用词、分析参数）
- [ ] 插件系统（可扩展的分析模块）
- [ ] 交互式 REPL 模式

---

# 📦 安装与部署

## pip 安装（推荐）

```bash
pip install textlens
```

## 从源码安装

```bash
git clone https://github.com/gitstq/TextLens.git
cd TextLens
pip install .
```

## 开发环境搭建

```bash
git clone https://github.com/gitstq/TextLens.git
cd TextLens

# 安装（开发模式）
pip install -e .

# 运行测试
python -m pytest textpulse/tests/

# 或直接运行
python -m textpulse.tests.test_all
```

## 系统要求

| 项目 | 最低要求 |
|------|----------|
| Python | 3.8+ |
| 操作系统 | Windows / macOS / Linux |
| 外部依赖 | 无 |

---

# 🤝 贡献指南

我们欢迎任何形式的贡献！无论是提交 Bug、改进文档，还是添加新功能。

## 贡献流程

1. **Fork** 本仓库
2. 创建特性分支：`git checkout -b feature/your-feature`
3. 提交更改：`git commit -m "feat: add your feature"`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 **Pull Request**

## Commit 规范

我们采用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
feat: 新功能
fix: 修复 Bug
docs: 文档更新
style: 代码格式调整
refactor: 重构
test: 测试相关
chore: 构建/工具链相关
```

## 代码规范

- 遵循 PEP 8 编码规范
- 所有新功能必须附带单元测试
- 保持零外部依赖的原则

---

# 📄 开源协议

本项目基于 [MIT License](LICENSE) 开源。

```
MIT License

Copyright (c) 2024 gitstq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<a id="繁體中文"></a>

# 🎉 專案介紹

**TextLens** 是一款輕量級的文字分析與視覺化命令列工具，旨在為開發者、寫作者和資料分析師提供**即時、直觀、零門檻**的文字洞察能力。

### 解決什麼問題？

在日常開發與寫作中，我們經常需要快速瞭解一段文字的特徵——情感傾向如何、可讀性怎樣、詞頻分佈如何、是否存在被動語態……然而，現有的文字分析工具往往存在以下痛點：

- **依賴沉重**：需要安裝 NLTK、spaCy 等大型 NLP 函式庫，動輒數百 MB
- **配置繁瑣**：需要下載語言模型、詞典等額外資源
- **功能分散**：情感分析、可讀性評估、詞頻統計分散在不同工具中
- **視覺化缺失**：分析結果只有枯燥的數字，缺乏直觀的終端視覺化

### TextLens 的不同之處

- **零外部依賴**：純 Python 標準函式庫實作，`pip install` 即用，無需下載任何模型或資料檔案
- **功能全面**：情感分析、可讀性評估、文字統計、詞頻分析、模式偵測，一站式搞定
- **終端視覺化**：內建豐富的終端圖表（柱狀圖、儀表板、迷你折線圖等），讓資料一目瞭然
- **靈活輸出**：支援 Dashboard、純文字、JSON、Markdown、CSV 等多種輸出格式
- **管道友善**：支援檔案處理、stdin 輸入、目錄批次處理，輕鬆融入工作流程

---

# ✨ 核心特性

| 特性 | 說明 |
|------|------|
| 🎭 **情感分析** | 正面/負面/中性分類，附帶置信度評分，支援否定詞與程度副詞處理 |
| 📊 **可讀性分析** | Flesch Reading Ease、Gunning Fog Index、Coleman-Liau Index，自動評估年級水準 |
| 📈 **文字統計** | 字數、句數、字元數、段落數、閱讀時長、詞彙多樣性（TTR） |
| 🔤 **詞頻分析** | Top N 高頻詞、N-gram 分析、停用詞過濾 |
| 🔍 **模式偵測** | 疑問/感嘆句計數、被動語態偵測、句子複雜度分析 |
| 🖥️ **終端視覺化** | 柱狀圖、水平條形圖、進度條、儀表板、迷你折線圖、完整 Dashboard |
| 📋 **多格式輸出** | Dashboard、純文字、JSON、Markdown、CSV |
| 🔗 **管道處理** | 檔案處理、stdin 支援、目錄批次處理 |

---

# 🚀 快速開始

## 環境要求

- **Python** 3.8 及以上版本
- **零**外部依賴（純標準函式庫）

## 安裝

```bash
# 從 PyPI 安裝（推薦）
pip install textlens

# 或從原始碼安裝
git clone https://github.com/gitstq/TextLens.git
cd TextLens
pip install .
```

## 基本使用

```bash
# 直接分析文字
textlens "TextLens 讓文字分析變得簡單高效！"

# 分析檔案
textlens -f document.txt

# 快速情感分析
textlens -m sentiment "I love this product!"

# 完整 Dashboard 視覺化
textlens -f report.txt --format dashboard
```

## Python API 快速體驗

```python
from textpulse.analyzer import TextLensEngine

engine = TextLensEngine()

# 一鍵取得完整分析結果
result = engine.analyze("TextLens 讓文字分析變得簡單高效！")
print(engine.quick_summary(result))
```

---

# 📖 詳細使用指南

## CLI 完整選項

```bash
# 分析模式
textlens -m sentiment "文字"        # 僅情感分析
textlens -m readability "文字"      # 僅可讀性分析
textlens -m stats "文字"            # 僅文字統計
textlens -m frequency "文字"        # 僅詞頻分析
textlens -m pattern "文字"          # 僅模式偵測
textlens -m compare -f a.txt -f b.txt  # 對比分析

# 輸出格式
textlens -f doc.txt --format json       # JSON 輸出
textlens -f doc.txt --format markdown   # Markdown 輸出
textlens -f doc.txt --format csv        # CSV 輸出
textlens -f doc.txt --format dashboard  # Dashboard 視覺化
textlens -f doc.txt --format text       # 純文字輸出

# 輸入方式
textlens -f document.txt               # 分析檔案
cat article.txt | textlens --stdin     # 從 stdin 讀取
textlens --dir ./docs --ext .txt,.md   # 批次處理目錄

# 組合使用
textlens -m readability -f essay.txt --format json
textlens -m sentiment -f review.txt --format dashboard
```

## Python API 詳解

```python
from textpulse.analyzer import TextLensEngine, SentimentAnalyzer
from textpulse.visualizer import TextLensDashboard

# ===== 完整分析 =====
engine = TextLensEngine()
result = engine.analyze("要分析的文字內容...")
print(TextLensDashboard.render_dashboard(result))

# ===== 快速摘要 =====
print(engine.quick_summary("要分析的文字內容..."))

# ===== 情感分析 =====
analyzer = SentimentAnalyzer()
sentiment = analyzer.analyze("I love this amazing product!")
print(f"得分: {sentiment.score}, 標籤: {sentiment.label}")

# ===== 可讀性分析 =====
result = engine.analyze("一段用於測試可讀性的文字...")
print(f"Flesch 指數: {result.readability.flesch_score}")
print(f"年級水準: {result.readability.grade_level}")
```

## 分析模式說明

| 模式 | 說明 | 適用場景 |
|------|------|----------|
| `sentiment` | 情感分析 | 使用者評論、回饋、社群媒體文字 |
| `readability` | 可讀性分析 | 文章、論文、技術文件 |
| `stats` | 文字統計 | 快速瞭解文字基本特徵 |
| `frequency` | 詞頻分析 | SEO 最佳化、關鍵字提取 |
| `pattern` | 模式偵測 | 寫作風格分析、文字品質檢查 |
| `compare` | 對比分析 | A/B 測試、版本對比 |

---

# 💡 設計思路與迭代規劃

## 為什麼選擇純 Python？

1. **零摩擦安裝**：`pip install textlens` 一條命令搞定，無需下載 GB 級別的模型檔案
2. **跨平台相容**：不依賴 C 擴充或系統函式庫，在任何 Python 環境中都能執行
3. **安全可控**：不引入第三方程式碼，適合對安全性有要求的環境
4. **輕量快速**：啟動時間極短，適合在管道和腳本中高頻呼叫

## 設計決策

- **CLI 優先**：命令列是開發者的自然工作環境，所有功能均可透過 CLI 存取
- **結構化輸出**：支援 JSON/CSV 輸出，方便與其他工具和腳本整合
- **漸進式分析**：支援單模組分析和全量分析，按需取得資訊

## 未來規劃

- [ ] 多語言支援（中文情感分析、中文可讀性指標）
- [ ] HTML 報告生成
- [ ] 設定檔支援（自訂停用詞、分析參數）
- [ ] 外掛系統（可擴充的分析模組）
- [ ] 互動式 REPL 模式

---

# 📦 安裝與部署

## pip 安裝（推薦）

```bash
pip install textlens
```

## 從原始碼安裝

```bash
git clone https://github.com/gitstq/TextLens.git
cd TextLens
pip install .
```

## 開發環境搭建

```bash
git clone https://github.com/gitstq/TextLens.git
cd TextLens

# 安裝（開發模式）
pip install -e .

# 執行測試
python -m pytest textpulse/tests/

# 或直接執行
python -m textpulse.tests.test_all
```

## 系統需求

| 項目 | 最低需求 |
|------|----------|
| Python | 3.8+ |
| 作業系統 | Windows / macOS / Linux |
| 外部依賴 | 無 |

---

# 🤝 貢獻指南

我們歡迎任何形式的貢獻！無論是提交 Bug、改進文件，還是新增功能。

## 貢獻流程

1. **Fork** 本倉庫
2. 建立特性分支：`git checkout -b feature/your-feature`
3. 提交變更：`git commit -m "feat: add your feature"`
4. 推送分支：`git push origin feature/your-feature`
5. 提交 **Pull Request**

## Commit 規範

我們採用 [Conventional Commits](https://www.conventionalcommits.org/) 規範：

```
feat: 新功能
fix: 修復 Bug
docs: 文件更新
style: 程式碼格式調整
refactor: 重構
test: 測試相關
chore: 建構/工具鏈相關
```

## 程式碼規範

- 遵循 PEP 8 編碼規範
- 所有新功能必須附帶單元測試
- 保持零外部依賴的原則

---

# 📄 開源協議

本專案基於 [MIT License](LICENSE) 開源。

```
MIT License

Copyright (c) 2024 gitstq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<a id="english"></a>

# 🎉 Introduction

**TextLens** is a lightweight text analytics and visualization CLI tool designed to provide developers, writers, and data analysts with **instant, intuitive, zero-friction** text insights.

### What Problem Does It Solve?

In daily development and writing, we often need to quickly understand the characteristics of a piece of text — what is the sentiment, how readable is it, what is the word frequency distribution, is passive voice present... However, existing text analysis tools often suffer from these pain points:

- **Heavy dependencies**: Require NLTK, spaCy, or other large NLP libraries, often hundreds of MB
- **Complex setup**: Need to download language models, dictionaries, and other additional resources
- **Fragmented features**: Sentiment analysis, readability assessment, and word frequency stats are spread across different tools
- **Lack of visualization**: Analysis results are just dry numbers without intuitive terminal visualization

### What Makes TextLens Different

- **Zero external dependencies**: Pure Python standard library implementation, ready to use with `pip install`, no model or data files to download
- **Comprehensive features**: Sentiment analysis, readability assessment, text statistics, word frequency analysis, pattern detection — all in one tool
- **Terminal visualization**: Built-in rich terminal charts (bar charts, gauges, sparklines, etc.) that make data immediately clear
- **Flexible output**: Supports Dashboard, plain text, JSON, Markdown, CSV, and more
- **Pipeline-friendly**: File processing, stdin support, directory batch processing — seamlessly fits into your workflow

---

# ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🎭 **Sentiment Analysis** | Positive/negative/neutral classification with confidence scores, handles negation and intensifiers |
| 📊 **Readability Analysis** | Flesch Reading Ease, Gunning Fog Index, Coleman-Liau Index, automatic grade level assessment |
| 📈 **Text Statistics** | Word count, sentence count, character count, paragraph count, reading time, lexical diversity (TTR) |
| 🔤 **Word Frequency Analysis** | Top N words, n-gram analysis, stop word filtering |
| 🔍 **Pattern Detection** | Question/exclamation counting, passive voice detection, sentence complexity analysis |
| 🖥️ **Terminal Visualization** | Bar charts, horizontal bars, progress bars, gauges, sparklines, full dashboards |
| 📋 **Multiple Output Formats** | Dashboard, plain text, JSON, Markdown, CSV |
| 🔗 **Pipeline Processing** | File processing, stdin support, directory batch processing |

---

# 🚀 Quick Start

## Requirements

- **Python** 3.8 or later
- **Zero** external dependencies (pure standard library)

## Installation

```bash
# Install from PyPI (recommended)
pip install textlens

# Or install from source
git clone https://github.com/gitstq/TextLens.git
cd TextLens
pip install .
```

## Basic Usage

```bash
# Analyze text directly
textlens "TextLens makes text analysis simple and efficient!"

# Analyze a file
textlens -f document.txt

# Quick sentiment analysis
textlens -m sentiment "I love this product!"

# Full dashboard visualization
textlens -f report.txt --format dashboard
```

## Python API Quick Start

```python
from textpulse.analyzer import TextLensEngine

engine = TextLensEngine()

# Get complete analysis results with one call
result = engine.analyze("TextLens makes text analysis simple and efficient!")
print(engine.quick_summary(result))
```

---

# 📖 Detailed Usage Guide

## Full CLI Options

```bash
# Analysis modes
textlens -m sentiment "text"          # Sentiment analysis only
textlens -m readability "text"        # Readability analysis only
textlens -m stats "text"              # Text statistics only
textlens -m frequency "text"         # Word frequency analysis only
textlens -m pattern "text"            # Pattern detection only
textlens -m compare -f a.txt -f b.txt # Compare analysis

# Output formats
textlens -f doc.txt --format json       # JSON output
textlens -f doc.txt --format markdown   # Markdown output
textlens -f doc.txt --format csv        # CSV output
textlens -f doc.txt --format dashboard  # Dashboard visualization
textlens -f doc.txt --format text       # Plain text output

# Input methods
textlens -f document.txt               # Analyze a file
cat article.txt | textlens --stdin     # Read from stdin
textlens --dir ./docs --ext .txt,.md   # Batch process directory

# Combined usage
textlens -m readability -f essay.txt --format json
textlens -m sentiment -f review.txt --format dashboard
```

## Python API Details

```python
from textpulse.analyzer import TextLensEngine, SentimentAnalyzer
from textpulse.visualizer import TextLensDashboard

# ===== Full Analysis =====
engine = TextLensEngine()
result = engine.analyze("Your text to analyze...")
print(TextLensDashboard.render_dashboard(result))

# ===== Quick Summary =====
print(engine.quick_summary("Your text to analyze..."))

# ===== Sentiment Analysis =====
analyzer = SentimentAnalyzer()
sentiment = analyzer.analyze("I love this amazing product!")
print(f"Score: {sentiment.score}, Label: {sentiment.label}")

# ===== Readability Analysis =====
result = engine.analyze("A piece of text for readability testing...")
print(f"Flesch Score: {result.readability.flesch_score}")
print(f"Grade Level: {result.readability.grade_level}")
```

## Analysis Modes Explained

| Mode | Description | Use Cases |
|------|-------------|-----------|
| `sentiment` | Sentiment analysis | User reviews, feedback, social media text |
| `readability` | Readability analysis | Articles, papers, technical documentation |
| `stats` | Text statistics | Quick overview of text characteristics |
| `frequency` | Word frequency analysis | SEO optimization, keyword extraction |
| `pattern` | Pattern detection | Writing style analysis, text quality checks |
| `compare` | Comparison analysis | A/B testing, version comparison |

---

# 💡 Design Philosophy & Roadmap

## Why Pure Python?

1. **Zero-friction installation**: `pip install textlens` and you're done — no GB-sized model files to download
2. **Cross-platform compatibility**: No C extensions or system libraries, runs in any Python environment
3. **Security and control**: No third-party code introduced, suitable for security-sensitive environments
4. **Lightweight and fast**: Extremely fast startup time, ideal for high-frequency use in pipelines and scripts

## Design Decisions

- **CLI-first**: The command line is the natural working environment for developers; all features are accessible via CLI
- **Structured output**: JSON/CSV output support for easy integration with other tools and scripts
- **Progressive analysis**: Supports single-module and full analysis — get only the information you need

## Roadmap

- [ ] Multi-language support (Chinese sentiment analysis, Chinese readability metrics)
- [ ] HTML report generation
- [ ] Configuration file support (custom stop words, analysis parameters)
- [ ] Plugin system (extensible analysis modules)
- [ ] Interactive REPL mode

---

# 📦 Installation & Deployment

## pip Install (Recommended)

```bash
pip install textlens
```

## Install from Source

```bash
git clone https://github.com/gitstq/TextLens.git
cd TextLens
pip install .
```

## Development Setup

```bash
git clone https://github.com/gitstq/TextLens.git
cd TextLens

# Install in development mode
pip install -e .

# Run tests
python -m pytest textpulse/tests/

# Or run directly
python -m textpulse.tests.test_all
```

## System Requirements

| Item | Minimum Requirement |
|------|---------------------|
| Python | 3.8+ |
| Operating System | Windows / macOS / Linux |
| External Dependencies | None |

---

# 🤝 Contributing

We welcome contributions of all kinds! Whether it's filing a bug, improving documentation, or adding new features.

## Contribution Workflow

1. **Fork** this repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push the branch: `git push origin feature/your-feature`
5. Submit a **Pull Request**

## Commit Convention

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
feat: New feature
fix: Bug fix
docs: Documentation update
style: Code formatting
refactor: Refactoring
test: Test-related
chore: Build/toolchain related
```

## Code Standards

- Follow PEP 8 coding conventions
- All new features must include unit tests
- Maintain the zero external dependency principle

---

# 📄 License

This project is licensed under the [MIT License](LICENSE).

```
MIT License

Copyright (c) 2024 gitstq

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
