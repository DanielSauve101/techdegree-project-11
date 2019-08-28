from django.urls import include, path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh import views


# API endpoints
urlpatterns = format_suffix_patterns([
    path('api/user/login/', obtain_auth_token, name='login-user'),
    path('api/user/', views.UserRegisterView.as_view(), name='register-user'),
    path('favicon\.ico',
        RedirectView.as_view(
            url='/static/icons/favicon.ico',
            permanent=True
        )),
    path('', TemplateView.as_view(template_name='index.html'))
])
