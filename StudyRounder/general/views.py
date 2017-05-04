from .models import SRUser, Question
from django import forms
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class RegisterForm(forms.ModelForm):
    class Meta:
        model = SRUser
        fields = ["username", "password"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "text", "clear_user"]


class IndexView(generic.TemplateView):
    template_name = "index.html"


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

    def get_context_data(self, **kwargs):
        context = super(TopView, self).get_context_data(**kwargs)
        question_list = Question.objects.all()

        context["question_list"] = question_list
        return context


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


class QuestionView(generic.DetailView, generic.FormView):
    template_name = "question.html"
    model = Question
    form_class = QuestionForm

    def get_queryset(self):
        self.queryset = Question.objects.all()
        return super(QuestionView, self).get_queryset()

    def get_context_data(self, **kwargs):
        context = super(QuestionView, self).get_context_data(**kwargs)
        clear_flag = False

        if self.request.user in list(self.get_object().clear_user.all()):
            clear_flag = True

        context["question"] = self.get_object()
        context["clear_flag"] = clear_flag
        return context

    def post(self, *args, **kwargs):
        add_remove_action = self.request.POST["add_remove_action"]

        if add_remove_action == "1":
            self.get_object().clear_user.add(self.request.user)
        elif add_remove_action == "2":
            self.get_object().clear_user.remove(self.request.user)
        else:
            pass

        return HttpResponseRedirect("/question/%d/" % int(kwargs.get("pk")))
