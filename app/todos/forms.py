from django import forms

from members.models import User
from .models import Todo


class TodosForm(forms.Form):
    choice = Todo.PRIORITY_CHOICE
    content = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control'
    }))
    priority = forms.ChoiceField(choices=choice, widget=forms.Select(attrs={
        'class': 'custom-select'
    }))

    def save(self, user_id):
        user = User.objects.get(pk=user_id)
        Todo.objects.create(
            user=user,
            content=self.cleaned_data['content'],
            priority=self.cleaned_data['priority'],
        )

