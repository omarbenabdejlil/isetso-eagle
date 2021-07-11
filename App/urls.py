from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.homePage, name='homePage'),
    path('detail/<int:id>/', views.detailPage, name='detailPage'),
    path('deleteMachine', csrf_exempt(views.deleteMachine), name='deleteMachine'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', views.logout, name='logout'),
]