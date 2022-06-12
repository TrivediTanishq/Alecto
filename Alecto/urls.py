from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name ="home"),
    path('classify/', views.classify, name ="classify"),
    path('result/', views.result, name ="result"),
    path('documentation/', views.documentation, name='documentation'),
    path('download-file/', views.download_file, name ="download-file")
]
