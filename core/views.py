from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from .forms import TaskForm
from .models import Task


# Create your views here.


@require_http_methods(["GET"])
def task_list(request):
    hide_completed = request.GET.get('hide_completed')
    tasks = Task.objects.all()
    # hide completed parameters is passed. so hide them
    if hide_completed:
        tasks = tasks.filter(done_by=None)

    return render(request, 'core/task_list.html', {'tasks': tasks})


@login_required
@require_http_methods(["GET", "POST"])
def task_add(request):
    form = TaskForm()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            url = reverse('task_list')
            return redirect(url)

    return render(request, 'core/add_edit_task.html', {'form': form})


@login_required
@csrf_exempt
@require_http_methods(["GET", "POST", "PATCH", "DELETE"])
def task_modify(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    # is_done can be done by any user
    if request.method == "PATCH":
        is_done = request.read()
        if is_done:
            task.done_by = request.user
            task.save()
            return HttpResponse(status=200)

    # own user can only edit
    if task.user != request.user:
        raise PermissionDenied

    if request.method == "DELETE":
        task.delete()
        return HttpResponse(status=204)

    form = TaskForm(instance=task)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            url = reverse('task_list')
            return redirect(url)

    return render(request, 'core/add_edit_task.html', {'form': form})
