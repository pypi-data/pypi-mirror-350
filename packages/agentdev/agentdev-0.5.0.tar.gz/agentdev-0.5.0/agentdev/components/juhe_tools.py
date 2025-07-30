# -*- coding: utf-8 -*-
import os
from datetime import date as datee
from datetime import timedelta
from typing import Optional
from urllib.parse import urlencode

import requests

from agentdev.base.function_tool import function_tool

EXCHANGE_AK = os.getenv("EXCHANGE_AK", "")
HIS_WEATHER_AK = os.getenv("HIS_WEATHER_AK", "")
WEATHER_AK = os.getenv("WEATHER_AK", "")
STOCK_AK = os.getenv("STOCK_AK", "")
GOLD_PRICE_AK = os.getenv("GOLD_PRICE_AK", "")
OIL_PRICE_AK = os.getenv("OIL_PRICE_AK", "")
CALENDAR_AK = os.getenv("CALENDAR_AK", "")

EXCHANGE_TOOL_URL = "http://op.juhe.cn/onebox/exchange/currency"
WEATHER_TOOL_URL = "http://apis.juhe.cn/simpleWeather/query"
HIS_WEATHER_TOOL_URL = "http://v.juhe.cn/hisWeather/weather"
# 沪深/hs、香港/hk、美国/usa
STOCK_TOOL_URL = "http://web.juhe.cn/finance/stock"
GOLD_PRICE_TOOL_URL = "http://web.juhe.cn/finance/gold/shgold"
OIL_PRICE_TOOL_URL = "http://apis.juhe.cn/gnyj/query"
CALENDAR_TOOL_URL = "http://v.juhe.cn/calendar/day"
NEWS_TOOL_URL = "http://pre-dataai.alibaba-inc.com/api/v1/web_tool/execute"

timeout_ms = 3000


@function_tool
def exchange(from_currency: str, to_currency: str) -> str:
    url = EXCHANGE_TOOL_URL
    params = {"key": EXCHANGE_AK, "from": from_currency, "to": to_currency}
    full_url = f"{url}?{urlencode(params)}"
    response = requests.get(full_url, timeout=timeout_ms / 1000.0)
    res = response.json()
    exchange_obj = res["result"][0]
    exchange_msg = (
        f"{from_currency}兑{to_currency}的当前汇率为{exchange_obj['exchange']}"
    )
    return exchange_msg


@function_tool
def weather(city_id: int, city_name: str, date: str) -> str:
    """get real time weather information"""
    date_str = date
    current_date = datee.today()
    if current_date > datee.fromisoformat(date_str):
        # 查历史天气
        url = HIS_WEATHER_TOOL_URL
        params = {
            "key": HIS_WEATHER_AK,
            "city_id": city_id,
            "weather_date": date_str,
        }
    else:
        # 查当前、未来天气
        url = WEATHER_TOOL_URL
        params = {"key": WEATHER_AK, "city": city_id}

    full_url = f"{url}?{urlencode(params)}"
    response = requests.get(full_url, timeout=timeout_ms / 1000.0)
    res = response.json()
    weather_obj = res["result"]
    weather_msg = f"{city_name} {date_str}天气信息：\n天气描述："
    if current_date > datee.fromisoformat(date_str):
        # 解析历史天气
        weather_msg += (
            f"{weather_obj['day_weather']}\n温度："
            f"{weather_obj['night_temp']}/{weather_obj['day_temp']}℃\n风向："
            f"{weather_obj['day_wind']}"
        )
    elif current_date == datee.fromisoformat(date_str):
        # 解析当前天气
        realtime_obj = weather_obj["realtime"]
        weather_msg += (
            f"{realtime_obj['info']}\n温度："
            f"{realtime_obj['temperature']}\n风向："
            f"{realtime_obj['direct']}"
        )
    else:
        # 解析未来天气
        future_arr = weather_obj["future"]
        for future in future_arr:
            if future["date"] == date_str:
                weather_msg += (
                    f"{future['weather']}\n温度："
                    f"{future['temperature']}\n风向："
                    f"{future['direct']}"
                )
    return weather_msg


