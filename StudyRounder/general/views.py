from django.views import generic
from django.conf import settings
from django.shortcuts import redirect


class TopView(generic.TemplateView):
    template_name = "top.html"
