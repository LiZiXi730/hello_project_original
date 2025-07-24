# hello_app/views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .sensor_simulator import I2CSensorSimulator
from .tasks import data_collector
import csv

# 启动数据收集器
data_collector.start()


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


def home(request):
    return JsonResponse({
        'message': 'Welcome to the homepage!',
        'available_endpoints': {
            'POST /greet/': 'Send a JSON with "name" to get a greeting',
            'GET /sensor/data/': 'Get latest sensor data',
            'GET /sensor/history/': 'Get historical sensor data'
        }
    })


def sensor_data(request):
    """获取最新传感器数据"""
    sensor = I2CSensorSimulator()
    data = sensor.read_sensors()
    return JsonResponse(data)


def sensor_history(request):
    """获取历史数据"""
    sensor = I2CSensorSimulator()
    history = []

    try:
        with open(sensor.report_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                history.append(row)

        # 支持限制返回数量
        limit = int(request.GET.get('limit', 100))
        return JsonResponse({'history': history[-limit:]})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)