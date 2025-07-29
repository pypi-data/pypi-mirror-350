# Python  MCP Server 记账服务

模型上下文协议 MCP 是一种开放协议，旨在标准化 AI 应用程序与外部数据源和工具的连接方式。其核心目标在于简化大型语言模型 LLM 与各种上下文和工具的集成，从而解决将多种 LLM 与多种工具相集成的复杂性问题。

不过，现在好了，因为有了 FastMCP，它是一个 Python 软件开发工具包 (SDK)，专门设计用于简化构建 MCP 服务的过程。它提供了一个高级且符合 Python 语言习惯的接口，用于定义工具、资源和提示。FastMCP 的核心优势在于其能够帮助开发者更轻松地创建符合 MCP 规范的服务，而无需深入了解底层的协议细节。

本文使用官方 Python SDK 里的 FastMCP 来构建自己的 MCP 服务。

## 记账 mcp 服务

我们基于 MCP 开发了一个轻量级（玩具级）记账服务 `Bill Track MCP`，旨在帮助用户管理和跟踪财务数据。该服务利用 Python 和 `FastMCP` 框架，提供了三种核心功能类型（工具、资源和提示），为用户提供一个灵活、高效的解决方案来记录收入和支出、查询账户状态以及生成格式化的财务报告。

项目虽小，但涉及环境变量的设置和读取，用户数据的存储等多个方面，对于开发更强大服务来说是一个不错的基础。完整代码的地址见文末。

### 核心功能

1. 工具 (​`​@tool​`​​)：服务提供了一个名为​`​record_transaction​`​ 的工具，允许用户动态输入当天的收入和支出，如「今天赚了 500 元，花了 250 元」。工具会自动更新累积的总收入、总支出，并计算当前余额。这些数据持久化存储在用户指定的文件中，确保数据不会丢失。
2. 资源 (​`​@resource​`​​)：通过​`​get_account_status​`​​ 资源，用户可以安全地检索当前账户的最新状态，包括总收入、总支出和余额。资源数据存储在 JSON 文件中，文件路径可以由用户通过环境变量或配置文件自定义，默认位于​`​./accounting_data/accounting_data.json​`​。
3. 提示 (​`​@prompt​`​​)：​`​format_account_report​`​ 提示负责将账户状态格式化为易读的报告。

### 技术架构

- **框架**：基于​`​FastMCP​`​，一个高效的 Python 库，简化了 MCP 服务器的开发。
- **存储**：数据保存在 JSON 文件中，支持用户自定义存储路径（如通过环境变量​`​ACCOUNTING_WORKING_DIR​`​ 或配置文件）。
- **通信**：默认使用标准输入输出 (​`​stdio​`​) 传输协议，方便本地开发和测试。
- **日志**：支持​`​INFO​`​​ 和​`​DEBUG​`​ 级别的日志记录，帮助开发者监控服务运行状态和调试问题。

### 使用场景

`BillTrack MCP` 适用于多种场景，包括但不限于：

- **个人财务管理**：个人用户可以通过客户端记录日常收支，并随时查看余额。
- **企业/团队记账**：小型企业或团队可以集成此服务到更大的财务系统中，快速统计现金流。
- **教育与开发示例**：开发者可以作为 MCP 服务的学习示例，了解工具、资源和提示的协同工作。

具体代码如下，

```
# ./src/server.py
from mcp.server.fastmcp import FastMCP
import os
import json
from typing import Dict, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量或默认值获取工作目录
DEFAULT_WORKING_DIR = "~/accounting_data"
WORKING_DIR = os.getenv("ACCOUNTING_WORKING_DIR", DEFAULT_WORKING_DIR)

# 确保目录存在
os.makedirs(WORKING_DIR, exist_ok=True)

# 数据文件路径
DATA_FILE = os.path.join(WORKING_DIR, "accounting_data.json")

# 初始数据（如果文件不存在）
INITIAL_DATA = {
    "total_income": 0,
    "total_expense": 0,
    "balance": 0
}

def load_data() -> Dict:
    """从文件中加载数据，如果文件不存在则创建默认数据"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        else:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(INITIAL_DATA, f, indent=4)
            return INITIAL_DATA
    except Exception as e:
        logger.error(f"Failed to load data: {str(e)}")
        return INITIAL_DATA

def save_data(data: Dict) -> None:
    """将数据保存到文件"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        logger.error(f"Failed to save data: {str(e)}")

# 创建 MCP 服务器
mcp = FastMCP("bill-track-mcp", log_level="ERROR")

# 工具：记录收入和支出
@mcp.tool()
def record_transaction(income: Optional[int] = 0, expense: Optional[int] = 0) -> Dict:
    """记录今天的收入和支出，更新账户余额"""
    ifnot isinstance(income, (int, float)) ornot isinstance(expense, (int, float)):
        return {"error": "Income and expense must be numbers"}

    data = load_data()
    data["total_income"] += income
    data["total_expense"] += expense
    data["balance"] = data["total_income"] - data["total_expense"]
    save_data(data)

    return {
        "message": "Transaction recorded successfully",
        "total_income": data["total_income"],
        "total_expense": data["total_expense"],
        "balance": data["balance"]
    }

# 资源：获取当前账户状态
@mcp.resource("accounting://status")
def get_account_status() -> Dict:
    """获取当前账户的收入、支出和余额"""
    data = load_data()
    return {
        "total_income": data["total_income"],
        "total_expense": data["total_expense"],
        "balance": data["balance"]
    }

# 提示：格式化账户报告
@mcp.prompt()
def format_account_report(status: Dict) -> str:
    """格式化账户状态为易读的报告"""
    returnf"""
    === 账户报告 ===
    总收入: ${status["total_income"]:.2f}
    总支出: ${status["total_expense"]:.2f}
    当前余额: ${status["balance"]:.2f}
    ================
    """

def run_server():
    """运行 MCP 服务器"""
    print("=== Bill Track MCP 服务启动 ===")
    logging.info("Bill Track MCP 服务启动")
    print(f"当前工作目录: {os.getcwd()}")

    mcp.run(transport='stdio')
```

### 安装

```bash
./setup_venv.sh
```

### 配置信息

```bash
{
  "mcpServers": {
    "bill-track-mcp": {
      "command": "your_python_path/python",
      "args": [
        "your_mcp_bill_track_path/main.py"
      ],
      "env": {
        "ACCOUNTING_WORKING_DIR": "your_accounting_data_path"
      }
    }
  }
} 
```