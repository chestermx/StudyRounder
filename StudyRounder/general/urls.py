from django.conf.urls import url
from . import views
from django.contrib.auth.decorators import login_required
from StudyRounder import settings
from django.conf.urls.static import static

app_name = 'general'
urlpatterns = [
    url(r'^$', views.LoginView.as_view(), name="login"),
    url(r'^top/$', login_required(views.TopView.as_view()), name="top"),
    url(r'^achievement/$', login_required(views.AchievementView.as_view()), name="achievement"),
    url(r'^register/$', views.RegisterView.as_view(), name="register"),
    url(r'^question/(?P<pk>[0-9]+)/$', login_required(views.QuestionView.as_view()), name="question"),
    url(r'^login/$', views.LoginView.as_view(), name="login"),
    url(r'^logout/$', views.LogoutView.as_view(), name="logout"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)