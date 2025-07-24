# hello_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.template.response import TemplateResponse
import json
import random
from datetime import datetime

# 用于存储传感器历史数据
sensor_history_data = []


@csrf_exempt
def greet(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            name = data.get('name', 'Guest')
            return JsonResponse({'greeting': f'Hello, {name}!'})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


def generate_sensor_data():
    """生成随机的传感器数据，模拟I2C传感器输出"""
    temperature = round(random.uniform(20.0, 35.0), 2)  # 温度: 20-35摄氏度
    humidity = round(random.uniform(30.0, 80.0), 2)  # 湿度: 30-80%
    current = round(random.uniform(0.5, 2.5), 2)  # 电流: 0.5-2.5A
    voltage = round(random.uniform(3.0, 5.0), 2)  # 电压: 3.0-5.0V

    return {
        'temperature': temperature,
        'humidity': humidity,
        'current': current,
        'voltage': voltage,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def sensor_data(request):
    """获取最新的传感器数据"""
    data = generate_sensor_data()

    # 保存到历史数据，只保留最近100条
    global sensor_history_data
    sensor_history_data.append(data)
    if len(sensor_history_data) > 100:
        sensor_history_data.pop(0)

    return JsonResponse(data)


def sensor_history(request):
    """获取历史传感器数据"""
    return JsonResponse({'history': sensor_history_data})


def home(request):
    return JsonResponse({
        'message': 'Welcome to the homepage!',
        'available_endpoints': {
            'POST /greet/': 'Send a JSON with "name" to get a greeting',
            'GET /sensor/data/': 'Get latest sensor data',
            'GET /sensor/history/': 'Get historical sensor data',
            'GET /sensor/dashboard/': 'View sensor data dashboard'
        }
    })


def sensor_dashboard(request):
    """传感器数据仪表盘页面"""
    return TemplateResponse(request, 'sensor_dashboard.html', {})