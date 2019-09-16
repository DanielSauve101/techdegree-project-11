from django.urls import include, path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

from pugorugh.views import (UserRegisterView, ListDogView, RetrieveDogView,
                            UpdateDogStatusView, RetrieveUpdateUserPrefView)


# API endpoints
urlpatterns = format_suffix_patterns([
    path('api/user/login/', obtain_auth_token, name='login-user'),
    path('api/user/', UserRegisterView.as_view(), name='register-user'),
    path('api/user/preferences/', RetrieveUpdateUserPrefView.as_view(), name=('user-pref')),
    path('api/dog/', ListDogView.as_view(), name=('dog-list')),
    path('api/dog/<int:pk>/<str:decision>/next/', RetrieveDogView.as_view(), name=('dog-decision')),
    path('api/dog/<int:pk>/<str:decision>/', UpdateDogStatusView.as_view(), name=('dog-status')),
    path('favicon\.ico', RedirectView.as_view(url='/static/icons/favicon.ico', permanent=True)),
    path('', TemplateView.as_view(template_name='index.html'))
])
