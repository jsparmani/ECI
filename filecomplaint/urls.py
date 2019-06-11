"""filecomplaint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path,include
from django.contrib.auth import views as auth_views
from django.conf import settings
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


from .import views


admin.site.site_header = 'ELECTION COMMISSION OF INDIA'
admin.site.site_title = 'Election Commission Of India Administration'
admin.site.index_title = 'Election Commission Of India Administration'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.HomePage.as_view(), name='home'),
    path('fault/<str:fault>/', views.fault_page, name='fault'),
    path('accounts/', include('accounts.urls',namespace='accounts')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('welcome/', views.WelcomePage.as_view(),name='welcome'),
    path('thanks/', views.ThanksPage.as_view(),name='thanks'),
    path('complaints/', include('complaints.urls',namespace='complaints')),
    path('sms/', include('sms.urls',namespace='sms')),
    path('admin/password_reset/', auth_views.PasswordResetView.as_view(), name='admin_password_reset'),
    path('admin/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
