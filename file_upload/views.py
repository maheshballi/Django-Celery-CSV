import os
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse
from celery.result import AsyncResult
from celery import current_app
from .models import UploadedFile
from .forms import UploadFileForm
from .tasks import process_csv  

def upload_file(request):
    """
    Handles file upload and triggers Celery task for processing.
    """
    if request.method == 'POST':
        print("Received a POST request.")  # Debugging statement
        
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save()  # Save file to database
            
            print(f"Received file: {uploaded_file.file.name}")  # Debugging statement

            # Ensure MEDIA_ROOT exists
            os.makedirs(settings.MEDIA_ROOT, exist_ok=True)

            # Get the file path safely
            file_path = uploaded_file.file.path

            # Check if the file actually exists on the server
            if os.path.exists(file_path):
                print(f"File saved at: {file_path}")  # Debugging statement
            else:
                print(f"File path does not exist: {file_path}")  # Debugging statement
                return JsonResponse({'error': 'File was not saved correctly'}, status=500)

            # Trigger Celery task asynchronously
            try:
                task_result = process_csv.delay(file_path)
                print(f"Celery task triggered with ID: {task_result.id}")  # Debugging statement
                return JsonResponse({
                    'message': 'File uploaded successfully!',
                    'task_id': task_result.id,
                    'file_name': uploaded_file.file.name,
                }, status=200)
            except Exception as e:
                print(f"Error in triggering Celery task: {e}")  # Debugging statement
                return JsonResponse({'error': str(e)}, status=500)
        else:
            print("Invalid form submission.")  # Debugging statement
            return JsonResponse({'error': 'Invalid form submission'}, status=400)

    else:
        print("Received a GET request.")  # Debugging statement
        form = UploadFileForm()

    return render(request, 'upload.html', {'form': form})

def get_task_status(request, task_id):
    """
    Check the status of a Celery task and return a JSON response.
    Handles serialization errors and failed task states properly.
    """
    task_result = AsyncResult(task_id, app=current_app)
    response_data = {
        'task_id': task_id,
        'status': task_result.state,
    }

    if task_result.ready():
        try:
            # Ensure the result is JSON serializable
            result = task_result.result
            if isinstance(result, Exception):
                response_data['result'] = str(result)  # Convert exception to string
            else:
                response_data['result'] = result
        except Exception as e:
            response_data['result'] = f"Error retrieving result: {str(e)}"
    else:
        response_data['result'] = None  # Task still processing

    return JsonResponse(response_data)