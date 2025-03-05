from django import forms
from .models import UploadedFile

# Form for handling CSV file uploads
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile  # Associates the form with the UploadedFile model
        fields = ['file']  # Only includes the 'file' field in the form
