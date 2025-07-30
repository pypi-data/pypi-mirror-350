# 技术指标分析工具
该工具提供mcp服务器用于分析ETF和股票的技术指标。它使用`akshare`库获取历史数据，并计算RSI、布林带和移动平均线等技术指标。该工具支持ETF和股票历史数据分析。


## API文档

mcp服务器提供的接口:

### analyze_etf_technical

```python
@mcp.tool()
def analyze_etf_technical(etf_code='510300', with_market_style=False):
    """
    ETF技术指标分析工具
    :param etf_code: ETF代码 (例如'510300')
    :param with_market_style: 是否包含市场风格分类 (True/False)
    :param base_date: 基准日期，格式为YYYYMMDD (可选)
    :return: 包含技术指标的Markdown表格(最后5条记录)
    """
```

**新增字段说明**:


**参数**:
- `etf_code`: ETF代码，默认为'510300'(沪深300ETF)

**返回值**:
- 包含以下技术指标的Markdown表格:
  - 价格数据
  - RSI指标
  - 布林带
  - 移动平均线
  - `atr`: 平均真实波幅(10日)，衡量价格波动性的指标，数值越大表示波动越大
  - `mkt_style`: 市场风格分类结果

**示例**:
```python
result = analyze_etf_technical('510300')
print(result)
```

### analyze_stock_hist_technical

```python
@mcp.tool()
def analyze_stock_hist_technical(stock_code='000001'):
    """
    股票历史数据技术指标分析工具
    :param stock_code: 股票代码 (例如'000001')
    :param base_date: 基准日期，格式为YYYYMMDD (可选)
    :return: 包含技术指标的Markdown表格(最后5条记录)
    """
```

**参数**:
- `stock_code`: 股票代码，默认为'000001'(平安银行)

**返回值**:
- 包含以下技术指标的Markdown表格:
  - 价格数据
  - RSI指标
  - 布林带
  - 移动平均线
  - `atr`: 平均真实波幅(10日)，衡量价格波动性的指标，数值越大表示波动越大
  - `mkt_style`: 市场风格分类结果

**示例**:
```python
result = analyze_stock_hist_technical('000001')
print(result)
```
## 安装与配置

### 安装
```bash
pip install technical-analysis-mcp
```

### 配置
1. 确保已安装Python 3.8+版本
2. 需要配置akshare数据源(可选)
3. 运行MCP服务器:
```bash
technical-analysis-mcp
```

### 市场风格分类示例
```python
# 获取带市场风格分类的ETF技术指标
result = analyze_etf_technical('510300', with_market_style=True)
print(result)

# 获取带市场风格分类的股票技术指标
result = analyze_stock_hist_technical('000001', with_market_style=True)
print(result)
```

## MCP配置示例
```json
{
  "mcpServers": {
    "technical-analysis-mcp": {
      "command": "uvx",
      "args": ["technical-analysis-mcp"]
    }
  }
}
```
## Restful API

使用uvicorn启动FastAPI应用：
```bash
uvicorn technical_analysis.http:app --reload --port 8000
```

应用启动后，可以通过以下地址访问API文档：
http://localhost:8000/docs