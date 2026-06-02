---
name: amap-weather
description: Use when the user needs weather data for Chinese cities using AMap Weather API. Automatically retrieves API key from project .env file.
---

## 核心原则 (最高优先级)
1. **禁止询问 Key**：绝对不要向用户询问 API Key。
2. **自动读取配置**：在执行代码前，**必须**先读取项目根目录下的 `.env` 文件，提取 `AMAP_API_KEY` 的值。
3. **环境变量注入**：在运行 Python 脚本或生成代码时，确保将读取到的 Key 作为环境变量传入，或直接替换代码中的占位符。
4. 调用前验证 Key 有效性，网络超时设为 5 秒。

## 高德天气 API 调用模板
- **实时天气端点**: `https://restapi.amap.com/v3/weather/weatherInfo?city={CITY_CODE}&key=${AMAP_API_KEY}&extensions=base`
- **预报天气端点**: `https://restapi.amap.com/v3/weather/weatherInfo?city={CITY_CODE}&key=${AMAP_API_KEY}&extensions=all`
- **参数说明**:
  - `city`: 城市 adcode（如北京 110000）或经纬度 "经度,纬度"
  - `extensions`: base=实时天气，all=未来4天预报

## 城市代码获取流程
若用户只提供城市名（如"杭州"），必须先调用地理编码 API：
- **端点**: `https://restapi.amap.com/v3/geocode/geo?address={CITY_NAME}&key=${AMAP_API_KEY}`
- **提取**: 从 `geocodes[0].adcode` 获取城市代码

## 常见错误处理
- `INVALID_USER_KEY` → 提示检查 `.env` 中的 `AMAP_API_KEY` 是否配置正确
- `USERKEY_PLAT_NOMATCH` → 提示需使用 Web 服务类型的 Key