from django import forms
from .models import Image , Task


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        label = "image",
        widget = forms.ClearableFileInput(attrs={"multiple": True})
    )
    class Meta:
        model = Image
        fields = ("image",)
        
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [ 'task_title', 'task_text', 'priority', 'quantity_left']
        exclude = ['client']
        