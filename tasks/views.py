from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# se crean las vistas como controladores, una funcion por vista(archivo.html)


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "Username already exists."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Passwords did not match."})


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'GET':
        return render(request, 'task_create.html', {'form': TaskForm})
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_create.html', {'form': TaskForm, 'error': 'Please privide valida data.'})
        
@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        tasks = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=tasks)
        return render(request, 'task_detail.html', {'task': tasks, 'form': form})
    else:
        try:
            tasks = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=tasks)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html',{'task':tasks, 'form': TaskForm,
                         'error': 'Error updating task. Please provide valid data.'})

@login_required
def completed_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        if user is not None:
            login(request, user)
            return redirect('tasks')
        else:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Username or password is incorrect.'})