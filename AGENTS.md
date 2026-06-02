---
name: amap-weather
description: Use when the user needs weather data for Chinese cities using AMap Weather API. Automatically retrieves API key from project .env file.
author: local
version: 1.0.0
---

## Description
获取中国城市天气数据，支持实时天气和未来天气预报。

## When to use
- 用户询问中国城市天气时
- 需要获取天气信息作为决策参考时

## Instructions
1. 用户请求天气时，直接调用本地 Python 脚本获取数据
2. 脚本路径：`.trae/skills/amap-weather/amap_weather.py`
3. 执行命令：`python .trae/skills/amap-weather/amap_weather.py <城市名>`

## Examples
输入：长沙天气
输出：调用脚本获取并返回格式化的天气信息

## Configuration
- 需要在项目根目录的 `.env` 文件中配置 `AMAP_API_KEY`
- 当前已配置：API Key 已存在
