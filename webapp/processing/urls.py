from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process_image/', views.process_image, name='process_image'),
    path('image_list/', views.image_list, name='image_list'),
    path('image/delete/<int:image_id>/', views.delete_image, name='delete_image'),

]
