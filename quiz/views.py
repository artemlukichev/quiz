from django.shortcuts import render, get_object_or_404, redirect
from collections import defaultdict
from .models import Task, TaskResult
from .forms import TaskForm, AnswerForm

def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'quiz/add_task.html', {'form': form})

def search_task(request):
    query = request.GET.get('q')
    tasks = Task.objects.filter(title__icontains=query) if query else []
    return render(request, 'quiz/search_task.html', {'tasks': tasks, 'query': query})

def search_by_subject(request):
    query = request.GET.get('q')
    results = []

    if query:
        results = Task.objects.filter(subject__icontains=query)

    return render(request, 'quiz/search_by_subject.html', {
        'query': query,
        'results': results
    })

def task_list(request):
    tasks_by_subject = {}
    tasks = Task.objects.all().order_by('subject', 'title')

    for task in tasks:
        tasks_by_subject.setdefault(task.subject, []).append(task)

    return render(request, 'quiz/task_list.html', {
        'tasks_by_subject': tasks_by_subject
    })

def answer_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['user_answer']
            is_correct = user_answer.strip().lower() == task.correct_answer.strip().lower()

            # Сохраняем результат
            TaskResult.objects.create(
                task=task,
                user_answer=user_answer,
                is_correct=is_correct
            )

            return render(request, 'quiz/result.html', {
                'task': task,
                'user_answer': user_answer,
                'is_correct': is_correct
            })
    else:
        form = AnswerForm()

    return render(request, 'quiz/answer_task.html', {'task': task, 'form': form})

def recent_results(request):
    results = TaskResult.objects.order_by('-created_at')[:10]
    return render(request, 'quiz/recent_results.html', {'results': results})