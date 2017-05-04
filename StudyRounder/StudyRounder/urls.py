from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^', include('general.urls')),
    url(r'^admin/', admin.site.urls),
    # url(r'^oauth/', include('social.apps.django_app.urls', namespace='social')),
    # url('', include('django.contrib.auth.urls', namespace='auth')),
    # url("r'^login/$", 'django.contrib.auth.views.login', {'template_name': 'register.html'}),

]
