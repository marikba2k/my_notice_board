from .models import Notice
from django import forms

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ["title", "body"]  