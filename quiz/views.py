"""Представления для работы с задачами."""

from django.shortcuts import render, get_object_or_404, redirect
from .models import Task, TaskResult
from .forms import TaskForm, AnswerForm
from django.db.models import Q


def add_task(request):
    """Добавление новой задачи."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'quiz/add_task.html', {'form': form})


def task_list(request):
    """Список всех задач, сгруппированных по предмету."""
    tasks = Task.objects.all()  # pylint: disable=no-member
    tasks_by_subject = {}
    for task in tasks:
        tasks_by_subject.setdefault(task.subject, []).append(task)
    return render(request, 'quiz/task_list.html', {'tasks_by_subject': tasks_by_subject})


def answer_task(request, task_id):
    """Обработка ответа пользователя на задачу."""
    task = get_object_or_404(Task, pk=task_id)  # pylint: disable=no-member
    result = None

    if request.method == 'POST':
        valid_options = [task.option1, task.option2, task.option3]
        form = AnswerForm(request.POST, valid_options=valid_options)
        if form.is_valid():
            user_answer = form.cleaned_data['user_answer']
            is_correct = user_answer == task.correct_answer
            TaskResult.objects.create(  # pylint: disable=no-member
                task=task,
                user_answer=user_answer,
                is_correct=is_correct
            )
            result = is_correct
    else:
        valid_options = [task.option1, task.option2, task.option3]
        form = AnswerForm(valid_options=valid_options)

    return render(request, 'quiz/answer_task.html', {
        'task': task,
        'form': form,
        'result': result
    })


def recent_results(request):
    """Показ последних результатов выполнения заданий."""
    results = TaskResult.objects.order_by('-created_at')[:10]  # pylint: disable=no-member
    return render(request, 'quiz/recent_results.html', {'results': results})


def search_task(request):
    """Поиск задачи по названию."""
    query = request.GET.get('q', '').strip()
    tasks = []

    if query:
        tasks = Task.objects.filter(title__icontains=query)  # pylint: disable=no-member

    return render(request, 'quiz/search_task.html', {
        'query': query,
        'tasks': tasks,
    })


def search_by_subject(request):
    """Поиск задач по предметной области."""
    query = request.GET.get('q', '').strip()
    results = []

    if query:
        results = Task.objects.filter(subject__icontains=query)  # pylint: disable=no-member

    return render(request, 'quiz/search_by_subject.html', {
        'query': query,
        'results': results
    })
