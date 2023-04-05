from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views import View
from django import forms
from django.urls import reverse
from task_manager.models import User, Status
from task_manager import forms
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'base.html')


class UsersListView(View):

    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        return render(request, 'user_list.html', context={
            'users': users,
        })


class CreateUser(View):

    def get(self, request, *args, **kwargs):
        form = forms.UserCreateForm()
        return render(request, 'create_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.save()
            return redirect(reverse('login'))
        return render(request, 'create_user.html', {'form': form})


class UpdateUser(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        if user_id != request.user.id:
            messages.warning(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect(reverse('users_list'))
        updated_user = User.objects.get(id=user_id)
        form = forms.UserUpdateForm(instance=updated_user)
        return render(request, 'update_user.html', {'form': form, 'updated_user': updated_user, 'id': user_id})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id != request.user.id:
            messages.warning(request, 'Вы не можете редактировать этого юзера')
            return redirect(reverse('users_list'))
        user = User.objects.get(id=user_id)
        form = forms.UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)  # Создаем объект user, но не сохраняем его в базе данных
            user.set_password(request.POST.get('password'))  # Устанавливаем зашифрованный пароль
            user.save()
            return redirect(reverse('users_list'))
        return render(request, 'update_user.html', {'form': form})


class DeleteUser(View):
    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        if user_id != request.user.id:
            messages.warning(request, 'У вас нет прав для изменения другого пользователя.')
            return redirect(reverse('users_list'))
        deleted_user = User.objects.get(id=user_id)
        return render(request, 'delete_user.html', {'user': deleted_user})

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('id')
        if user_id != request.user.id:
            messages.warning(request, 'Вы не можете редактировать этого юзера')
            return redirect(reverse('users_list'))
        deleted_user = User.objects.get(id=user_id)
        deleted_user.delete()
        return redirect(reverse('users_list'))


class LoginUser(View):

    def get(self, request, *args, **kwargs):
        form = forms.LoginForm()
        return render(request, 'login_user.html', {'form': form})

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if request.user.is_authenticated:
                messages.success(request, 'Вы залогинены')
            return redirect(reverse('users_list'))
        else:
            messages.warning(request, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
            return render(request, 'login_user.html', {'form': forms.LoginForm()})


class LogoutUser(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect(reverse('index'))


class StatusesListView(View):

    def get(self, request, *args, **kwargs):
        statuses = Status.objects.all()
        return render(request, 'status_list.html', context={
            'statuses': statuses,
        })


class CreateStatus(View):

    def get(self, request, *args, **kwargs):
        form = forms.StatusCreateForm()
        return render(request, 'create_status.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.StatusCreateForm(request.POST)
        if form.is_valid():
            status = form.save(commit=False)
            status.save()
            messages.success(request, 'Статус успешно создан')
            return redirect(reverse('statuses_list'))
        return render(request, 'create_status.html', {'form': form})


class UpdateStatus(View):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        updated_status = Status.objects.get(id=status_id)
        form = forms.StatusUpdateForm(instance=updated_status)
        return render(request, 'update_status.html', {'form': form, 'updated_status': updated_status, 'id': status_id})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        status = Status.objects.get(id=status_id)
        form = forms.StatusUpdateForm(request.POST, instance=status)
        if form.is_valid():
            status = form.save(commit=False)
            status.save()
            messages.success(request, 'Статус успешно изменён')
            return redirect(reverse('statuses_list'))
        return render(request, 'update_status.html', {'form': form})
    
    
class DeleteStatus(View):
    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        deleted_status = Status.objects.get(id=status_id)
        return render(request, 'delete_status.html', {'status': deleted_status})

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('id')
        if not request.user.id:
            messages.warning(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            return redirect(reverse('login'))
        deleted_status = Status.objects.get(id=status_id)
        deleted_status.delete()
        messages.success(request, 'Статус успешно удалён')
        return redirect(reverse('statuses_list'))
