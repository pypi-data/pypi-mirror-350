from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from .stock_data import get_etf_data, get_stock_hist_data, calculate_rsi, calculate_bollinger_bands, calculate_moving_averages, calculate_atr, classify_market_style
import pandas as pd

app = FastAPI(
    title="Technical Analysis API",
    description="金融技术指标分析API",
    version="0.1.0",
    openapi_url="/openapi.json",
    docs_url="/docs"
)

@app.get("/api/etf/{etf_code}", summary="ETF技术指标分析")
async def analyze_etf_technical(etf_code: str = '510300', with_market_style: bool = True, base_date: str = None) ->dict:
    """
    获取ETF技术指标数据
    - **etf_code**: ETF代码 (例如'510300') 不要使用LOF代码
    - **with_market_style**: 是否对市场风格进行分类 (True/False)
    - **base_date**: 基准日期(格式YYYYMMDD)，默认为当前日期
    
    返回格式示例:
    {
        "date": "2023-01-01",
        "close": 4.12,
        "rsi_10": 65.32,
        "boll_upper": 4.25,
        "boll_middle": 4.10,
        "boll_lower": 3.95,
        "ma_5": 4.08,
        "ma_10": 4.05,
        "ma_20": 4.02,
        "atr": 0.15,
        "mkt_style": "震荡市",
        "volume": 120000
    }
    
    字段说明:
    - date: 交易日期
    - close: 收盘价
    - rsi_10: 10日相对强弱指数(30-70为正常区间)
    - boll_upper: 布林带上轨(20日平均+2倍标准差)
    - boll_middle: 布林带中轨(20日移动平均)
    - boll_lower: 布林带下轨(20日平均-2倍标准差)
    - ma_5: 5日移动平均
    - ma_10: 10日移动平均
    - ma_20: 20日移动平均
    - atr: 平均真实波幅(10日)，衡量价格波动性的指标
    - mkt_style: 市场风格分类结果
    - volume: 成交量(单位:份)，反映市场活跃度，高成交量通常伴随价格趋势确认
    """
    df = get_etf_data(etf_code=etf_code, end_date=base_date)
    if df is not None:
        df = calculate_rsi(df)
        df = calculate_bollinger_bands(df)
        df = calculate_moving_averages(df)
        df['atr'] = calculate_atr(df)
        if with_market_style:
            df = pd.concat([df, classify_market_style(df)], axis=1)
        return {"results": df.tail(5).to_dict(orient="records")}
    else:
        return {"error": "无法获取数据"}

@app.get("/api/stock/{stock_code}", summary="股票技术指标分析")
async def analyze_stock_hist_technical(stock_code: str = '000001', with_market_style: bool = True, base_date: str = None) ->dict:
    """
    获取股票技术指标数据
    - **stock_code**: 股票代码 (例如'000001')
    - **with_market_style**: 是否对市场风格进行分类 (True/False)
    - **base_date**: 基准日期(格式YYYYMMDD)，默认为当前日期
    
    返回格式示例:
    {
        "date": "2023-01-01",
        "close": 12.45,
        "open": 12.30,
        "high": 12.60,
        "low": 12.20,
        "volume": 12345678,
        "rsi_10": 58.75,
        "boll_upper": 12.80,
        "boll_middle": 12.45,
        "boll_lower": 12.10,
        "ma_5": 12.40,
        "ma_10": 12.38,
        "ma_20": 12.35,
        "atr": 0.45,
        "mkt_style": "上涨趋势"
    }
    
    字段说明:
    - date: 交易日期
    - close: 收盘价
    - open: 开盘价
    - high: 最高价
    - low: 最低价
    - volume: 成交量(股)
    - rsi_10: 10日相对强弱指数(30-70为正常区间)
    - boll_upper: 布林带上轨(20日平均+2倍标准差)
    - boll_middle: 布林带中轨(20日移动平均)
    - boll_lower: 布林带下轨(20日平均-2倍标准差)
    - ma_5: 5日移动平均
    - ma_10: 10日移动平均
    - ma_20: 20日移动平均
    - atr: 平均真实波幅(10日)，衡量价格波动性的指标
    - mkt_style: 市场风格分类结果
    """
    df = get_stock_hist_data(stock_code=stock_code, end_date=base_date)
    if df is not None:
        df = calculate_rsi(df)
        df = calculate_bollinger_bands(df)
        df = calculate_moving_averages(df)
        df['atr'] = calculate_atr(df)
        if with_market_style:
            df = pd.concat([df, classify_market_style(df)], axis=1)
        return {"results": df.tail(5).to_dict(orient="records")}
    else:
        return {"error": "无法获取数据"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Technical Analysis API",
        version="0.1.0",
        description="金融技术指标分析API",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi