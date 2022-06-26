from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.index,name='index'),
    path('user_signup', views.user_signup, name='user_signup'),
    path('user_login', views.user_login, name='user_login'),
    path('user_logout', views.user_logout, name='user_logout'),
    path('upload', views.upload, name='upload'),
    path('details', views.details, name='details'),
    path('new', views.new, name='new'),
    #path('delete/<int:id>',views.delete_view ,name='delete'),
    path('delete/<int:id>', views.destroy), 
    #path("password_reset", views.password_reset_request, name="password_reset"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name="password_reset"),
    path('password_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_done.html'), name='password_reset_complete'),  
     
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