@function_tool
def stock(
    market_name: str,
    company_code: str,
    index_name: Optional[str] = "沪",
    company_name: Optional[str] = None,
) -> str:
    """get real time stock information"""
    base_url = STOCK_TOOL_URL

    if market_name in ["沪", "深"]:
        base_url += "/hs"
    elif market_name == "港":
        base_url += "/hk"
    else:
        base_url += "/usa"

    url = base_url
    params = {"key": STOCK_AK, "gid": company_code}

    if index_name:
        params["type"] = "0" if index_name == "沪" else "1"

    full_url = f"{url}?{urlencode(params)}"
    response = requests.get(full_url, timeout=timeout_ms / 1000.0)
    res = response.json()
    stock_msg = ""

    if index_name:
        # 指数信息
        index_obj = res["result"][0]["data"]
        stock_msg = f"{index_name}股指数：\n最新价{index_obj['lastestpri']}\n开盘价{index_obj['openpri']}\n最高价{index_obj['maxpri']}\n最低价{index_obj['minpri']}\n涨跌额{index_obj['uppic']}\n涨跌幅%{index_obj['limit']}"  # noqa: E501
    else:
        # 股票信息
        stock_obj = res["result"][0]
        stock_data = stock_obj["data"]

        if market_name in ["沪", "深"]:
            stock_msg = f"{company_name}{market_name}股：\n最新价{stock_data['nowpri']}\n开盘价{stock_data['todayStartPri']}\n最高价{stock_data['todayMax']}\n最低价{stock_data['todayMin']}\n涨跌额{stock_data['increase']}\n涨跌幅{stock_data['increPer']}"  # noqa: E501
        else:
            stock_msg = f"{company_name}{market_name}股：\n最新价{stock_data['lastestpri']}\n开盘价{stock_data['openpri']}\n最高价{stock_data['maxpri']}\n最低价{stock_data['minpri']}\n涨跌额{stock_data['uppic']}\n涨跌幅%{stock_data['limit']}"  # noqa: E501

    return stock_msg


@function_tool
def gold_price() -> str:
    """get real time gold price detail"""
    url = GOLD_PRICE_TOOL_URL
    params = {"key": GOLD_PRICE_AK, "v": "1"}
    full_url = f"{url}?{urlencode(params)}"
    response = requests.get(full_url, timeout=timeout_ms / 1000.0)
    res = response.json()
    gold_obj = res["result"][0]
    au = gold_obj["Au100g"]
    gold_msg = f"黄金价格：\n最新价{au['latestpri']}元/克\n开盘价{au['openpri']}元/克\n最高价{au['maxpri']}元/克\n最低价{au['minpri']}元/克\n涨跌幅{au['limit']}"  # noqa: E501
    return gold_msg


@function_tool
def silver_price() -> str:
    """get real time silver price"""
    url = GOLD_PRICE_TOOL_URL
    params = {"key": GOLD_PRICE_AK, "v": "1"}
    full_url = f"{url}?{urlencode(params)}"
    response = requests.get(full_url, timeout=timeout_ms / 1000.0)
    res = response.json()
    silver_obj = res["result"][0]
    ag = silver_obj["Ag(T+D)"]
    silver_msg = f"白银价格：\n最新价{ag['latestpri']}元/千克\n开盘价{ag['openpri']}元/千克\n最高价{ag['maxpri']}元/千克\n最低价{ag['minpri']}元/千克\n涨跌幅{ag['limit']}"  # noqa: E501
    return silver_msg


@function_tool
def oil_price(province: str) -> str:
    """get real time oil price"""
    url = OIL_PRICE_TOOL_URL
    params = {"key": OIL_PRICE_AK}
    full_url = f"{url}?{urlencode(params)}"
    response = requests.get(full_url, timeout=timeout_ms / 1000.0)
    res = response.json()
    oil_arr = res["result"]
    oil_msg = ""
    oil_beijing_msg = ""

    for oil_obj in oil_arr:
        if oil_obj["city"] == "北京":
            oil_beijing_msg = f"北京油价：\n92号：{oil_obj['92h']}\n95号：{oil_obj['95h']}\n98号：{oil_obj['98h']}\n0号：{oil_obj['0h']}"  # noqa: E501
        if oil_obj["city"] == province:
            oil_msg = f"{province}油价：\n92号：{oil_obj['92h']}\n95号：{oil_obj['95h']}\n98号：{oil_obj['98h']}\n0号：{oil_obj['0h']}"  # noqa: E501

    if not oil_msg:
        oil_msg = oil_beijing_msg

    return oil_msg


