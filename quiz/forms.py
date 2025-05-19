from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'question', 'option1', 'option2', 'option3', 'correct_answer',
                  'subject']

class AnswerForm(forms.Form):
    user_answer = forms.CharField(label="Ваш ответ", max_length=200)

    def __init__(self, *args, **kwargs):
        self.valid_options = kwargs.pop('valid_options', [])
        super().__init__(*args, **kwargs)

    def clean_user_answer(self):
        answer = self.cleaned_data['user_answer'].strip()
        if not answer:
            raise forms.ValidationError("Ответ не может быть пустым.")
        if answer not in self.valid_options:
            raise forms.ValidationError("Ответ должен быть одним из предложенных вариантов.")
        return answer
