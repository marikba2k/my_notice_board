from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from .models import Notice
from .forms import NoticeForm
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin



class NoticeListView(ListView):
    model = Notice
    template_name = "notices/notice_list.html"
    context_object_name = "notices"
    paginate_by = 10


class NoticeDetailView(DetailView):
    model = Notice
    template_name = "notices/notice_detail.html"
    context_object_name = "notice"

class NoticeCreateView(LoginRequiredMixin,CreateView): 
    model = Notice
    form_class = NoticeForm
    template_name = "notices/notice_form.html"
    success_url = reverse_lazy("notices:list")

    def form_valid(self, form):
            form.instance.author = self.request.user
            return super().form_valid(form)

class NoticeUpdateView(LoginRequiredMixin,UpdateView):
    model = Notice
    form_class = NoticeForm
    template_name = "notices/notice_form.html"
    success_url = reverse_lazy("notices:list")

    def get_queryset(self):
        return Notice.objects.filter(author=self.request.user)

class NoticeDeleteView(LoginRequiredMixin,DeleteView):
    model = Notice
    success_url = reverse_lazy("notices:list")
    template_name = "notices/notice_confirm_delete.html"
    context_object_name = "notice"

    def get_queryset(self):
        return Notice.objects.filter(author=self.request.user)
