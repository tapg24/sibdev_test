from django.urls import path

from . import views

app_name = 'board'
urlpatterns = [
    # /board/
    path('', views.IndexView.as_view(), name='index'),
    # /board/1
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    # /board/add
    path('add/', views.AdCreateView.as_view(), name='add'),
    # /board/update/1
    path('update/<int:pk>/', views.AdUpdateView.as_view(), name='update'),
    # /board/delete/1
    path('delete/<int:pk>/', views.AdDeleteView.as_view(), name='delete'),
    # /board/special
    path('special/', views.special, name='special'),
]