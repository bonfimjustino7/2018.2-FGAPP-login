"""login URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls import url, include
from . import views
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import refresh_jwt_token
from rest_framework_jwt.views import verify_jwt_token
# from rest_framework import routers
# from authentication.views import UserViewSet

# router = routers.DefaultRouter()
# router.register(r'users', UserViewSet, base_name='users')
# urlpatterns = router.urls

urlpatterns = [
    #'',
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.singIn),
    url(r'^postsign/',views.postsign),
    url(r'^', include('accounts.urls')),
    url(r'^signup/',views.signUp,name='signup'),
    url(r'^postsignup/',views.postsignup,name='postsignup'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

]
