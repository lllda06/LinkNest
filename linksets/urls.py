from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'linksets'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),  # страница с коллекциями
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('collections/<int:pk>/', views.CollectionDetailView.as_view(), name='collection_detail'),  # коллекция с элементами
    path('collections/create/', views.CollectionCreateView.as_view(), name='collection_create'),  # создание коллекции
    path('items/create/', views.ItemCreateView.as_view(), name='item_create'),  # создание элемента
]