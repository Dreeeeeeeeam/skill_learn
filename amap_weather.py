import os
import requests
import json

class AmapWeather:
    # 类级别的静态变量，用于缓存API Key，只加载一次
    _cached_api_key = None
    _key_loaded = False
    
    def __init__(self):
        self.api_key = self._get_api_key()
        self.timeout = 5
    
    @classmethod
    def _load_api_key_once(cls):
        """仅在首次调用时从.env文件加载API Key，之后缓存复用"""
        if cls._key_loaded:
            return
        
        # 优先从环境变量获取
        api_key = os.environ.get('AMAP_API_KEY', '')
        if api_key:
            cls._cached_api_key = api_key
            cls._key_loaded = True
            return
        
        # 从项目根目录的.env文件读取（已知路径）
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        env_path = os.path.join(project_root, '.env')
        
        if os.path.exists(env_path):
            try:
                with open(env_path, 'r', encoding='utf-8-sig') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and line.startswith('AMAP_API_KEY='):
                            cls._cached_api_key = line.split('=', 1)[1].strip()
                            break
            except Exception:
                pass
        
        cls._key_loaded = True
    
    @classmethod
    def _get_api_key(cls):
        """获取API Key（自动处理缓存）"""
        cls._load_api_key_once()
        return cls._cached_api_key or ''
    
    def get_city_code(self, city_name):
        """通过地理编码API获取城市adcode"""
        if not self.api_key:
            return None, "未配置AMAP_API_KEY环境变量"
        
        url = f"https://restapi.amap.com/v3/geocode/geo?address={city_name}&key={self.api_key}"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.encoding = 'utf-8'
            data = response.json()
            
            if data.get('status') == '1' and data.get('geocodes'):
                return data['geocodes'][0]['adcode'], None
            else:
                return None, data.get('info', '获取城市代码失败')
        except Exception as e:
            return None, str(e)
    
    def get_weather(self, city, extensions='all'):
        """获取天气数据"""
        if not self.api_key:
            return None, "未配置AMAP_API_KEY环境变量"
        
        city_code, error = self.get_city_code(city)
        if error:
            return None, error
        
        url = f"https://restapi.amap.com/v3/weather/weatherInfo?city={city_code}&key={self.api_key}&extensions={extensions}"
        try:
            response = requests.get(url, timeout=self.timeout)
            response.encoding = 'utf-8'
            data = response.json()
            
            if data.get('status') == '1':
                return data, None
            else:
                info = data.get('info', '获取天气失败')
                if info == 'INVALID_USER_KEY':
                    return None, "API Key无效或未开通天气服务"
                elif info == 'USERKEY_PLAT_NOMATCH':
                    return None, "Key类型不匹配，请使用Web服务Key"
                return None, info
        except requests.exceptions.Timeout:
            return None, "请求超时，请检查网络或Key配额"
        except Exception as e:
            return None, str(e)
    
    def format_weather_response(self, weather_data):
        """格式化天气响应"""
        if not weather_data:
            return "获取天气数据失败"
        
        result = ""
        
        # 实时天气
        if 'lives' in weather_data and weather_data['lives']:
            live = weather_data['lives'][0]
            result += f"【实时天气】\n"
            result += f"城市：{live.get('city', '')}\n"
            result += f"天气：{live.get('weather', '')}\n"
            result += f"温度：{live.get('temperature', '')}℃\n"
            result += f"风向：{live.get('winddirection', '')}\n"
            result += f"风力：{live.get('windpower', '')}级\n"
            result += f"湿度：{live.get('humidity', '')}%\n"
            result += f"更新时间：{live.get('reporttime', '')}\n\n"
        
        # 预报天气
        if 'forecasts' in weather_data and weather_data['forecasts']:
            forecast = weather_data['forecasts'][0]
            result += f"【未来天气预报】\n"
            result += f"城市：{forecast.get('city', '')}\n"
            
            for cast in forecast.get('casts', []):
                result += f"\n{cast.get('date', '')} {cast.get('week', '')}\n"
                result += f"  天气：{cast.get('dayweather', '')}转{cast.get('nightweather', '')}\n"
                result += f"  气温：{cast.get('nighttemp', '')}℃~{cast.get('daytemp', '')}℃\n"
                result += f"  风向：{cast.get('daywind', '')} {cast.get('daypower', '')}级\n"
        
        return result.strip()

def main(city, extensions='all'):
    weather = AmapWeather()
    data, error = weather.get_weather(city, extensions)
    
    if error:
        return f"错误：{error}"
    
    return weather.format_weather_response(data)

if __name__ == "__main__":
    import sys
    city = sys.argv[1] if len(sys.argv) > 1 else "北京"
    print(main(city))