@function_tool
def calendar(date: str, origin_obj: bool = False) -> str:
    """return calendar detail info"""
    calendar_date = date.replace("-0", "-")
    url = CALENDAR_TOOL_URL
    params = {"key": CALENDAR_AK, "date": calendar_date}
    full_url = f"{url}?{urlencode(params)}"
    response = requests.get(full_url, timeout=timeout_ms / 1000.0)
    res = response.json()

    calendar_obj = res["result"]
    calendar_data = calendar_obj["data"]
    if origin_obj:
        return calendar_data

    calendar_msg = (
        "#万年历\n\n"
        + f"##假日\n{calendar_data.get('holiday', '')}\n\n"
        + f"##忌\n{calendar_data.get('avoid', '')}\n\n"
        + f"##属相\n{calendar_data.get('animalsYear', '')}\n\n"
        + f"##假日描述\n{calendar_data.get('desc', '')}\n\n"
        + f"##周几\n{calendar_data.get('weekday', '')}\n\n"
        + f"##宜\n{calendar_data.get('suit', '')}\n\n"
        + f"##纪年\n{calendar_data.get('lunarYear', '')}\n\n"
        + f"##农历\n{calendar_data.get('lunar', '')}\n\n"
        + f"##年份和月份\n{calendar_data.get('year-month', '')}\n\n"
        + f"##具体日期\n{calendar_data.get('date', '')}"
    )

    return calendar_msg


@function_tool
def calculate_relative_date(date: str, days: int) -> str:
    """calculate relative date from start date to the days given"""
    start_date = date
    calendar_obj = calendar(start_date, True)
    holiday = calendar_obj.get("holiday", "")
    start_weekday = calendar_obj.get("weekday")
    end_date = datee.fromisoformat(start_date) + timedelta(days=days)
    end_date = end_date.isoformat()
    calendar_obj = calendar(end_date, True)
    end_holiday = calendar_obj.get("holiday", "")
    end_weekday = calendar_obj.get("weekday")
    msg = f"距离({start_date} {start_weekday} {holiday}){days}天的日期是({end_date} {end_weekday} {end_holiday})"  # noqa E501
    return msg


@function_tool
def calculate_days_between_dates(start_date: str, end_date: str) -> str:
    """calculate days between start data to end data"""
    calendar_obj = calendar(start_date, True)
    start_holiday = calendar_obj.get("holiday", "")
    start_weekday = calendar_obj.get("weekday")
    calendar_obj = calendar(end_date, True)
    end_holiday = calendar_obj.get("holiday", "")
    end_weekday = calendar_obj.get("weekday")
    day_delta = datee.fromisoformat(end_date) - datee.fromisoformat(start_date)
    days = day_delta.days
    if days > 0:
        msg = (
            f"({start_date} {start_weekday} {start_holiday})距离({end_date} "
            f"{end_weekday} {end_holiday})还有{days}天"
        )
    else:
        msg = (
            f"({end_date} {end_weekday} {end_holiday})距离({start_date} "
            f"{start_weekday} {start_holiday})还有{-days}天"
        )
    return msg


if __name__ == "__main__":
    parameters = exchange.verify_args(
        {"from_currency": "CNY", "to_currency": "USD"},
    )
    resp = exchange.run(parameters)
    print(resp, "\nExchange Passed")

    resp = weather.run(
        **{"city_id": 1, "city_name": "北京", "date": "2024-02-27"},
    )
    print(resp)

    resp = weather.run(
        **{"city_id": 1, "city_name": "安庆", "date": "2024-12-27"},
    )
    print(resp, "\nWeather Passed")

    resp = stock.run(**{"market_name": "美", "company_code": "BABA"})
    print(resp, "\nStock Passed")

    resp = oil_price.run(**{"province": "北京"})
    print(oil_price.function_schema.model_dump())
    print(resp, "\nOil_price Passed")

    resp = gold_price.run(**{"test": "123"})
    print(gold_price.function_schema.model_dump())
    print(resp, "\ngold_price Passed")

    resp = silver_price.run()
    print(resp, "\nsilver_price Passed")

    resp = calendar.run({"date": "2024-12-30"})
    print(resp, "\nCalender Passed")

    resp = calculate_relative_date.run(**{"date": "2025-01-02", "days": 12})
    print(resp, "\n calculate_relative_date Passed")

    resp = calculate_days_between_dates.run(
        **{"start_date": "2025-01-01", "end_date": "2025-01-28"},
    )
    print(resp, "\n calculate_days_between_dates Passed")
