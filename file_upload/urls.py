from django.urls import path
from .views import upload_file, get_task_status

urlpatterns = [
    path('', upload_file, name='upload_file'), 
    path('task-status/<str:task_id>/', get_task_status, name='task_status'),
    
]
