from .models import SRUser, Question, Category
from django import forms
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import generic
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout

# 自分で順番を指定できるかつ, 自動更新できるようにする
show_category_list = ["javascript", "jquery", "node.js"]
# show_category_list = ["javascript", "jquery", "node.js", "express", "react", "other", "vue.js", "angular.js",
#                       "material design", "electron", "php", "python", "flask"]


# Form
class RegisterForm(forms.ModelForm):
    class Meta:
        model = SRUser
        fields = ["username", "password"]


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["title", "text", "clear_user"]


# View
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


class RegisterView(generic.FormView):
    template_name = "register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("general:top")

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect("general:top")
        return super(RegisterView, self).get(request)

    def form_valid(self, form):
        user = SRUser.objects.create_user(form.cleaned_data["username"], form.cleaned_data["password"])
        login(user=user, request=self.request)
        return super(RegisterView, self).form_valid(form)

    def form_invalid(self, form):
        return super(RegisterView, self).form_invalid(form)


class TopView(generic.TemplateView):
    template_name = "top.html"

    def get_context_data(self, **kwargs):
        context = super(TopView, self).get_context_data(**kwargs)
        nested_question_list = []

        for category_name in show_category_list:
            nested_question_list.append(list(Question.objects.filter(category__name=category_name).all()))

        context["zipped_category_question_list"] = zip(show_category_list, nested_question_list)
        context["choose_number"] = 0
        context["question_list"] = Question.objects.all()
        return context


class AchievementView(generic.TemplateView):
    template_name = "achievement.html"

    def get_context_data(self, **kwargs):
        context = super(AchievementView, self).get_context_data(**kwargs)
        achievement_rate_list = []

        # ユーザのトータルの達成率を算出
        question_all = Question.objects.all()
        clear_all = Question.objects.filter(clear_user=self.request.user)

        # ユーザのカテゴリ毎の達成率を算出
        for category in show_category_list:
            category_question_all = Question.objects.filter(category=Category.objects.filter(name=category))
            category_clear_all = Question.objects.filter(category=Category.objects.filter(name=category),
                                                         clear_user=self.request.user)
            if len(category_question_all) != 0:
                achievement_rate_list.append('{:.1f}'.format((len(category_clear_all) / len(category_question_all))*100))
            else:
                achievement_rate_list.append('{:.1f}'.format(0))

        # すべてのユーザのスコアを算出
        all_username_total_score = []
        for user in SRUser.objects.all():
            all_username_total_score.append([user.username,
                                             sum(x.point for x in Question.objects.filter(clear_user=user))])

        # すべてのユーザをランキング順にソート
        sorted_all_username_total_score = sorted(all_username_total_score, key=lambda x: x[1], reverse=True)

        context["result_clear_all_rate"] = '{:.1f}'.format((len(clear_all) / len(question_all))*100)
        context["result_category_achievementrate"] = zip(show_category_list, achievement_rate_list)
        context["sorted_all_username_total_score"] = sorted_all_username_total_score
        context["choose_number"] = 1
        context["question_list"] = Question.objects.all()
        return context


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
        context["choose_number"] = 2
        context["question_list"] = Question.objects.all()
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
