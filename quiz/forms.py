from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """Форма для добавления и редактирования задачи."""

    class Meta:
        model = Task
        fields = ['title', 'question', 'option1', 'option2', 'option3', 'correct_answer', 'subject']


class AnswerForm(forms.Form):
    """Форма для получения ответа от пользователя на задачу."""

    user_answer = forms.CharField(label="Ваш ответ", max_length=200)

    def __init__(self, *args, **kwargs):
        """Инициализация формы с возможностью передавать валидные варианты ответа."""
        self.valid_options = kwargs.pop('valid_options', [])
        super().__init__(*args, **kwargs)

    def clean_user_answer(self):
        """Проверка ответа пользователя."""
        answer = self.cleaned_data['user_answer'].strip()

        # Проверяем, что ответ не пустой
        if not answer:
            raise forms.ValidationError("Ответ не может быть пустым.")

        # Проверяем, что ответ является одним из предложенных вариантов
        if answer not in self.valid_options:
            raise forms.ValidationError("Ответ должен быть одним из предложенных вариантов.")

        return answer
