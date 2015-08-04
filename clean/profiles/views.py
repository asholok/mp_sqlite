from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils import translation
from django.core.urlresolvers import reverse

def login_user(request):
    logout(request)
    if request.POST:
        password = request.POST['password']
        username = request.POST['username']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/')

def change_language(request):
    if request.GET:
        lang = request.GET.get('language', '')
        if lang:
            translation.activate(lang)
            print translation.get_language()
            request.LANGUAGE_CODE = translation.get_language()
            return HttpResponseRedirect(reverse('home'))
            
    
    return HttpResponseRedirect('/')


class CourseEdit(TemplateView):
    template_name = 'edit_course.html'

    def get_context_data(self, **kwargs):
        print "aaaaaaaaaa", self.args
        context = super(CourseEdit, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['resource'] = self.request.GET['resource']
        return context
        

# Create your views here.
