# MoffettHub CLI

MoffettHub CLI 是一个命令行工具，用于查询和下载 MoffettHub 上的模型文件。它提供了类似 Hugging Face CLI 的体验，让您可以方便地管理和下载模型。

## 功能特点

- 浏览和搜索模型仓库
- 下载模型文件
- 显示下载进度
- 支持并行下载
- 管理本地下载模型

## 安装要求

- Python >= 3.7
- pigz (用于并行解压缩，可选)

## 安装

```bash
# 安装 Python 包
pip install moffetthub-cli

# 安装 pigz (Ubuntu/Debian)
sudo apt install pigz

# 安装 pigz (macOS)
brew install pigz
```

## 使用示例

### 列出模型仓库内容

```bash
moffetthub-cli list
```

### 下载模型（默认下载路径为 ~/.moffetthub_cache）

```bash
moffetthub-cli download deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```

### 查看本地下载模型

```bash
moffetthub-cli list-cache
```

### 删除本地下载模型

```bash
moffetthub-cli remove-cache deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B
```

## 许可证

本项目采用 MIT 许可证 - 详见 LICENSE 文件

