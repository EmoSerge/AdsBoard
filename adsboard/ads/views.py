from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from ads.forms import *

from ads.models import *


class AdsList(ListView):
    model = Advert
    ordering = '-time_add'
    template_name = 'ads.html'
    context_object_name = 'ads'
    paginate_by = 20


class Ad(DetailView):
    model = Advert
    template_name = 'ad.html'
    context_object_name = 'ad'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        responses = Response.objects.filter(advert=self.object, status_delete=False)
        context['responses'] = responses
        return context


class AdCreate(LoginRequiredMixin, CreateView):
    form_class = AdForm
    model = Advert
    template_name = 'ad_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)


class AdUpdate(LoginRequiredMixin, UpdateView):
    form_class = AdForm
    model = Advert
    template_name = 'ad_edit.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if request.user == self.object.author:
            self.object.post()
            return HttpResponseRedirect(success_url)
        else:
            return self.handle_no_permission()


class AdDelete(LoginRequiredMixin, DeleteView):
    model = Advert
    template_name = 'ad_delete.html'
    success_url = reverse_lazy('ads')
    context_object_name = 'ad'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        if request.user == self.object.author:
            self.object.post()
            return HttpResponseRedirect(success_url)
        else:
            return self.handle_no_permission()


class UserAdsList(ListView):
    model = Advert
    ordering = '-time_add'
    template_name = 'profile.html'
    context_object_name = 'ads'
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        author_ads = Advert.objects.filter(author=self.request.user)
        responses = Response.objects.filter(advert__author=self.request.user, status_delete=False)
        context['author_ads'] = author_ads
        context['responses'] = responses
        return context


class Resp(DetailView):
    model = Response
    template_name = 'resp.html'
    context_object_name = 'resp'


class ResponseCreate(LoginRequiredMixin, CreateView):
    model = Response
    form_class = ResponseForm
    template_name = 'response_create.html'
    context_object_name = 'advert'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        advert = Advert.objects.get(id=self.kwargs.get('pk'))
        context['advert'] = advert
        return context

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.buyer = User.objects.get(id=self.request.user.pk)
        self.object.advert = Advert.objects.get(id=self.kwargs.get('pk'))
        self.object.save()
        return super().form_valid(form)


class RespAccept(LoginRequiredMixin, UpdateView):
    model = Response
    template_name = 'resp_accept.html'
    form_class = ResponseAcceptForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('profile')
        if request.user == self.object.advert.author:
            self.object.status_accept = True
            self.object.save()
            return HttpResponseRedirect(success_url)
        else:
            return self.handle_no_permission()


class RespDelete(LoginRequiredMixin, UpdateView):
    model = Response
    template_name = 'resp_delete.html'
    form_class = ResponseAcceptForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = reverse_lazy('profile')
        if request.user == self.object.advert.author:
            self.object.status_delete = True
            self.object.save()
            return HttpResponseRedirect(success_url)
        else:
            return self.handle_no_permission()
