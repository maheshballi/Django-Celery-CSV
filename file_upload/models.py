from django.db import models

# Model to store uploaded CSV files
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')  # Stores the uploaded file in the 'uploads/' directory
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Stores the timestamp when the file was uploaded

    def __str__(self):
        return self.file.name  # Returns the file name as the string representation
