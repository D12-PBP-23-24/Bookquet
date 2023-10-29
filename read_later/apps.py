from django.apps import AppConfig


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dashboard'

class ReadLaterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'read_later'
