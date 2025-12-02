from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy

from .models import Collection, Item


class DashboardView(LoginRequiredMixin, ListView):
    model = Collection
    template_name = 'linksets/dashboard.html'
    context_object_name = 'collections'

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)


class CollectionDetailView(LoginRequiredMixin, DetailView):
    model = Collection
    template_name = 'linksets/collection_detail.html'
    context_object_name = 'collection'

    def get_queryset(self):
        return Collection.objects.filter(owner=self.request.user)


class CollectionCreateView(LoginRequiredMixin, CreateView):
    model = Collection
    template_name = 'linksets/collection_form.html'
    fields = ['title', 'description', 'visibility', 'emoji', 'color']
    success_url = reverse_lazy('linksets:dashboard')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    template_name = 'linksets/item_form.html'
    fields = ['title', 'url', 'note', 'tags', 'image']

    def dispatch(self, request, *args, **kwargs):
        # один раз на запрос достаём коллекцию или 404
        self.collection = get_object_or_404(
            Collection,
            pk=kwargs['collection_pk'],
            owner=request.user,  # дополнительно защищаем от чужих коллекций
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.collection = self.collection
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['collection'] = self.collection
        return ctx

    def get_success_url(self):
        return reverse_lazy('linksets:collection_detail', kwargs={'pk': self.collection.pk})