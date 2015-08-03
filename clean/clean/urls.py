"""clean URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from profiles import views
from tastypie.api import Api
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import activate
from apis.profile_response import *

v1_api = Api(api_name='v1')
v1_api.register(PrivateUserResource())
v1_api.register(PrivateProfileResource())
v1_api.register(PrivateCourseResource())
v1_api.register(PublicUserResource())
v1_api.register(PublicProfileResource())
v1_api.register(PublicCourseResource())
v1_api.register(CourseTypeResource())
v1_api.register(CourseSearchResource())

urlpatterns = patterns('',)

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^profile/', include('profiles.urls', namespace='profile')),
    url(r'^search/', TemplateView.as_view(template_name='search.html'), name='search'),
    url(r'^langs/$', views.change_language, name='lang'),
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

)
