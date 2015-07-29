from django.shortcuts import render
from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
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

class CourseEdit(TemplateView):
    template_name = 'edit_course.html'

    def get_context_data(self, **kwargs):
        context = super(CourseEdit, self).get_context_data(**kwargs)
        if self.request.method == 'GET':
            context['resource'] = self.request.GET['resource']
        return context
        

# Create your views here.
