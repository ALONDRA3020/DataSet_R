
from django.contrib import admin
from django.urls import path
from data import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.dataset_upload_view, name='dataset_upload_view'),
]


