from django.conf.urls import patterns, url
from profiles import views
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = patterns("",
    url(r'^$', TemplateView.as_view(template_name='create_profile.html'), name='create_profile'),
    url(r'^edit_profile/$', login_required(TemplateView.as_view(template_name='edit_profile.html')), name='edit_profile'),
    url(r'^edit_course/$', login_required(views.CourseEdit.as_view()), name='edit_course'),
    url(r'^create_course/$', login_required(TemplateView.as_view(template_name='create_course.html')), name='create_course'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),
)

