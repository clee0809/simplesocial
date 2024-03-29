"""simplesocial URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from  . import views # from simplesocial import views

## for media files 
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('admin/', admin.site.urls),
	path('test/', views.TestPage.as_view(), name='test'),
    path('thanks/', views.ThanksPage.as_view(), name='thanks'),    
    path('accounts/', include('accounts.urls', namespace='accounts')), # for creating accounts app
    path('accounts/', include('django.contrib.auth.urls')), # for default account which comes through django
    
    path('posts/', include('posts.urls', namespace='posts')),
	path('groups/', include('groups.urls', namespace='groups')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # media files
