from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('<int:pk>/', views.DetailArticleView.as_view(), name='detail_article'),
    path('<int:pk>/likes/', views.LikeArticle.as_view(), name='like_article'),
    path('featured/', views.Featured.as_view(), name='featured'),
    path('<int:pk>/delete/', views.DeleteArticleView.as_view(), name='delete_article'),
]
