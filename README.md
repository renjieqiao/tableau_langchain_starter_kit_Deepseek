
# Tableau LangChain 启动套件  (DeepSeek版)
这是一个强大的集成工具，通过 LangChain 为 Tableau Server 或 Tableau Cloud 增加 AI 功能，使用户可以用自然语言与 Tableau 中的数据进行交互。

本仓库是 tableau_langchain 的实现，并已注册至 PyPi。

## 🚀 功能  
- 用自然语言查询 Tableau 数据  
- 可通过 Web 界面或仪表板扩展访问  
- 支持 Tableau Server 和 Tableau Cloud

## 📋 前置条件  
在开始之前，请确保您具备以下条件：

- Tableau Server 版本 2025.1 或更高版本，或 Tableau Cloud（可通过 Tableau 开发者计划获得免费的 Tableau Cloud 试用）
- Python 3.12 或更高版本 - 下载 Python
- Git - 下载 Git
- 您选择的 AI 模型的 API 凭证（例如 DeepSeek）

⚠️ **警告**  
使用此代码时，来自 Tableau 的数据将被发送到外部 AI 模型（默认情况下为 DeepSeek）。为了学习和测试，强烈建议使用 Tableau 自带的 Superstore 数据集。

如果您需要处理敏感或专有信息，建议配置工具使用本地 AI 模型，而不是外部服务。这样可以确保您的数据保持在公司内部，减少数据泄露的风险。

## 📺 启动指南

### 🛠️ 安装  
1. 克隆仓库  
```bash
git clone https://github.com//tableau-langchain-starter-kit.git  
cd tableau-langchain-starter-kit
```
2. 创建虚拟环境  
创建虚拟环境有助于隔离项目依赖：

```bash
python -m venv venv
```
3. 激活虚拟环境  
Windows:

```bash
venv\Scriptsctivate
```
macOS/Linux:

```bash
source venv/bin/activate
```
💡 **提示**：当虚拟环境激活时，您应该看到命令行前面有（venv）标志。

4. 安装依赖  
```bash
pip install -r requirements.txt
```
如果遇到安装问题，请尝试先升级 pip：

```bash
pip install --upgrade pip
```

### ⚙️ 配置  
环境变量设置  
复制模板环境文件：

```bash
cp .env_template .env
```
用您喜欢的文本编辑器打开 `.env` 文件或者可以直接用VS打开编辑，并配置以下变量：
- # 模型提供者
```bash
OPENAI_API_KEY='来自 OpenAI 开发者门户'
MODEL_PROVIDER='openai'
```
- # LangSmith
```bash
LANGCHAIN_TRACING='true'
LANGCHAIN_API_KEY="来自 Langsmith 应用"
LANGCHAIN_PROJECT="Langsmith 项目名称"
```
- # Tableau Server / Cloud
```bash
TABLEAU_DOMAIN='您的 Tableau Cloud 或 Server 域名'
TABLEAU_SITE='您的 Tableau 站点'
TABLEAU_JWT_CLIENT_ID='来自 Connected App 配置页'
TABLEAU_JWT_SECRET_ID='来自 Connected App 配置页'
TABLEAU_JWT_SECRET='来自 Connected App 配置页'
TABLEAU_API_VERSION='3.21'
TABLEAU_USER='代理账户'
DATASOURCE_LUID='通过 graphql 元数据 API 获取的数据源唯一标识符'
```
⚠️ **安全提示**：永远不要将 `.env` 文件提交到版本控制中，它已经包含在 `.gitignore` 中。

### 🏃‍♂️ 运行应用程序  
#### 测试模式（命令行）  
适合测试配置并进行快速实验：

```bash
python main.py
```
该模式可以让您：

- 测试 Tableau 连接
- 验证 AI 服务集成
- 从命令行运行示例查询

#### Web 界面模式  
启动完整的 Web 应用程序，支持仪表板扩展：

```bash
python web_app.py
```
运行后，打开您的浏览器并访问：

本地开发： http://localhost:8000  
应用程序将在终端显示正确的 URL  
您现在可以像这样用自然语言提问：

- “客户满意度的趋势是什么？”
- “比较 Q1 和 Q2 的收入”
- “展示销售数据中的异常值”

#### 仪表板扩展  
启动完整的 Web 应用程序，支持仪表板扩展：

```bash
python web_app.py
```
运行后，打开您的 Tableau 工作簿或 Superstore 仪表板

在仪表板页面，左下角菜单拖动仪表板扩展，选择本地扩展，选择 `tableau_langchain.trex`（位于 dashboard_extension 文件夹）。

### 📄 许可证  
本项目采用 MIT 许可证 - 详情请参见 LICENSE 文件。

### 🤝 参与  
查看 Tableau LangChain 仓库获取更多开发信息  
加入 #tableau-langchain 话题，参与 Slack 讨论。可在此注册 DataDev Slack 渠道。

### 🙏 致谢  
感谢 Tableau LangChain 团队开发此工具  
感谢 LangChain 提供 AI 框架  
感谢 Tableau 提供可视化平台  
感谢所有帮助改进该项目的贡献者  

⭐ 如果您觉得这个项目有帮助，请考虑给它加个星！
