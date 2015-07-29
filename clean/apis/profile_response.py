import json
from tastypie import resources, fields
from tastypie.authorization import Authorization
from profiles.models import Profile, Course, CourseType
from django.contrib.auth.models import User
from django.http import HttpResponse
from tastypie.exceptions import ImmediateHttpResponse

class LocalProfileAuth(Authorization):
    def read_list(self, object_list, bundle):
        return object_list.filter(user=bundle.request.user)
    
    def update_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user
    
    def read_detail(self, object_list, bundle):
        return bundle.obj.user == bundle.request.user

class LocalUserAuth(Authorization):
    def read_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

    def update_detail(self, object_list, bundle):
        return bundle.obj == bundle.request.user

class LocalCourseAuth(Authorization):   
    def read_list(self, object_list, bundle):
        allowed = []

        for obj in object_list:
            if obj.owner.user == bundle.request.user:
                allowed.append(obj)
        return allowed

    def read_detail(self, object_list, bundle):
        print 'LocalCourseAuth - read_detail'
        return bundle.obj.owner.user == bundle.request.user

    def update_detail(self, object_list, bundle):
        return bundle.obj.owner.user == bundle.request.user

    def create_detail(self, object_list, bundle):
        print 'LocalCourseAuth - create_detail'
        return bundle.obj.owner.user == bundle.request.user


class CourseTypeResource(resources.ModelResource):
    class Meta:
        queryset = CourseType.objects.all()
        fields = ['id', 'name']
        allowed_methods = ['get']
        resource_name = 'course_type'
        authorization = Authorization()

""" ***************** Private ************************************************ """

class PrivateUserResource(resources.ModelResource):
    class Meta:
        queryset = User.objects.all()
        excludes = ['password', 'is_active', 'is_staff', 'is_superuser']
        resource_name = 'private_user'
        allowed_methods = ['get', 'put']
        authorization = LocalUserAuth()

class PrivateProfileResource(resources.ModelResource):
    user = fields.ForeignKey(PrivateUserResource, 'user', full=True, null=True, blank=True)

    class Meta:
        queryset = Profile.objects.all()
        object_class = Profile
        resource_name = 'private_profile'
        fields = ['user', 'zip_code', 'country', 'city', 'user_desciption']
        allowed_methods = ['get', 'put']
        always_return_data = True
        authorization = LocalProfileAuth()
        filtering = {'user': resources.ALL_WITH_RELATIONS}  


    print 'PrivateProfileResource'


class PrivateCourseResource(resources.ModelResource):
    owner = fields.ForeignKey(PrivateProfileResource, 'owner', full=True)
    course_type = fields.ForeignKey(CourseTypeResource, 'course_type', full=True)

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'private_course'
        fields = ['course_name', 'course_type', 'course_desciption', 'owner', 'price']
        allowed_methods = ['get', 'put', 'post']
        always_return_data = True
        authorization = LocalCourseAuth()
        filtering = {
            'owner': resources.ALL_WITH_RELATIONS,
            'course_type': resources.ALL_WITH_RELATIONS
        }

    def obj_create(self, bundle, request=None, **kwargs):
        print 'PrivateCourseResource - obj_create'
        bundle.data['owner'] = Profile.objects.get(user=bundle.request.user)
        bundle.data['price'] = int(bundle.data['price'])
        bundle.data['course_type'] = CourseType.objects.get(id=bundle.data['course_type'])
        
        print bundle.data
        
        super(PrivateCourseResource, self).obj_create(bundle, request=request, **kwargs)
        print 'bjaka'
        return ImmediateHttpResponse(response=HttpResponse(
                                            content=json.dumps({'response': 'ok'}),
                                            status=200
                                        ))
    # def authorized_update_list(self, object_list, bundle):
    #     return object_list.filter(user=bundle.request.user)

""" ***************** End Private ********************************************* """

""" ***************** Public ************************************************** """

class PublicUserResource(resources.ModelResource):
    class Meta:
        queryset = User.objects.all()
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
        resource_name = 'user'
        allowed_methods = ['get', 'post']
        filtering = {'id': ('exact',)}

class PublicProfileResource(resources.ModelResource):
    user = fields.ForeignKey(PublicUserResource, 'user')

    class Meta:
        queryset = Profile.objects.all()
        resource_name = 'profile'
        fields = ['user', 'zip_code', 'country', 'city', 'user_desciption']
        allowed_methods = ['get', 'post']
        always_return_data = True
        authorization = Authorization()
        filtering = {'user': resources.ALL_WITH_RELATIONS}

    def obj_create(self, bundle, request=None, **kwargs):
        print "obj_create"
        print bundle.data
        try:
            User.objects.get(username=bundle.data.get('username'))
            error_response = {'error':'Already exists a user with this username!'}
            raise ImmediateHttpResponse(response=HttpResponse(
                                            content=json.dumps(error_response),
                                            status=400
                                        ))
        except User.DoesNotExist:
            user = User.objects.create_user(
                    username=bundle.data.pop('username'), 
                    email=bundle.data.pop('email'), 
                    password=bundle.data.pop('password')
                )

            bundle.data['user'] = user
            print user
            super(PublicProfileResource, self).obj_create(bundle, request=request, **kwargs)
            raise ImmediateHttpResponse(response=HttpResponse(
                                            content=json.dumps({'response': 'ok'}),
                                            status=200
                                        ))

             

class PublicCourseResource(resources.ModelResource):
    owner = fields.ForeignKey(PublicProfileResource, 'profile')

    class Meta:
        queryset = Course.objects.all()
        resource_name = 'course'
        fields = ['course_name', 'course_type', 'course_desciption', 'owner']
        allowed_methods = ['get', 'post']
        always_return_data = True
        filtering = {'owner': resources.ALL_WITH_RELATIONS}



""" ***************** End Public *********************************************** """



