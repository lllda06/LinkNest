from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Collection, Item
from django.urls import reverse_lazy

# PAGE WITH COLLECTIONS
class DashboardView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'linksets/dashboard.html'
    context_object_name = 'collections'

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)

# PAGE WITH COLLECTION DETAILS
class CollectionDetailView(DetailView):
    model = Collection
    template_name = 'linksets/collection_detail.html'
    context_object_name = 'collection'

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)

# PAGE FOR CREATION NEW COLLECTION
class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    template_name = 'linksets/collection_form.html'
    fields = ['title', 'description', 'visibility', 'emoji', 'color']
    success_url = reverse_lazy('linksets:dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# PAGE FOR CREATION NEW ELEMENT
class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'linksets/item_form.html'
    fields = ['title', 'url', 'note', 'tags', 'image']

    def form_valid(self, form):
        form.instance.collection = Collection.objects.get(pk=self.kwargs['collection_pk'])
        return super().form_valid(form)
    def get_success_url(self):
        return reverse_lazy('linksets:collection_detail', kwargs={'pk':self.kwargs['collection_pk']})