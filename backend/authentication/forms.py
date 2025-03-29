from django import forms
from django.contrib.auth.models import User
from .models import Worker


class WorkerForm(forms.ModelForm):
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Worker
        fields = ['phone', 'skills', 'availability']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        worker = super().save(commit=False)
        worker.user = user
        if commit:
            worker.save()
        return worker