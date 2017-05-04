from .models import SRUser
from django import forms
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout


class IndexView(generic.TemplateView):
    template_name = "index.html"


class RegisterForm(forms.ModelForm):
    class Meta:
        model = SRUser
        fields = ["username", "password"]


class LoginView(generic.FormView):
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("general:top")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("general:top")
        return super(LoginView, self).get(request)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        login(user=user, request=self.request)
        return super(LoginView, self).form_valid(form)

    def form_invalid(self, form):
        print("Error, username or password is not match...")
        return super(LoginView, self).form_invalid(form)


class LogoutView(generic.View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect("general:login")


class TopView(generic.TemplateView):
    template_name = "top.html"


class RegisterView(generic.FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("general:top")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("general:top")
        return super(RegisterView, self).get(request)

    def form_valid(self, form):
        # user = RegisterForm(request.POST).save(commit=False)
        user = SRUser.objects.create_user(form.cleaned_data["username"], form.cleaned_data["password"])
        login(user=user, request=self.request)
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)


class QuestionView(generic.TemplateView):
    template_name = "question.html"
