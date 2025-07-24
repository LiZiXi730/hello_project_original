from django.apps import AppConfig

class HelloAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hello_app'

    def ready(self):
        """应用启动时启动数据收集器"""
        from .tasks import data_collector
        data_collector.start()