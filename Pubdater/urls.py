from django.contrib import admin
from django.urls import path
from Backend import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/process/', views.processUpdate),
]
