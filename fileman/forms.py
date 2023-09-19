from django import forms
from fileman.models import File


class UpdateFileForm(forms.ModelForm):

    class Meta:
        model = File
        fields = ('file',)
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-control', 'required': True})
        }
