from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Notice


class NoticeListView(ListView):
    model = Notice
    template_name = "notices/notice_list.html"
    context_object_name = "notices"
    paginate_by = 10


class NoticeDetailView(DetailView):
    model = Notice
    template_name = "notices/notice_detail.html"
    context_object_name = "notice"
