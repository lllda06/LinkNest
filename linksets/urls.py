from django.urls import path
from . import views

app_name = 'linksets'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),
    path('collections/create/', views.CollectionCreateView.as_view(), name='collection_create'),
    path('items/create/<int:collection_pk>/', views.ItemCreateView.as_view(), name='item_create'),
]