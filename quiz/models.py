from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    question = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    correct_answer = models.CharField(max_length=200)
    subject = models.CharField(max_length=100, verbose_name="Предметная область")

    def __str__(self):
        return self.title

class TaskResult(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=200)
    is_correct = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.task.title} – {'Правильно' if self.is_correct else 'Неправильно'}"