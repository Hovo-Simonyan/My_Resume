from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import DeletionMixin

from .forms import *
from .models import *


def home(request):
    context = {'selected': 0, 'title': 'Резюме онлайн и бесплатно'}
    return render(request, 'mysite/home_page.html', context=context)


class PublishedResume(ListView):
    paginate_by = 4
    model = Resume
    template_name = 'mysite/published_resume.html'
    context_object_name = 'resumes'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 1
        context['title'] = 'Готовые резюме'
        context['xz'] = 'Selected'
        if self.request.user.is_authenticated:
            if Resume.objects.filter(user=self.request.user):
                context['is_there'] = 'True'
        return context

    def get_queryset(self):
        return Resume.objects.filter(is_published=True)


class PublishedByLanguages(ListView):
    paginate_by = 4
    model = Resume
    template_name = 'mysite/published_resume.html'
    context_object_name = 'resumes'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 1
        context['title'] = 'Готовые резюме'
        context['select'] = self.kwargs['lang_slug']
        if self.request.user.is_authenticated:
            if Resume.objects.filter(user=self.request.user):
                context['is_there'] = 'True'
        return context

    def get_queryset(self):
        return Resume.objects.filter(is_published=True, language__slug=self.kwargs['lang_slug'])


class ShowPost(DetailView):
    model = Resume
    template_name = 'mysite/read_more.html'

    context_object_name = 'resume'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Конкретно'
        context['selected'] = 4
        return context

    def get_object(self, queryset=None):
        post = get_object_or_404(Resume, pk=self.kwargs['pk'])
        if self.request.user != post.user:
            post.view += 1
            post.save()

        return post


class ShowUserPosts(LoginRequiredMixin, ListView):
    paginate_by = 4
    model = Resume
    template_name = 'mysite/published_resume.html'
    context_object_name = 'resumes'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 1
        context['title'] = 'Готовые резюме'
        if Resume.objects.filter(user=self.request.user):
            context['is_there'] = 'True'
        context['selected_my'] = 'True'

        return context

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


class AddResume(LoginRequiredMixin, CreateView):
    form_class = AddResumeForm
    template_name = 'mysite/add_new_resume.html'
    success_url = reverse_lazy('home')
    raise_exception = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 2
        context['title'] = 'Добавить резюме'
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateResume(UpdateView):
    model = Resume
    template_name = 'mysite/update_resume.html'
    form_class = AddResumeForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 2
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Resume, pk=self.kwargs['pk'], user=self.request.user)


# class DeleteResume(LoginRequiredMixin, DeleteView):
#     template_name = 'mysite/delete_resume.html'
#
#     def get_object(self, queryset=None):
#         return get_object_or_404(Resume, pk=self.kwargs['pk'], user=self.request.user)
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['selected'] = 2
#         return context
#
#     def get_success_url(self):
#         return reverse('published_resume')

def delete_resume(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    resume.delete()
    return redirect('published_resume')

class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'mysite/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = 3
        context['header_selected'] = 2
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'mysite/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Войти на сайт'
        context['selected'] = 3
        context['header_selected'] = 1
        return context

    def get_success_url(self):
        return reverse_lazy('home')



def logout_user(request):
    logout(request)
    return redirect('login')
