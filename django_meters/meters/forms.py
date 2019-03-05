from django import forms
from .models import Meters, ResourceType

class MetersForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Name'}),max_length=64, required=True)
    resource_type = forms.ModelChoiceField(queryset=ResourceType.objects.all(),
                                           widget=forms.Select(attrs={'class' : 'custom-select', 'placeholder': 'Resource type'}),
                                           required=True,)
    unit = forms.CharField(widget=forms.TextInput(attrs={'class' : 'form-control', 'placeholder': 'Unit'}),max_length=10, required=True)

    class Meta:
        model = Meters
        fields = ('name', 'resource_type', 'unit')


class CSVUploadForm(forms.Form):
    file = forms.FileField(label="Choose file", widget=forms.FileInput(attrs={'class' : 'custom-file', 'placeholder': 'Choose file', 'accept': '.csv'}))