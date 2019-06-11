from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.urls import path
from .import views

app_name = 'accounts'

urlpatterns = [
    # path('login/',auth_views.LoginView.as_view(template_name = 'accounts/login.html'), name = 'login'),
    path('login/', views.TempLogin, name='login'),
    path('login/1/<int:pk>/', views.login, name='permanent_login'),
    path('logout/',auth_views.LogoutView.as_view(), name = 'logout'),
    path('add_user/',views.add_user,name='add_user'),
    path('add_voter/<str:username>/',views.add_voter,name='add_voter'),
    path('add_gov_user/',views.add_gov_user,name='add_gov_user'),
    path('add_gov_user_phone/<str:username>/',views.add_gov_user_phone,name='add_gov_user_phone'),
    path('add_constituency/',views.add_constituency, name = 'add_constituency'),
    path('add_complaint_type/',views.add_complaint_type, name = 'add_complaint_type'),
    path('update_constituency/',views.update_constituency, name = 'update_constituency'),
    path('constituency_list/', views.ConstituencyList.as_view(), name = 'constituency_list'),
]